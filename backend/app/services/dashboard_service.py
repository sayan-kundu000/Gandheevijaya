from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.attempt import Attempt, AttemptAnswer
from backend.app.models.content import Question, Subject, Topic
from backend.app.models.quiz import Quiz
from backend.app.schemas.dashboard import (
    AreaInsightItem,
    AreaInsightListResponse,
    CompactDashboardResponse,
    DashboardOverviewResponse,
    PerformanceTrendItem,
    PerformanceTrendListResponse,
    RecentActivityItem,
    RecentActivityListResponse,
    StudyConsistencyResponse,
    SubjectProgressItem,
    SubjectProgressListResponse,
    TopicProgressItem,
    TopicProgressListResponse,
)
from backend.app.services.base import BaseService


class DashboardService(BaseService):
    """
    Student Dashboard & Learning Progress Aggregation Engine.
    Consumes authoritative Attempt, AttemptAnswer, Quiz, Question, Topic, and Subject records.
    Provides fast, deterministic SQL aggregations for learning analytics.
    """

    def get_overview(self, user_id: str, exam_id: Optional[int] = None) -> DashboardOverviewResponse:
        """Calculates global student dashboard overview metrics using database aggregations."""
        stmt = (
            select(
                func.count(Attempt.id).label("total_attempts"),
                func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), 1), else_=0)).label("completed_attempts"),
                func.sum(case((Attempt.status == "IN_PROGRESS", 1), else_=0)).label("active_attempts"),
                func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.attempted_count), else_=0)).label("questions_attempted"),
                func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.correct_count), else_=0)).label("correct_answers"),
                func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.incorrect_count), else_=0)).label("incorrect_answers"),
                func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.unanswered_count), else_=0)).label("unanswered_questions"),
                func.sum(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.time_taken_seconds), else_=0)).label("total_study_time"),
                func.avg(case((Attempt.status.in_(["SUBMITTED", "EXPIRED"]), Attempt.percentage), else_=None)).label("avg_percentage"),
            )
            .select_from(Attempt)
            .join(Attempt.quiz)
            .where(Attempt.user_id == user_id)
        )

        if exam_id:
            stmt = stmt.where(Quiz.exam_id == exam_id)

        row = self.db.execute(stmt).one()

        tot_att = row.total_attempts or 0
        comp_att = row.completed_attempts or 0
        act_att = row.active_attempts or 0
        q_att = row.questions_attempted or 0
        corr = row.correct_answers or 0
        incorr = row.incorrect_answers or 0
        unans = row.unanswered_questions or 0
        study_time = row.total_study_time or 0
        avg_pct = round(float(row.avg_percentage or 0.0), 2)

        accuracy = round((corr / q_att * 100.0), 2) if q_att > 0 else 0.0

        # Recent activity count in last 30 days
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        recent_cnt_stmt = select(func.count(Attempt.id)).where(
            Attempt.user_id == user_id,
            Attempt.started_at >= thirty_days_ago,
        )
        recent_cnt = self.db.scalar(recent_cnt_stmt) or 0

        return DashboardOverviewResponse(
            total_attempts=tot_att,
            completed_attempts=comp_att,
            active_attempts=act_att,
            questions_attempted=q_att,
            correct_answers=corr,
            incorrect_answers=incorr,
            unanswered_questions=unans,
            overall_accuracy=accuracy,
            average_percentage=avg_pct,
            total_study_time_seconds=study_time,
            recent_activity_count=recent_cnt,
        )

    def get_subject_progress(self, user_id: str, exam_id: Optional[int] = None) -> SubjectProgressListResponse:
        """Aggregates subject-level performance metrics, attempt counts, and unique syllabus coverage."""
        subj_stmt = select(Subject)
        if exam_id:
            subj_stmt = subj_stmt.where(Subject.exam_id == exam_id)
        subjects = list(self.db.scalars(subj_stmt).all())

        items: List[SubjectProgressItem] = []

        for subj in subjects:
            # Query attempts for quizzes in this subject
            att_stmt = (
                select(
                    func.count(Attempt.id).label("attempt_count"),
                    func.sum(Attempt.attempted_count).label("q_attempted"),
                    func.sum(Attempt.correct_count).label("corr"),
                    func.sum(Attempt.incorrect_count).label("incorr"),
                    func.avg(Attempt.score).label("avg_score"),
                    func.max(Attempt.completed_at).label("last_active"),
                )
                .select_from(Attempt)
                .join(Attempt.quiz)
                .where(
                    Attempt.user_id == user_id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                    Quiz.subject_id == subj.id,
                )
            )
            att_row = self.db.execute(att_stmt).one()

            q_att = att_row.q_attempted or 0
            corr = att_row.corr or 0
            incorr = att_row.incorr or 0
            att_cnt = att_row.attempt_count or 0
            avg_sc = round(float(att_row.avg_score or 0.0), 2)
            accuracy = round((corr / q_att * 100.0), 2) if q_att > 0 else 0.0
            last_act = att_row.last_active

            # Unique question coverage calculation
            unique_q_stmt = (
                select(func.count(func.distinct(AttemptAnswer.question_id)))
                .select_from(AttemptAnswer)
                .join(AttemptAnswer.attempt)
                .join(Attempt.quiz)
                .where(
                    Attempt.user_id == user_id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                    Quiz.subject_id == subj.id,
                )
            )
            unique_covered = self.db.scalar(unique_q_stmt) or 0

            tot_q_stmt = (
                select(func.count(Question.id))
                .select_from(Question)
                .join(Question.topic)
                .where(Topic.subject_id == subj.id)
            )
            tot_available = self.db.scalar(tot_q_stmt) or 0

            completion = round((unique_covered / tot_available * 100.0), 2) if tot_available > 0 else 0.0

            items.append(
                SubjectProgressItem(
                    subject_id=subj.id,
                    subject_name=subj.name,
                    exam_id=subj.exam_id,
                    questions_attempted=q_att,
                    correct_answers=corr,
                    incorrect_answers=incorr,
                    accuracy=accuracy,
                    average_score=avg_sc,
                    unique_questions_covered=unique_covered,
                    total_available_questions=tot_available,
                    completion_rate=completion,
                    attempt_count=att_cnt,
                    last_activity=last_act,
                )
            )

        return SubjectProgressListResponse(items=items, total=len(items))

    def get_topic_progress(self, user_id: str, subject_id: Optional[int] = None) -> TopicProgressListResponse:
        """Aggregates topic-level accuracy, question count, and performance status."""
        topic_stmt = select(Topic).options(joinedload(Topic.subject))
        if subject_id:
            topic_stmt = topic_stmt.where(Topic.subject_id == subject_id)
        topics = list(self.db.scalars(topic_stmt).all())

        items: List[TopicProgressItem] = []

        for top in topics:
            ans_stmt = (
                select(
                    func.count(AttemptAnswer.id).label("total_answers"),
                    func.sum(case((AttemptAnswer.is_correct == True, 1), else_=0)).label("correct"),
                    func.sum(case((AttemptAnswer.is_correct == False, 1), else_=0)).label("incorrect"),
                    func.max(AttemptAnswer.answered_at).label("last_active"),
                )
                .select_from(AttemptAnswer)
                .join(AttemptAnswer.attempt)
                .join(AttemptAnswer.question)
                .where(
                    Attempt.user_id == user_id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                    Question.topic_id == top.id,
                )
            )
            ans_row = self.db.execute(ans_stmt).one()

            total_ans = ans_row.total_answers or 0
            corr = ans_row.correct or 0
            incorr = ans_row.incorrect or 0
            last_act = ans_row.last_active

            accuracy = round((corr / total_ans * 100.0), 2) if total_ans > 0 else 0.0

            if total_ans == 0:
                status = "NOT_STARTED"
            elif total_ans < 3:
                status = "PRACTICING"
            elif accuracy >= 80.0:
                status = "STRONG"
            elif accuracy < 60.0:
                status = "WEAK"
            else:
                status = "PRACTICING"

            items.append(
                TopicProgressItem(
                    topic_id=top.id,
                    topic_name=top.name,
                    subject_id=top.subject_id,
                    subject_name=top.subject.name if top.subject else None,
                    questions_attempted=total_ans,
                    correct_answers=corr,
                    incorrect_answers=incorr,
                    accuracy=accuracy,
                    attempt_count=total_ans,
                    performance_status=status,
                    last_activity=last_act,
                )
            )

        return TopicProgressListResponse(items=items, total=len(items))

    def get_recent_activity(self, user_id: str, limit: int = 10) -> RecentActivityListResponse:
        """Retrieves recent quiz attempt activity ordered newest first."""
        stmt = (
            select(Attempt)
            .options(joinedload(Attempt.quiz).joinedload(Quiz.subject))
            .where(Attempt.user_id == user_id)
            .order_by(Attempt.started_at.desc())
            .limit(limit)
        )
        attempts = list(self.db.scalars(stmt).all())

        items = [
            RecentActivityItem(
                attempt_id=att.id,
                quiz_id=att.quiz_id,
                quiz_title=att.quiz.title if att.quiz else f"Quiz {att.quiz_id}",
                subject_name=att.quiz.subject.name if (att.quiz and att.quiz.subject) else None,
                status=att.status,
                score=att.score,
                total_marks=att.total_marks,
                percentage=att.percentage,
                accuracy=att.accuracy,
                completed_at=att.completed_at,
                started_at=att.started_at,
            )
            for att in attempts
        ]

        return RecentActivityListResponse(items=items, total=len(items))

    def get_performance_trend(self, user_id: str, days: int = 30) -> PerformanceTrendListResponse:
        """Groups completed attempts by calendar date to generate time-series accuracy and percentage trends."""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = (
            select(
                func.date(Attempt.started_at).label("day"),
                func.count(Attempt.id).label("attempts_count"),
                func.sum(Attempt.attempted_count).label("q_attempted"),
                func.sum(Attempt.correct_count).label("corr"),
                func.avg(Attempt.percentage).label("avg_pct"),
                func.sum(Attempt.time_taken_seconds).label("study_time"),
            )
            .where(
                Attempt.user_id == user_id,
                Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                Attempt.started_at >= start_date,
            )
            .group_by(func.date(Attempt.started_at))
            .order_by(func.date(Attempt.started_at).asc())
        )

        rows = self.db.execute(stmt).all()
        items = []

        for row in rows:
            q_att = row.q_attempted or 0
            corr = row.corr or 0
            acc = round((corr / q_att * 100.0), 2) if q_att > 0 else 0.0
            avg_pct = round(float(row.avg_pct or 0.0), 2)
            day_str = str(row.day)

            items.append(
                PerformanceTrendItem(
                    date=day_str,
                    attempts_count=row.attempts_count or 0,
                    questions_attempted=q_att,
                    accuracy=acc,
                    average_percentage=avg_pct,
                    study_time_seconds=row.study_time or 0,
                )
            )

        return PerformanceTrendListResponse(items=items)

    def get_weak_areas(
        self, user_id: str, threshold: float = 60.0, min_attempts: int = 3
    ) -> AreaInsightListResponse:
        """Identifies topics where user accuracy is below threshold with sufficient sample size."""
        topic_progress = self.get_topic_progress(user_id=user_id)
        weak_items: List[AreaInsightItem] = []

        for top in topic_progress.items:
            if top.questions_attempted >= min_attempts and top.accuracy < threshold:
                reason = f"Accuracy of {top.accuracy}% is below the target threshold of {threshold}% across {top.questions_attempted} questions."
                weak_items.append(
                    AreaInsightItem(
                        topic_id=top.topic_id,
                        topic_name=top.topic_name,
                        subject_id=top.subject_id,
                        subject_name=top.subject_name or f"Subject {top.subject_id}",
                        accuracy=top.accuracy,
                        questions_attempted=top.questions_attempted,
                        incorrect_answers=top.incorrect_answers,
                        recommendation_reason=reason,
                    )
                )

        weak_items.sort(key=lambda x: x.accuracy)
        return AreaInsightListResponse(items=weak_items, total=len(weak_items))

    def get_strong_areas(
        self, user_id: str, threshold: float = 80.0, min_attempts: int = 3
    ) -> AreaInsightListResponse:
        """Identifies topics where user accuracy meets or exceeds threshold with sufficient sample size."""
        topic_progress = self.get_topic_progress(user_id=user_id)
        strong_items: List[AreaInsightItem] = []

        for top in topic_progress.items:
            if top.questions_attempted >= min_attempts and top.accuracy >= threshold:
                reason = f"High accuracy of {top.accuracy}% demonstrates strong topic mastery across {top.questions_attempted} questions."
                strong_items.append(
                    AreaInsightItem(
                        topic_id=top.topic_id,
                        topic_name=top.topic_name,
                        subject_id=top.subject_id,
                        subject_name=top.subject_name or f"Subject {top.subject_id}",
                        accuracy=top.accuracy,
                        questions_attempted=top.questions_attempted,
                        incorrect_answers=top.incorrect_answers,
                        recommendation_reason=reason,
                    )
                )

        strong_items.sort(key=lambda x: x.accuracy, reverse=True)
        return AreaInsightListResponse(items=strong_items, total=len(strong_items))

    def get_study_consistency(self, user_id: str) -> StudyConsistencyResponse:
        """Calculates active study days, current streak, longest streak, and study time."""
        stmt = (
            select(func.date(Attempt.started_at).label("day"))
            .where(
                Attempt.user_id == user_id,
                Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
            )
            .distinct()
            .order_by(func.date(Attempt.started_at).desc())
        )
        date_rows = list(self.db.scalars(stmt).all())

        if not date_rows:
            return StudyConsistencyResponse(
                active_study_days=0,
                current_streak_days=0,
                longest_streak_days=0,
                total_study_time_seconds=0,
                last_active_date=None,
            )

        # Parse unique sorted dates
        dates = [r if isinstance(r, datetime) else datetime.strptime(str(r), "%Y-%m-%d") for r in date_rows]
        dates_sorted_desc = sorted([d.date() for d in dates], reverse=True)

        active_days = len(dates_sorted_desc)
        last_active_str = str(dates_sorted_desc[0])

        # Streak calculation
        today = datetime.now(timezone.utc).date()
        current_streak = 0
        longest_streak = 0

        # Current streak check
        check_date = today
        if dates_sorted_desc[0] in [today, today - timedelta(days=1)]:
            check_date = dates_sorted_desc[0]
            dates_set = set(dates_sorted_desc)
            while check_date in dates_set:
                current_streak += 1
                check_date -= timedelta(days=1)

        # Longest streak check
        dates_set = set(dates_sorted_desc)
        for d in dates_sorted_desc:
            temp_streak = 0
            curr_d = d
            while curr_d in dates_set:
                temp_streak += 1
                curr_d -= timedelta(days=1)
            if temp_streak > longest_streak:
                longest_streak = temp_streak

        # Total study time
        tot_time_stmt = select(func.sum(Attempt.time_taken_seconds)).where(
            Attempt.user_id == user_id,
            Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
        )
        tot_time = self.db.scalar(tot_time_stmt) or 0

        return StudyConsistencyResponse(
            active_study_days=active_days,
            current_streak_days=current_streak,
            longest_streak_days=longest_streak,
            total_study_time_seconds=tot_time,
            last_active_date=last_active_str,
        )

    def get_compact_dashboard(self, user_id: str) -> CompactDashboardResponse:
        """Returns a lightweight, compact one-shot dashboard summary payload."""
        overview = self.get_overview(user_id=user_id)
        recent = self.get_recent_activity(user_id=user_id, limit=5).items
        weak = self.get_weak_areas(user_id=user_id).items[:3]
        strong = self.get_strong_areas(user_id=user_id).items[:3]
        consistency = self.get_study_consistency(user_id=user_id)

        return CompactDashboardResponse(
            overview=overview,
            recent_activity=recent,
            weak_areas=weak,
            strong_areas=strong,
            consistency=consistency,
        )
