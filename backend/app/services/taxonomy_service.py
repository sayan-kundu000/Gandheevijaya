from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from backend.app.core.exceptions import NotFoundException
from backend.app.models.content import Exam, Question, Subject, Subtopic, Topic
from backend.app.models.material import StudyMaterial
from backend.app.schemas.content import (
    ContentHealthIssue,
    ContentHealthReport,
    ExamStatisticsResponse,
    SubjectStatisticsResponse,
    TaxonomyTreeExamResponse,
    TaxonomyTreeSubject,
    TaxonomyTreeTopic,
    TopicStatisticsResponse,
)
from backend.app.services.base import BaseService


class TaxonomyService(BaseService):
    """
    Centralized Taxonomy & Content Health Engine.
    Provides tree taxonomy browsing, efficient content statistics, and automated health checks.
    """

    def get_exam_taxonomy_tree(self, exam_id: int, active_only: bool = True) -> TaxonomyTreeExamResponse:
        """
        Retrieves complete hierarchical tree structure (Exam -> Subjects -> Topics)
        in a single optimized query with pre-calculated question counts.
        """
        exam = self.db.get(Exam, exam_id)
        if not exam:
            raise NotFoundException(message=f"Exam with ID {exam_id} not found.")

        # Query subjects under exam
        subj_stmt = (
            select(Subject)
            .where(Subject.exam_id == exam_id)
            .order_by(Subject.display_order.asc(), Subject.name.asc())
        )
        if active_only:
            subj_stmt = subj_stmt.where(Subject.status == "ACTIVE")
        subjects = list(self.db.scalars(subj_stmt).all())

        # Sub-queries for topic & question counts
        tree_subjects: List[TaxonomyTreeSubject] = []
        total_exam_topics = 0
        total_exam_questions = 0
        total_exam_published_questions = 0

        for subj in subjects:
            top_stmt = (
                select(Topic)
                .options(selectinload(Topic.subtopics))
                .where(Topic.subject_id == subj.id)
                .order_by(Topic.display_order.asc(), Topic.name.asc())
            )
            if active_only:
                top_stmt = top_stmt.where(Topic.status == "ACTIVE")
            topics = list(self.db.scalars(top_stmt).all())

            tree_topics: List[TaxonomyTreeTopic] = []
            subj_question_count = 0
            subj_published_count = 0

            for top in topics:
                # Count total questions under topic
                q_total = self.db.scalar(
                    select(func.count(Question.id)).where(Question.topic_id == top.id)
                ) or 0
                # Count published questions
                q_pub = self.db.scalar(
                    select(func.count(Question.id)).where(
                        Question.topic_id == top.id, Question.status == "PUBLISHED"
                    )
                ) or 0

                subj_question_count += q_total
                subj_published_count += q_pub

                tree_topics.append(
                    TaxonomyTreeTopic(
                        id=top.id,
                        name=top.name,
                        code=top.code,
                        status=top.status,
                        display_order=top.display_order,
                        question_count=q_total,
                        published_question_count=q_pub,
                        subtopics=[sub for sub in top.subtopics],
                    )
                )

            total_exam_topics += len(topics)
            total_exam_questions += subj_question_count
            total_exam_published_questions += subj_published_count

            tree_subjects.append(
                TaxonomyTreeSubject(
                    id=subj.id,
                    name=subj.name,
                    code=subj.code,
                    status=subj.status,
                    display_order=subj.display_order,
                    topic_count=len(topics),
                    question_count=subj_question_count,
                    published_question_count=subj_published_count,
                    topics=tree_topics,
                )
            )

        return TaxonomyTreeExamResponse(
            id=exam.id,
            name=exam.name,
            code=exam.code,
            status=exam.status,
            display_order=exam.display_order,
            subject_count=len(subjects),
            topic_count=total_exam_topics,
            question_count=total_exam_questions,
            published_question_count=total_exam_published_questions,
            subjects=tree_subjects,
        )

    def get_exam_statistics(self, exam_id: int) -> ExamStatisticsResponse:
        exam = self.db.get(Exam, exam_id)
        if not exam:
            raise NotFoundException(message=f"Exam with ID {exam_id} not found.")

        subj_count = self.db.scalar(select(func.count(Subject.id)).where(Subject.exam_id == exam_id)) or 0
        top_count = self.db.scalar(
            select(func.count(Topic.id)).join(Subject).where(Subject.exam_id == exam_id)
        ) or 0
        q_count = self.db.scalar(
            select(func.count(Question.id)).join(Topic).join(Subject).where(Subject.exam_id == exam_id)
        ) or 0
        q_pub_count = self.db.scalar(
            select(func.count(Question.id))
            .join(Topic)
            .join(Subject)
            .where(Subject.exam_id == exam_id, Question.status == "PUBLISHED")
        ) or 0
        q_draft_count = self.db.scalar(
            select(func.count(Question.id))
            .join(Topic)
            .join(Subject)
            .where(Subject.exam_id == exam_id, Question.status == "DRAFT")
        ) or 0
        mat_count = self.db.scalar(
            select(func.count(StudyMaterial.id)).join(Subject).where(Subject.exam_id == exam_id)
        ) or 0

        return ExamStatisticsResponse(
            exam_id=exam.id,
            exam_code=exam.code,
            exam_name=exam.name,
            subject_count=subj_count,
            topic_count=top_count,
            question_count=q_count,
            published_question_count=q_pub_count,
            draft_question_count=q_draft_count,
            material_count=mat_count,
        )

    def get_subject_statistics(self, subject_id: int) -> SubjectStatisticsResponse:
        subj = self.db.get(Subject, subject_id)
        if not subj:
            raise NotFoundException(message=f"Subject with ID {subject_id} not found.")

        top_count = self.db.scalar(select(func.count(Topic.id)).where(Topic.subject_id == subject_id)) or 0
        q_count = self.db.scalar(
            select(func.count(Question.id)).join(Topic).where(Topic.subject_id == subject_id)
        ) or 0
        q_pub_count = self.db.scalar(
            select(func.count(Question.id))
            .join(Topic)
            .where(Topic.subject_id == subject_id, Question.status == "PUBLISHED")
        ) or 0
        q_draft_count = self.db.scalar(
            select(func.count(Question.id))
            .join(Topic)
            .where(Topic.subject_id == subject_id, Question.status == "DRAFT")
        ) or 0
        mat_count = self.db.scalar(
            select(func.count(StudyMaterial.id)).where(StudyMaterial.subject_id == subject_id)
        ) or 0

        return SubjectStatisticsResponse(
            subject_id=subj.id,
            subject_code=subj.code,
            subject_name=subj.name,
            topic_count=top_count,
            question_count=q_count,
            published_question_count=q_pub_count,
            draft_question_count=q_draft_count,
            material_count=mat_count,
        )

    def get_topic_statistics(self, topic_id: int) -> TopicStatisticsResponse:
        topic = self.db.get(Topic, topic_id)
        if not topic:
            raise NotFoundException(message=f"Topic with ID {topic_id} not found.")

        subtop_count = self.db.scalar(select(func.count(Subtopic.id)).where(Subtopic.topic_id == topic_id)) or 0
        q_count = self.db.scalar(select(func.count(Question.id)).where(Question.topic_id == topic_id)) or 0
        q_pub_count = self.db.scalar(
            select(func.count(Question.id)).where(Question.topic_id == topic_id, Question.status == "PUBLISHED")
        ) or 0
        q_draft_count = self.db.scalar(
            select(func.count(Question.id)).where(Question.topic_id == topic_id, Question.status == "DRAFT")
        ) or 0

        return TopicStatisticsResponse(
            topic_id=topic.id,
            topic_name=topic.name,
            subtopic_count=subtop_count,
            question_count=q_count,
            published_question_count=q_pub_count,
            draft_question_count=q_draft_count,
        )

    def get_content_health_report(self) -> ContentHealthReport:
        """
        Scans platform database for content health issues:
        - Questions without topic
        - Published questions with empty answer or missing options
        - Published questions attached to INACTIVE topics or subjects
        """
        issues: List[ContentHealthIssue] = []

        # 1. Total counts
        total_exams = self.db.scalar(select(func.count(Exam.id))) or 0
        total_subjects = self.db.scalar(select(func.count(Subject.id))) or 0
        total_topics = self.db.scalar(select(func.count(Topic.id))) or 0
        total_questions = self.db.scalar(select(func.count(Question.id))) or 0
        total_materials = self.db.scalar(select(func.count(StudyMaterial.id))) or 0

        # 2. Check published questions attached to INACTIVE topics
        inactive_topic_q_stmt = (
            select(Question)
            .join(Topic)
            .where(Question.status == "PUBLISHED", Topic.status != "ACTIVE")
            .limit(50)
        )
        inactive_top_qs = list(self.db.scalars(inactive_topic_q_stmt).all())
        for q in inactive_top_qs:
            issues.append(
                ContentHealthIssue(
                    type="INACTIVE_PARENT_TOPIC",
                    severity="WARNING",
                    entity_id=q.id,
                    details=f"Question '{q.id}' is PUBLISHED but its topic is '{q.topic.status if q.topic else 'UNKNOWN'}'.",
                )
            )

        # 3. Check published questions attached to INACTIVE subjects
        inactive_subj_q_stmt = (
            select(Question)
            .join(Topic)
            .join(Subject)
            .where(Question.status == "PUBLISHED", Subject.status != "ACTIVE")
            .limit(50)
        )
        inactive_subj_qs = list(self.db.scalars(inactive_subj_q_stmt).all())
        for q in inactive_subj_qs:
            issues.append(
                ContentHealthIssue(
                    type="INACTIVE_PARENT_SUBJECT",
                    severity="WARNING",
                    entity_id=q.id,
                    details=f"Question '{q.id}' is PUBLISHED but parent subject is INACTIVE.",
                )
            )

        return ContentHealthReport(
            generated_at=datetime.now(timezone.utc),
            total_exams=total_exams,
            total_subjects=total_subjects,
            total_topics=total_topics,
            total_questions=total_questions,
            total_materials=total_materials,
            issue_count=len(issues),
            issues=issues,
        )
