from typing import List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, selectinload

from backend.app.models.performance import (
    PerformanceSnapshot,
    StudentSubjectPerformance,
    StudentTopicPerformance,
)
from backend.app.models.user import User


class PerformanceRepository:
    @staticmethod
    def get_subject_performance_by_user(db: Session, user_id: str) -> List[StudentSubjectPerformance]:
        stmt = (
            select(StudentSubjectPerformance)
            .options(selectinload(StudentSubjectPerformance.subject))
            .where(StudentSubjectPerformance.user_id == user_id)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_topic_performance_by_user(db: Session, user_id: str) -> List[StudentTopicPerformance]:
        stmt = (
            select(StudentTopicPerformance)
            .options(selectinload(StudentTopicPerformance.topic))
            .where(StudentTopicPerformance.user_id == user_id)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_latest_snapshot(db: Session, user_id: str) -> Optional[PerformanceSnapshot]:
        stmt = (
            select(PerformanceSnapshot)
            .where(PerformanceSnapshot.user_id == user_id)
            .order_by(PerformanceSnapshot.timestamp.desc())
        )
        return db.scalar(stmt)

    @staticmethod
    def get_leaderboard(db: Session, limit: int = 50) -> List[tuple]:
        """Fetch top performers aggregated across completed attempts."""
        # Query total quizzes taken and average score per user
        stmt = (
            select(
                User.id.label("user_id"),
                User.full_name.label("user_name"),
                func.count(StudentSubjectPerformance.subject_id).label("quizzes_taken"),
                func.avg(StudentSubjectPerformance.average_score).label("average_score"),
                func.sum(StudentSubjectPerformance.average_score).label("total_score"),
            )
            .join(StudentSubjectPerformance, StudentSubjectPerformance.user_id == User.id)
            .group_by(User.id, User.full_name)
            .order_by(desc("average_score"), desc("quizzes_taken"))
            .limit(limit)
        )
        return db.execute(stmt).all()
