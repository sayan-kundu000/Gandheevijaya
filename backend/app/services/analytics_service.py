from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.attempt import Attempt
from backend.app.models.content import Exam, Question, Subject, Topic
from backend.app.models.quiz import Quiz
from backend.app.models.user import User
from backend.app.repositories.performance_repository import PerformanceRepository
from backend.app.schemas.analytics import (
    AdminStatsResponse,
    LeaderboardEntryResponse,
    SubjectPerformanceItem,
    TopicPerformanceItem,
    UserPerformanceSummary,
)
from backend.app.services.base import BaseService


class AnalyticsService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.perf_repo = PerformanceRepository()

    def get_user_performance_summary(self, user_id: str, user_name: str) -> UserPerformanceSummary:
        subject_perfs = self.perf_repo.get_subject_performance_by_user(self.db, user_id=user_id)
        topic_perfs = self.perf_repo.get_topic_performance_by_user(self.db, user_id=user_id)
        snapshot = self.perf_repo.get_latest_snapshot(self.db, user_id=user_id)

        # Calculate aggregations
        total_quizzes = sum(sp.total_quizzes_taken for sp in subject_perfs)
        avg_score = (
            round(sum(sp.average_score for sp in subject_perfs) / len(subject_perfs), 2)
            if subject_perfs
            else 0.0
        )
        total_q = sum(tp.total_questions_attempted for tp in topic_perfs)

        sub_items = [
            SubjectPerformanceItem(
                subject_id=sp.subject_id,
                subject_name=sp.subject.name if sp.subject else f"Subject {sp.subject_id}",
                total_quizzes_taken=sp.total_quizzes_taken,
                average_score=sp.average_score,
                completion_rate=sp.completion_rate,
                last_updated=sp.last_updated,
            )
            for sp in subject_perfs
        ]

        topic_items = [
            TopicPerformanceItem(
                topic_id=tp.topic_id,
                topic_name=tp.topic.name if tp.topic else f"Topic {tp.topic_id}",
                total_questions_attempted=tp.total_questions_attempted,
                correct_attempts=tp.correct_attempts,
                accuracy_percentage=round((tp.correct_attempts / tp.total_questions_attempted * 100), 2)
                if tp.total_questions_attempted > 0
                else 0.0,
                average_time_per_question=tp.average_time_per_question,
                weakness_score=tp.weakness_score,
                last_updated=tp.last_updated,
            )
            for tp in topic_perfs
        ]

        return UserPerformanceSummary(
            user_id=user_id,
            user_name=user_name,
            overall_accuracy=snapshot.overall_accuracy if snapshot else avg_score,
            total_quizzes_completed=total_quizzes,
            total_questions_attempted=total_q,
            subject_performance=sub_items,
            weak_topics=sorted(topic_items, key=lambda t: t.weakness_score, reverse=True)[:5],
            score_trend=snapshot.score_trend if snapshot and snapshot.score_trend else [],
        )

    def get_leaderboard(self, limit: int = 50) -> List[LeaderboardEntryResponse]:
        rows = self.perf_repo.get_leaderboard(self.db, limit=limit)
        leaderboard = []
        for idx, row in enumerate(rows, start=1):
            leaderboard.append(
                LeaderboardEntryResponse(
                    rank=idx,
                    user_id=row.user_id,
                    user_name=row.user_name or "Anonymous Student",
                    quizzes_taken=row.quizzes_taken,
                    average_score=round(float(row.average_score or 0.0), 2),
                    total_score=round(float(row.total_score or 0.0), 2),
                )
            )
        return leaderboard

    def get_admin_dashboard_stats(self) -> AdminStatsResponse:
        total_users = self.db.scalar(select(func.count()).select_from(User)) or 0
        total_students = self.db.scalar(select(func.count()).select_from(User).where(User.role == "STUDENT")) or 0
        total_admins = self.db.scalar(select(func.count()).select_from(User).where(User.role == "ADMIN")) or 0
        total_exams = self.db.scalar(select(func.count()).select_from(Exam)) or 0
        total_subjects = self.db.scalar(select(func.count()).select_from(Subject)) or 0
        total_topics = self.db.scalar(select(func.count()).select_from(Topic)) or 0
        total_questions = self.db.scalar(select(func.count()).select_from(Question)) or 0
        total_quizzes = self.db.scalar(select(func.count()).select_from(Quiz)) or 0
        total_attempts = self.db.scalar(select(func.count()).select_from(Attempt)) or 0

        return AdminStatsResponse(
            total_users=total_users,
            total_students=total_students,
            total_admins=total_admins,
            total_exams=total_exams,
            total_subjects=total_subjects,
            total_topics=total_topics,
            total_questions=total_questions,
            total_quizzes=total_quizzes,
            total_attempts=total_attempts,
        )
