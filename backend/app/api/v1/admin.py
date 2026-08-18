from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, require_admin
from backend.app.etl.importer import QuestionImportService
from backend.app.etl.schemas import ContentImportReport
from backend.app.models.content import Question
from backend.app.models.security_audit import SecurityAuditLog
from backend.app.models.user import User
from backend.app.schemas.admin import (
    AdminAttemptItem,
    AdminDashboardOverviewResponse,
    AdminExamCreateRequest,
    AdminQuestionCreateRequest,
    AdminQuestionUpdateRequest,
    AdminSubjectCreateRequest,
    AdminTopicCreateRequest,
    AdminUserDetailResponse,
    AdminUserItem,
    AdminUserUpdateRequest,
    ContentImportJobDetailResponse,
    ContentImportJobItem,
    UserStatusToggleRequest,
)
from backend.app.schemas.analytics import AdminStatsResponse
from backend.app.schemas.common import PaginatedResponse, PaginationParams
from backend.app.schemas.content import (
    BulkStatusUpdateRequest,
    ContentHealthReport,
    QuestionAdminResponse,
)
from backend.app.schemas.quiz import QuestionPoolInfoResponse, QuizResponse
from backend.app.services.admin_service import AdminManagementService
from backend.app.services.analytics_service import AnalyticsService
from backend.app.services.content_lifecycle_service import ContentLifecycleService
from backend.app.services.quiz_service import QuizService
from backend.app.services.taxonomy_service import TaxonomyService

router = APIRouter(prefix="/admin", tags=["Admin Operations & System Control"])


