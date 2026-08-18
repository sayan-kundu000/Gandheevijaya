from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import case, func, or_, select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    ValidationException,
)
from backend.app.models.attempt import Attempt
from backend.app.models.content import Exam, Question, Subject, Topic
from backend.app.models.import_audit import ContentImport, ContentImportError
from backend.app.models.quiz import Quiz, QuizQuestion
from backend.app.models.security_audit import SecurityAuditLog
from backend.app.models.user import User
from backend.app.schemas.admin import (
    AdminAttemptItem,
    AdminDashboardOverviewResponse,
    AdminExamCreateRequest,
    AdminQuestionCreateRequest,
    AdminQuestionUpdateRequest,
    AdminQuizCreateRequest,
    AdminQuizUpdateRequest,
    AdminSubjectCreateRequest,
    AdminTopicCreateRequest,
    AdminUserDetailResponse,
    AdminUserItem,
    AdminUserUpdateRequest,
    ContentImportJobDetailResponse,
    ContentImportJobItem,
)
from backend.app.schemas.common import PaginatedResponse, PaginationParams
from backend.app.services.base import BaseService


class AdminManagementService(BaseService):
    """
    Core Operational Control & System Governance Engine for Administrators.
    Manages users, question bank records, quizzes, content taxonomy, attempt monitoring,
    ETL import history, and append-only security audit trail generation.
    """

    def _log_audit(self, admin_id: str, event_type: str, details: Dict[str, Any]):
        """Records an administrative mutation in append-only SecurityAuditLog."""
        audit_entry = SecurityAuditLog(
            user_id=admin_id,
            event_type=event_type,
            details=details,
        )
        self.db.add(audit_entry)
        self.db.flush()

    def get_dashboard_overview(self) -> AdminDashboardOverviewResponse:
        """Calculates system-wide administrative stats across users, content, assessment attempts, and imports."""
        total_users = self.db.scalar(select(func.count()).select_from(User)) or 0
        total_students = self.db.scalar(select(func.count()).select_from(User).where(User.role == "STUDENT")) or 0
        total_admins = self.db.scalar(select(func.count()).select_from(User).where(User.role == "ADMIN")) or 0
        disabled_users = self.db.scalar(select(func.count()).select_from(User).where(User.is_active == False)) or 0

        # Active students (students with at least 1 completed attempt)
        active_students_stmt = select(func.count(func.distinct(Attempt.user_id))).where(Attempt.status.in_(["SUBMITTED", "EXPIRED"]))
        active_students = self.db.scalar(active_students_stmt) or 0

        # Content counts
        total_exams = self.db.scalar(select(func.count()).select_from(Exam)) or 0
        total_subjects = self.db.scalar(select(func.count()).select_from(Subject)) or 0
        total_topics = self.db.scalar(select(func.count()).select_from(Topic)) or 0

        total_questions = self.db.scalar(select(func.count()).select_from(Question)) or 0
        published_q = self.db.scalar(select(func.count()).select_from(Question).where(Question.status == "PUBLISHED")) or 0
        draft_q = self.db.scalar(select(func.count()).select_from(Question).where(Question.status == "DRAFT")) or 0
        archived_q = self.db.scalar(select(func.count()).select_from(Question).where(Question.status == "ARCHIVED")) or 0

        total_quizzes = self.db.scalar(select(func.count()).select_from(Quiz)) or 0
        published_quizzes = self.db.scalar(select(func.count()).select_from(Quiz).where(Quiz.status == "PUBLISHED")) or 0

        # Assessment attempts
        total_attempts = self.db.scalar(select(func.count()).select_from(Attempt)) or 0
        completed_att = self.db.scalar(select(func.count()).select_from(Attempt).where(Attempt.status.in_(["SUBMITTED", "EXPIRED"]))) or 0
        active_att = self.db.scalar(select(func.count()).select_from(Attempt).where(Attempt.status == "IN_PROGRESS")) or 0

        # Scoring averages
        score_stmt = select(
            func.avg(Attempt.score).label("avg_score"),
            func.sum(Attempt.correct_count).label("tot_corr"),
            func.sum(Attempt.attempted_count).label("tot_att"),
        ).where(Attempt.status.in_(["SUBMITTED", "EXPIRED"]))

        score_row = self.db.execute(score_stmt).one()
        avg_score = round(float(score_row.avg_score or 0.0), 2)
        tot_corr = score_row.tot_corr or 0
        tot_att = score_row.tot_att or 0
        accuracy = round((tot_corr / tot_att * 100.0), 2) if tot_att > 0 else 0.0

        # Import jobs
        total_imports = self.db.scalar(select(func.count()).select_from(ContentImport)) or 0

        return AdminDashboardOverviewResponse(
            total_users=total_users,
            total_students=total_students,
            total_admins=total_admins,
            active_students=active_students,
            disabled_users=disabled_users,
            total_exams=total_exams,
            total_subjects=total_subjects,
            total_topics=total_topics,
            total_questions=total_questions,
            published_questions=published_q,
            draft_questions=draft_q,
            archived_questions=archived_q,
            total_quizzes=total_quizzes,
            published_quizzes=published_quizzes,
            total_attempts=total_attempts,
            completed_attempts=completed_att,
            active_attempts=active_att,
            global_average_score=avg_score,
            global_accuracy=accuracy,
            total_import_jobs=total_imports,
        )

    # ==================== USER MANAGEMENT ====================

    def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[AdminUserItem]:
        """Lists users with pagination, search, role filtering, and attempt count summary."""
        params = PaginationParams(page=page, page_size=page_size)
        stmt = select(User)

        if search:
            search_pattern = f"%{search.strip()}%"
            stmt = stmt.where(or_(User.email.ilike(search_pattern), User.full_name.ilike(search_pattern)))
        if role:
            stmt = stmt.where(User.role == role.upper())
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)

        stmt = stmt.order_by(User.created_at.desc())

        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        users = list(self.db.scalars(stmt.offset(params.offset).limit(params.limit)).all())

        items: List[AdminUserItem] = []
        for u in users:
            tot_att = self.db.scalar(select(func.count(Attempt.id)).where(Attempt.user_id == u.id)) or 0
            last_act = self.db.scalar(select(func.max(Attempt.started_at)).where(Attempt.user_id == u.id))
            items.append(
                AdminUserItem(
                    id=u.id,
                    email=u.email,
                    full_name=u.full_name,
                    role=u.role,
                    is_active=u.is_active,
                    created_at=u.created_at,
                    updated_at=u.updated_at,
                    total_attempts=tot_att,
                    last_activity=last_act,
                )
            )

        return PaginatedResponse.create(items=items, total=total, params=params)

    def get_user_detail(self, user_id: str) -> AdminUserDetailResponse:
        """Retrieves administrative detail for a specific user, strictly excluding credentials."""
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException(f"User {user_id} not found")

        att_stmt = select(
            func.count(Attempt.id).label("total_attempts"),
            func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), 1), else_=0)).label("completed_attempts"),
            func.avg(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.score), else_=None)).label("avg_score"),
            func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.correct_count), else_=0)).label("corr"),
            func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.attempted_count), else_=0)).label("att_q"),
            func.max(Attempt.started_at).label("last_active"),
        ).where(Attempt.user_id == user_id)

        row = self.db.execute(att_stmt).one()

        tot_att = row.total_attempts or 0
        comp_att = row.completed_attempts or 0
        avg_sc = round(float(row.avg_score or 0.0), 2)
        corr = row.corr or 0
        att_q = row.att_q or 0
        acc = round((corr / att_q * 100.0), 2) if att_q > 0 else 0.0

        return AdminUserDetailResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            total_attempts=tot_att,
            completed_attempts=comp_att,
            average_score=avg_sc,
            overall_accuracy=acc,
            last_activity=row.last_active,
        )

    def update_user(self, user_id: str, update_data: AdminUserUpdateRequest, current_admin_id: str) -> AdminUserItem:
        """Updates user details with self-role demotion protection."""
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException(f"User {user_id} not found")

        # Self-demotion check
        if user_id == current_admin_id and update_data.role and update_data.role != "ADMIN":
            raise ForbiddenException("Self-demotion protection: Administrators cannot revoke their own ADMIN role.")

        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.role is not None:
            if update_data.role not in ["STUDENT", "ADMIN"]:
                raise ValidationException(f"Invalid role: {update_data.role}")
            user.role = update_data.role
        if update_data.is_active is not None:
            if user_id == current_admin_id and not update_data.is_active:
                raise ForbiddenException("Self-disable protection: Administrators cannot disable their own account.")
            user.is_active = update_data.is_active

        self.db.flush()
        self._log_audit(current_admin_id, "USER_UPDATED", {"target_user_id": user_id, "updated_fields": update_data.model_dump(exclude_unset=True)})

        return self.list_users(page=1, page_size=1, search=user.email).items[0]

    def disable_user(self, user_id: str, current_admin_id: str, reason: Optional[str] = None) -> AdminUserItem:
        """Disables a user account with self-disable protection."""
        if user_id == current_admin_id:
            raise ForbiddenException("Self-disable protection: You cannot disable your own administrator account.")

        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException(f"User {user_id} not found")

        user.is_active = False
        self.db.flush()
        self._log_audit(current_admin_id, "USER_DISABLED", {"target_user_id": user_id, "reason": reason})

        return self.get_user_detail(user_id)

    def reactivate_user(self, user_id: str, current_admin_id: str, reason: Optional[str] = None) -> AdminUserItem:
        """Reactivates a disabled user account."""
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundException(f"User {user_id} not found")

        user.is_active = True
        self.db.flush()
        self._log_audit(current_admin_id, "USER_REACTIVATED", {"target_user_id": user_id, "reason": reason})

        return self.get_user_detail(user_id)

    # ==================== QUESTION MANAGEMENT ====================

    def create_question(self, req: AdminQuestionCreateRequest, current_admin_id: str) -> Question:
        """Creates a new question record with taxonomy validation and audit logging."""
        topic = self.db.get(Topic, req.topic_id)
        if not topic:
            raise NotFoundException(f"Topic {req.topic_id} not found")

        if req.type not in ["MCQ", "MSQ", "NAT"]:
            raise ValidationException(f"Invalid question type: {req.type}")

        if req.type in ["MCQ", "MSQ"] and not req.options:
            raise ValidationException(f"{req.type} question requires non-empty options dictionary.")

        question_id = f"q_admin_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{req.topic_id}"
        q = Question(
            id=question_id,
            topic_id=req.topic_id,
            difficulty=req.difficulty,
            type=req.type,
            question_text=req.question_text,
            options=req.options,
            correct_answer=req.correct_answer,
            explanation=req.explanation,
            status=req.status,
            created_by=current_admin_id,
        )
        self.db.add(q)
        self.db.flush()

        self._log_audit(current_admin_id, "QUESTION_CREATED", {"question_id": q.id, "topic_id": req.topic_id})
        return q

    def update_question(self, question_id: str, req: AdminQuestionUpdateRequest, current_admin_id: str) -> Question:
        """Updates question details while preserving historical attempt integrity."""
        q = self.db.get(Question, question_id)
        if not q:
            raise NotFoundException(f"Question {question_id} not found")

        if req.topic_id is not None:
            topic = self.db.get(Topic, req.topic_id)
            if not topic:
                raise NotFoundException(f"Topic {req.topic_id} not found")
            q.topic_id = req.topic_id

        if req.difficulty is not None:
            q.difficulty = req.difficulty
        if req.type is not None:
            q.type = req.type
        if req.question_text is not None:
            q.question_text = req.question_text
        if req.options is not None:
            q.options = req.options
        if req.correct_answer is not None:
            q.correct_answer = req.correct_answer
        if req.explanation is not None:
            q.explanation = req.explanation
        if req.status is not None:
            q.status = req.status
        q.updated_by = current_admin_id

        self.db.flush()
        self._log_audit(current_admin_id, "QUESTION_UPDATED", {"question_id": q.id, "updated_fields": req.model_dump(exclude_unset=True)})
        return q

    # ==================== TAXONOMY MANAGEMENT ====================

    def create_exam(self, req: AdminExamCreateRequest, current_admin_id: str) -> Exam:
        """Creates a new Exam taxonomy record."""
        existing = self.db.scalar(select(Exam).where(Exam.code == req.code))
        if existing:
            raise BadRequestException(f"Exam code '{req.code}' already exists.")

        exam = Exam(
            code=req.code,
            name=req.name,
            description=req.description,
            category_id=req.category_id,
            status="ACTIVE" if req.is_active else "INACTIVE",
        )
        self.db.add(exam)
        self.db.flush()
        self._log_audit(current_admin_id, "EXAM_CREATED", {"exam_id": exam.id, "code": exam.code})
        return exam

    def create_subject(self, req: AdminSubjectCreateRequest, current_admin_id: str) -> Subject:
        """Creates a new Subject taxonomy record."""
        exam = self.db.get(Exam, req.exam_id)
        if not exam:
            raise NotFoundException(f"Exam {req.exam_id} not found")

        subject = Subject(
            exam_id=req.exam_id,
            code=req.code,
            name=req.name,
            description=req.description,
            status="ACTIVE" if req.is_active else "INACTIVE",
        )
        self.db.add(subject)
        self.db.flush()
        self._log_audit(current_admin_id, "SUBJECT_CREATED", {"subject_id": subject.id, "code": subject.code})
        return subject

    def create_topic(self, req: AdminTopicCreateRequest, current_admin_id: str) -> Topic:
        """Creates a new Topic taxonomy record."""
        subject = self.db.get(Subject, req.subject_id)
        if not subject:
            raise NotFoundException(f"Subject {req.subject_id} not found")

        topic = Topic(
            subject_id=req.subject_id,
            code=req.code,
            name=req.name,
            description=req.description,
            status="ACTIVE" if req.is_active else "INACTIVE",
        )
        self.db.add(topic)
        self.db.flush()
        self._log_audit(current_admin_id, "TOPIC_CREATED", {"topic_id": topic.id, "code": topic.code})
        return topic

    # ==================== ATTEMPT & INGESTION MONITORING ====================

    def list_attempts(
        self,
        page: int = 1,
        page_size: int = 20,
        user_id: Optional[str] = None,
        quiz_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> PaginatedResponse[AdminAttemptItem]:
        """Lists student quiz attempts for administrative monitoring."""
        params = PaginationParams(page=page, page_size=page_size)
        stmt = (
            select(Attempt)
            .options(joinedload(Attempt.user), joinedload(Attempt.quiz))
            .order_by(Attempt.started_at.desc())
        )

        if user_id:
            stmt = stmt.where(Attempt.user_id == user_id)
        if quiz_id:
            stmt = stmt.where(Attempt.quiz_id == quiz_id)
        if status:
            stmt = stmt.where(Attempt.status == status.upper())

        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        attempts = list(self.db.scalars(stmt.offset(params.offset).limit(params.limit)).all())

        items = [
            AdminAttemptItem(
                id=att.id,
                user_id=att.user_id,
                user_email=att.user.email if att.user else "unknown@student.com",
                quiz_id=att.quiz_id,
                quiz_title=att.quiz.title if att.quiz else f"Quiz {att.quiz_id}",
                status=att.status,
                score=att.score,
                total_marks=att.total_marks,
                percentage=att.percentage,
                accuracy=att.accuracy,
                started_at=att.started_at,
                completed_at=att.completed_at,
            )
            for att in attempts
        ]

        return PaginatedResponse.create(items=items, total=total, params=params)

    def list_import_jobs(self, page: int = 1, page_size: int = 20) -> PaginatedResponse[ContentImportJobItem]:
        """Lists JSON ETL import job history records."""
        params = PaginationParams(page=page, page_size=page_size)
        stmt = select(ContentImport).order_by(ContentImport.created_at.desc())

        total = self.db.scalar(select(func.count()).select_from(ContentImport)) or 0
        jobs = list(self.db.scalars(stmt.offset(params.offset).limit(params.limit)).all())

        items = [ContentImportJobItem.model_validate(j) for j in jobs]
        return PaginatedResponse.create(items=items, total=total, params=params)

    def get_import_job_detail(self, job_id: int) -> ContentImportJobDetailResponse:
        """Retrieves detailed JSON ETL import job metrics and validation error list."""
        job = self.db.scalar(
            select(ContentImport).options(joinedload(ContentImport.errors)).where(ContentImport.id == job_id)
        )
        if not job:
            raise NotFoundException(f"Import job {job_id} not found")

        return ContentImportJobDetailResponse.model_validate(job)