@router.get("/dashboard", response_model=AdminDashboardOverviewResponse)
def get_admin_dashboard_overview(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retrieve complete administrative overview dashboard statistics."""
    service = AdminManagementService(db)
    return service.get_dashboard_overview()


@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_dashboard_stats(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retrieve system-wide entity counts for administrator dashboard."""
    service = AnalyticsService(db)
    return service.get_admin_dashboard_stats()


# ==================== USER MANAGEMENT ====================

@router.get("/users", response_model=PaginatedResponse[AdminUserItem])
def list_admin_users(
    search: Optional[str] = Query(None, description="Search by email or full name"),
    role: Optional[str] = Query(None, description="Filter by role: STUDENT or ADMIN"),
    is_active: Optional[bool] = Query(None, description="Filter by account status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Paginated user directory listing for administrators."""
    service = AdminManagementService(db)
    return service.list_users(page=page, page_size=page_size, search=search, role=role, is_active=is_active)


@router.get("/users/{user_id}", response_model=AdminUserDetailResponse)
def get_admin_user_detail(
    user_id: str,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retrieve detailed user account metrics and attempt performance summary. Credentials excluded."""
    service = AdminManagementService(db)
    return service.get_user_detail(user_id=user_id)


@router.patch("/users/{user_id}", response_model=AdminUserItem)
def update_admin_user(
    user_id: str,
    body: AdminUserUpdateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update user profile or role. Protected against self-demotion."""
    service = AdminManagementService(db)
    return service.update_user(user_id=user_id, update_data=body, current_admin_id=admin_user.id)


@router.post("/users/{user_id}/disable", response_model=AdminUserDetailResponse)
def disable_user_account(
    user_id: str,
    body: Optional[UserStatusToggleRequest] = None,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Disable a user account. Protected against self-disable action."""
    service = AdminManagementService(db)
    reason = body.reason if body else None
    return service.disable_user(user_id=user_id, current_admin_id=admin_user.id, reason=reason)


@router.post("/users/{user_id}/reactivate", response_model=AdminUserDetailResponse)
def reactivate_user_account(
    user_id: str,
    body: Optional[UserStatusToggleRequest] = None,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Reactivate a disabled user account."""
    service = AdminManagementService(db)
    reason = body.reason if body else None
    return service.reactivate_user(user_id=user_id, current_admin_id=admin_user.id, reason=reason)


# ==================== QUESTION BANK MANAGEMENT ====================

@router.get("/questions", response_model=PaginatedResponse[QuestionAdminResponse])
def list_admin_questions(
    topic_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    question_type: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List questions with administrative filters."""
    params = PaginationParams(page=page, page_size=page_size)
    stmt = select(Question)
    if topic_id:
        stmt = stmt.where(Question.topic_id == topic_id)
    if status:
        stmt = stmt.where(Question.status == status.upper())
    if question_type:
        stmt = stmt.where(Question.type == question_type.upper())
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty.upper())

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    questions = list(db.scalars(stmt.offset(params.offset).limit(params.limit)).all())
    items = [QuestionAdminResponse.model_validate(q) for q in questions]
    return PaginatedResponse.create(items=items, total=total, params=params)


@router.post("/questions", response_model=QuestionAdminResponse)
def create_question(
    body: AdminQuestionCreateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new question record."""
    service = AdminManagementService(db)
    q = service.create_question(req=body, current_admin_id=admin_user.id)
    return QuestionAdminResponse.model_validate(q)


@router.patch("/questions/{question_id}", response_model=QuestionAdminResponse)
def update_question(
    question_id: str,
    body: AdminQuestionUpdateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update question content or taxonomy link."""
    service = AdminManagementService(db)
    q = service.update_question(question_id=question_id, req=body, current_admin_id=admin_user.id)
    return QuestionAdminResponse.model_validate(q)


@router.post("/questions/{question_id}/publish", response_model=QuestionAdminResponse)
def publish_question(
    question_id: str,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Publish a question record."""
    service = ContentLifecycleService(db)
    question = service.publish_question(question_id, user_id=admin_user.id)
    return QuestionAdminResponse.model_validate(question)


@router.post("/questions/{question_id}/unpublish", response_model=QuestionAdminResponse)
def unpublish_question(
    question_id: str,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Unpublish a question record."""
    service = ContentLifecycleService(db)
    question = service.unpublish_question(question_id, user_id=admin_user.id)
    return QuestionAdminResponse.model_validate(question)


@router.post("/questions/{question_id}/archive", response_model=QuestionAdminResponse)
def archive_question(
    question_id: str,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Archive a question record."""
    service = ContentLifecycleService(db)
    question = service.archive_question(question_id, user_id=admin_user.id)
    return QuestionAdminResponse.model_validate(question)


@router.post("/questions/bulk-status")
def bulk_update_question_status(
    body: BulkStatusUpdateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Bulk update lifecycle status for multiple questions."""
    service = ContentLifecycleService(db)
    return service.bulk_update_question_status(
        question_ids=body.item_ids, target_status=body.status, user_id=admin_user.id
    )


# ==================== TAXONOMY MANAGEMENT ====================

@router.post("/exams")
def create_exam(
    body: AdminExamCreateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new Exam taxonomy record."""
    service = AdminManagementService(db)
    exam = service.create_exam(req=body, current_admin_id=admin_user.id)
    return {"id": exam.id, "code": exam.code, "name": exam.name, "status": exam.status}


@router.post("/subjects")
def create_subject(
    body: AdminSubjectCreateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new Subject taxonomy record."""
    service = AdminManagementService(db)
    subject = service.create_subject(req=body, current_admin_id=admin_user.id)
    return {"id": subject.id, "code": subject.code, "name": subject.name, "exam_id": subject.exam_id}


@router.post("/topics")
def create_topic(
    body: AdminTopicCreateRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new Topic taxonomy record."""
    service = AdminManagementService(db)
    topic = service.create_topic(req=body, current_admin_id=admin_user.id)
    return {"id": topic.id, "code": topic.code, "name": topic.name, "subject_id": topic.subject_id}


# ==================== QUIZ & ATTEMPT MONITORING ====================

@router.post("/quizzes/{quiz_id}/publish", response_model=QuizResponse)
def publish_quiz(
    quiz_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Publish a quiz after question pool validation."""
    service = QuizService(db)
    return service.publish_quiz(quiz_id)


@router.post("/quizzes/{quiz_id}/archive", response_model=QuizResponse)
def archive_quiz(
    quiz_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Archive a quiz."""
    service = QuizService(db)
    return service.archive_quiz(quiz_id)


@router.get("/quizzes/{quiz_id}/question-pool", response_model=QuestionPoolInfoResponse)
def inspect_quiz_question_pool(
    quiz_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Inspect available published question pool for a quiz."""
    service = QuizService(db)
    return service.inspect_question_pool(quiz_id)


@router.get("/attempts", response_model=PaginatedResponse[AdminAttemptItem])
def list_admin_attempts(
    user_id: Optional[str] = Query(None),
    quiz_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Monitor student quiz attempts."""
    service = AdminManagementService(db)
    return service.list_attempts(page=page, page_size=page_size, user_id=user_id, quiz_id=quiz_id, status=status)


# ==================== INGESTION & HEALTH MONITORING ====================

@router.get("/content/health", response_model=ContentHealthReport)
def get_content_health_report(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Run content health validation scan for orphan records or inactive taxonomy."""
    service = TaxonomyService(db)
    return service.get_content_health_report()


@router.get("/imports", response_model=PaginatedResponse[ContentImportJobItem])
def list_import_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List JSON ETL import job history."""
    service = AdminManagementService(db)
    return service.list_import_jobs(page=page, page_size=page_size)


@router.get("/imports/{job_id}", response_model=ContentImportJobDetailResponse)
def get_import_job_detail(
    job_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retrieve detailed import job record and validation errors."""
    service = AdminManagementService(db)
    return service.get_import_job_detail(job_id=job_id)


@router.post("/import/questions", response_model=ContentImportReport)
def trigger_question_import(
    source_path: str = Query("datasets", description="Source path or directory for JSON import"),
    dry_run: bool = Query(False, description="Dry run mode (preview without database mutation)"),
    upsert: bool = Query(False, description="Upsert mode for updating existing duplicates"),
    subject: Optional[str] = Query(None, description="Default subject code or name override"),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Trigger question bank JSON ETL ingestion."""
    service = QuestionImportService(db)
    return service.run_import(
        source_path=source_path,
        is_dry_run=dry_run,
        upsert_mode=upsert,
        default_subject_code=subject,
    )


@router.get("/audit-logs")
def list_security_audit_logs(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """View append-only security audit trail logs."""
    params = PaginationParams(page=page, page_size=page_size)
    stmt = select(SecurityAuditLog)
    if event_type:
        stmt = stmt.where(SecurityAuditLog.event_type == event_type)
    if user_id:
        stmt = stmt.where(SecurityAuditLog.user_id == user_id)

    stmt = stmt.order_by(SecurityAuditLog.created_at.desc())

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = list(db.scalars(stmt.offset(params.offset).limit(params.limit)).all())

    logs_data = [
        {
            "id": log.id,
            "user_id": log.user_id,
            "event_type": log.event_type,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "details": log.details,
            "created_at": log.created_at,
        }
        for log in items
    ]
    return PaginatedResponse.create(items=logs_data, total=total, params=params)
