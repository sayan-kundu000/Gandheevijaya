from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.core.exceptions import NotFoundException, ValidationException
from backend.app.models.attempt import Attempt, AttemptAnswer
from backend.app.models.content import Question, Subject, Topic
from backend.app.models.quiz import Quiz
from backend.app.schemas.intelligence import (
    ContentHealthAnomalyItem,
    ContentHealthAnomalyResponse,
    ItemAnalysisItem,
    ItemAnalysisListResponse,
    OptionDistractorAnalysisResponse,
    OptionFrequencyItem,
    PerformanceDeltaResponse,
    PrescriptiveRecommendationItem,
    PrescriptiveRecommendationListResponse,
    SpeedAccuracyQuadrantResponse,
    SpeedAccuracyTopicItem,
    StudentIntelligenceProfileResponse,
    TopicPerformanceMatrixItem,
    TopicPerformanceMatrixResponse,
)
from backend.app.services.base import BaseService
from backend.app.services.dashboard_service import DashboardService


class PerformanceIntelligenceService(BaseService):
    """
    Data Science & Performance Intelligence Engine for Gandheevijaya.
    Provides multidimensional student profiling, Speed vs Accuracy quadrant analysis,
    time-window performance deltas, empirical item difficulty/discrimination analysis,
    MCQ distractor diagnostics, and explainable prescriptive recommendations.
    """

    def __init__(self, db: Session):
        super().__init__(db)
        self.dashboard_service = DashboardService(db)

    def get_performance_delta(self, user_id: str, days: int = 7) -> PerformanceDeltaResponse:
        """Calculates performance deltas between current period (last N days) and prior equivalent period."""
        now = datetime.now(timezone.utc)
        current_start = now - timedelta(days=days)
        prior_start = now - timedelta(days=2 * days)

        # Current period metrics
        curr_stmt = select(
            func.count(Attempt.id).label("attempts_cnt"),
            func.sum(Attempt.attempted_count).label("q_attempted"),
            func.sum(Attempt.correct_count).label("corr"),
            func.avg(Attempt.score).label("avg_score"),
        ).where(
            Attempt.user_id == user_id,
            Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
            Attempt.started_at >= current_start,
        )
        curr_row = self.db.execute(curr_stmt).one()

        curr_att = curr_row.attempts_cnt or 0
        curr_q = curr_row.q_attempted or 0
        curr_corr = curr_row.corr or 0
        curr_acc = round((curr_corr / curr_q * 100.0), 2) if curr_q > 0 else 0.0
        curr_score = round(float(curr_row.avg_score or 0.0), 2)

        # Prior period metrics
        prior_stmt = select(
            func.count(Attempt.id).label("attempts_cnt"),
            func.sum(Attempt.attempted_count).label("q_attempted"),
            func.sum(Attempt.correct_count).label("corr"),
            func.avg(Attempt.score).label("avg_score"),
        ).where(
            Attempt.user_id == user_id,
            Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
            Attempt.started_at >= prior_start,
            Attempt.started_at < current_start,
        )
        prior_row = self.db.execute(prior_stmt).one()

        prior_att = prior_row.attempts_cnt or 0
        prior_q = prior_row.q_attempted or 0
        prior_corr = prior_row.corr or 0
        prior_acc = round((prior_corr / prior_q * 100.0), 2) if prior_q > 0 else 0.0
        prior_score = round(float(prior_row.avg_score or 0.0), 2)

        acc_delta = round(curr_acc - prior_acc, 2)
        score_delta = round(curr_score - prior_score, 2)
        attempts_delta = curr_att - prior_att

        if curr_q < 3 or prior_q < 3:
            velocity = "INSUFFICIENT_DATA"
        elif acc_delta >= 5.0:
            velocity = "IMPROVING"
        elif acc_delta <= -5.0:
            velocity = "DECLINING"
        else:
            velocity = "STABLE"

        return PerformanceDeltaResponse(
            window_days=days,
            current_period_attempts=curr_att,
            current_period_questions=curr_q,
            current_period_accuracy=curr_acc,
            current_period_avg_score=curr_score,
            prior_period_attempts=prior_att,
            prior_period_questions=prior_q,
            prior_period_accuracy=prior_acc,
            prior_period_avg_score=prior_score,
            accuracy_delta=acc_delta,
            score_delta=score_delta,
            attempts_delta=attempts_delta,
            velocity_status=velocity,
        )

    def get_speed_accuracy_analysis(self, user_id: str) -> SpeedAccuracyQuadrantResponse:
        """Analyzes speed (seconds/question) vs accuracy across topics and maps into 4 quadrants."""
        topic_progress = self.dashboard_service.get_topic_progress(user_id=user_id)

        topic_items: List[SpeedAccuracyTopicItem] = []
        tot_q = 0
        tot_time = 0.0
        tot_corr = 0

        # Benchmark thresholds
        SPEED_BENCHMARK_SEC = 45.0  # target max seconds per question
        ACCURACY_BENCHMARK_PCT = 70.0  # target min accuracy percentage

        for top in topic_progress.items:
            if top.questions_attempted == 0:
                continue

            # Calculate total time spent on this topic from Attempt.time_taken_seconds
            time_stmt = (
                select(
                    func.sum(
                        case(
                            (Attempt.attempted_count > 0, Attempt.time_taken_seconds * (1.0 / Attempt.attempted_count)),
                            else_=0.0,
                        )
                    )
                )
                .select_from(AttemptAnswer)
                .join(AttemptAnswer.attempt)
                .join(AttemptAnswer.question)
                .where(
                    Attempt.user_id == user_id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                    Question.topic_id == top.topic_id,
                )
            )
            top_time = float(self.db.scalar(time_stmt) or 0.0)
            avg_speed = round((top_time / top.questions_attempted), 2) if top.questions_attempted > 0 else 0.0

            acc = top.accuracy
            if acc >= ACCURACY_BENCHMARK_PCT and avg_speed <= SPEED_BENCHMARK_SEC:
                quad = "FAST_ACCURATE"
            elif acc < ACCURACY_BENCHMARK_PCT and avg_speed <= SPEED_BENCHMARK_SEC:
                quad = "FAST_INACCURATE"
            elif acc >= ACCURACY_BENCHMARK_PCT and avg_speed > SPEED_BENCHMARK_SEC:
                quad = "SLOW_ACCURATE"
            else:
                quad = "SLOW_INACCURATE"

            tot_q += top.questions_attempted
            tot_time += top_time
            tot_corr += top.correct_answers

            topic_items.append(
                SpeedAccuracyTopicItem(
                    topic_id=top.topic_id,
                    topic_name=top.topic_name,
                    subject_id=top.subject_id,
                    subject_name=top.subject_name or f"Subject {top.subject_id}",
                    accuracy=acc,
                    questions_attempted=top.questions_attempted,
                    average_time_per_question_seconds=avg_speed,
                    quadrant=quad,
                )
            )

        overall_acc = round((tot_corr / tot_q * 100.0), 2) if tot_q > 0 else 0.0
        overall_speed = round((tot_time / tot_q), 2) if tot_q > 0 else 0.0

        if overall_acc >= ACCURACY_BENCHMARK_PCT and overall_speed <= SPEED_BENCHMARK_SEC:
            overall_quad = "FAST_ACCURATE"
        elif overall_acc < ACCURACY_BENCHMARK_PCT and overall_speed <= SPEED_BENCHMARK_SEC:
            overall_quad = "FAST_INACCURATE"
        elif overall_acc >= ACCURACY_BENCHMARK_PCT and overall_speed > SPEED_BENCHMARK_SEC:
            overall_quad = "SLOW_ACCURATE"
        else:
            overall_quad = "SLOW_INACCURATE"

        return SpeedAccuracyQuadrantResponse(
            overall_quadrant=overall_quad,
            average_speed_seconds_per_question=overall_speed,
            overall_accuracy=overall_acc,
            topics=topic_items,
        )

    def get_student_profile(self, user_id: str) -> StudentIntelligenceProfileResponse:
        """Retrieves a student's multidimensional intelligence profile."""
        overview = self.dashboard_service.get_overview(user_id=user_id)
        consistency = self.dashboard_service.get_study_consistency(user_id=user_id)
        quadrant = self.get_speed_accuracy_analysis(user_id=user_id)
        delta = self.get_performance_delta(user_id=user_id, days=7)

        # Unique coverage calculation
        tot_q_available = self.db.scalar(select(func.count(Question.id))) or 1
        unique_covered = self.db.scalar(
            select(func.count(func.distinct(AttemptAnswer.question_id)))
            .select_from(AttemptAnswer)
            .join(AttemptAnswer.attempt)
            .where(Attempt.user_id == user_id, Attempt.status.in_(["SUBMITTED", "EXPIRED"]))
        ) or 0

        coverage_pct = round((unique_covered / tot_q_available * 100.0), 2)

        return StudentIntelligenceProfileResponse(
            user_id=user_id,
            overall_accuracy=overview.overall_accuracy,
            syllabus_coverage_percentage=coverage_pct,
            total_questions_attempted=overview.questions_attempted,
            unique_questions_covered=unique_covered,
            total_study_time_seconds=overview.total_study_time_seconds,
            active_study_days=consistency.active_study_days,
            current_streak_days=consistency.current_streak_days,
            quadrant_status=quadrant.overall_quadrant,
            delta_7d=delta,
        )

    def get_prescriptive_recommendations(
        self, user_id: str, limit: int = 5
    ) -> PrescriptiveRecommendationListResponse:
        """Computes deterministic topic priority scores and returns human-explainable study recommendations."""
        subject_progress = self.dashboard_service.get_subject_progress(user_id=user_id)
        topic_progress = self.dashboard_service.get_topic_progress(user_id=user_id)
        delta = self.get_performance_delta(user_id=user_id, days=7)

        recommendations: List[PrescriptiveRecommendationItem] = []

        for top in topic_progress.items:
            # Topic coverage estimation
            tot_t_q = self.db.scalar(select(func.count(Question.id)).where(Question.topic_id == top.topic_id)) or 1
            unique_t_q = self.db.scalar(
                select(func.count(func.distinct(AttemptAnswer.question_id)))
                .select_from(AttemptAnswer)
                .join(AttemptAnswer.attempt)
                .join(AttemptAnswer.question)
                .where(
                    Attempt.user_id == user_id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                    Question.topic_id == top.topic_id,
                )
            ) or 0

            coverage_pct = round((unique_t_q / tot_t_q * 100.0), 2)

            # Priority math: 0.5 * (100 - acc) + 0.3 * (100 - coverage) + 0.2 * (decline_penalty)
            acc_gap = 100.0 - top.accuracy
            cov_gap = 100.0 - coverage_pct
            decline_penalty = max(0.0, -delta.accuracy_delta) if top.questions_attempted >= 3 else 0.0

            priority_score = round((0.5 * acc_gap + 0.3 * cov_gap + 0.2 * decline_penalty), 2)

            if top.questions_attempted == 0:
                action = "EXPAND_SYLLABUS_COVERAGE"
                reason = f"Topic '{top.topic_name}' has not been started yet (0% coverage). Begin practicing initial questions."
            elif top.accuracy < 60.0 and top.questions_attempted >= 3:
                action = "PRACTICE_WEAK_TOPIC"
                reason = f"Recommended because your accuracy in '{top.topic_name}' is {top.accuracy}% across {top.questions_attempted} questions, representing a high-priority weak area."
            elif delta.velocity_status == "DECLINING" and top.questions_attempted >= 3:
                action = "REVISE_DECLINING_CONCEPT"
                reason = f"Recent accuracy decline of {abs(delta.accuracy_delta)}% detected across study sessions. Revisit fundamental concepts in '{top.topic_name}'."
            else:
                action = "PRACTICE_WEAK_TOPIC"
                reason = f"Targeted practice in '{top.topic_name}' (Accuracy: {top.accuracy}%, Coverage: {coverage_pct}%) will improve overall exam readiness."

            recommendations.append(
                PrescriptiveRecommendationItem(
                    priority_rank=0,  # assigned after sorting
                    topic_id=top.topic_id,
                    topic_name=top.topic_name,
                    subject_id=top.subject_id,
                    subject_name=top.subject_name or f"Subject {top.subject_id}",
                    priority_score=priority_score,
                    accuracy=top.accuracy,
                    questions_attempted=top.questions_attempted,
                    coverage_percentage=coverage_pct,
                    recommended_action=action,
                    explanation_reason=reason,
                )
            )

        recommendations.sort(key=lambda x: x.priority_score, reverse=True)

        items: List[PrescriptiveRecommendationItem] = []
        for idx, rec in enumerate(recommendations[:limit], start=1):
            items.append(
                PrescriptiveRecommendationItem(
                    priority_rank=idx,
                    topic_id=rec.topic_id,
                    topic_name=rec.topic_name,
                    subject_id=rec.subject_id,
                    subject_name=rec.subject_name,
                    priority_score=rec.priority_score,
                    accuracy=rec.accuracy,
                    questions_attempted=rec.questions_attempted,
                    coverage_percentage=rec.coverage_percentage,
                    recommended_action=rec.recommended_action,
                    explanation_reason=rec.explanation_reason,
                )
            )

        return PrescriptiveRecommendationListResponse(items=items, total=len(items))

    def get_topic_performance_matrix(
        self, user_id: str, subject_id: Optional[int] = None
    ) -> TopicPerformanceMatrixResponse:
        """Retrieves topic-level performance matrix with health status, coverage, and priority scores."""
        topic_progress = self.dashboard_service.get_topic_progress(user_id=user_id, subject_id=subject_id)
        delta = self.get_performance_delta(user_id=user_id, days=7)
        speed_analysis = self.get_speed_accuracy_analysis(user_id=user_id)

        speed_map = {t.topic_id: t for t in speed_analysis.topics}
        items: List[TopicPerformanceMatrixItem] = []

        for top in topic_progress.items:
            tot_t_q = self.db.scalar(select(func.count(Question.id)).where(Question.topic_id == top.topic_id)) or 1
            unique_t_q = self.db.scalar(
                select(func.count(func.distinct(AttemptAnswer.question_id)))
                .select_from(AttemptAnswer)
                .join(AttemptAnswer.attempt)
                .join(AttemptAnswer.question)
                .where(
                    Attempt.user_id == user_id,
                    Attempt.status.in_(["SUBMITTED", "EXPIRED"]),
                    Question.topic_id == top.topic_id,
                )
            ) or 0

            cov_pct = round((unique_t_q / tot_t_q * 100.0), 2)
            sp_item = speed_map.get(top.topic_id)
            avg_speed = sp_item.average_time_per_question_seconds if sp_item else 0.0
            quad = sp_item.quadrant if sp_item else "SLOW_INACCURATE"

            if top.questions_attempted == 0:
                health = "NOT_STARTED"
            elif top.questions_attempted < 3:
                health = "INSUFFICIENT_DATA"
            elif top.accuracy >= 80.0:
                health = "STRONG"
            elif top.accuracy >= 65.0:
                health = "STABLE"
            elif delta.velocity_status == "DECLINING":
                health = "DECLINING"
            elif delta.velocity_status == "IMPROVING":
                health = "IMPROVING"
            else:
                health = "WEAK"

            priority = round(0.5 * (100.0 - top.accuracy) + 0.3 * (100.0 - cov_pct), 2)

            items.append(
                TopicPerformanceMatrixItem(
                    topic_id=top.topic_id,
                    topic_name=top.topic_name,
                    subject_id=top.subject_id,
                    subject_name=top.subject_name or f"Subject {top.subject_id}",
                    questions_attempted=top.questions_attempted,
                    correct_answers=top.correct_answers,
                    accuracy=top.accuracy,
                    unique_coverage_percentage=cov_pct,
                    average_time_per_question_seconds=avg_speed,
                    quadrant=quad,
                    health_status=health,
                    priority_score=priority,
                )
            )

        items.sort(key=lambda x: x.priority_score, reverse=True)
        return TopicPerformanceMatrixResponse(items=items, total=len(items))

    # ==================== ITEM ANALYSIS & DISTRACTOR DIAGNOSTICS ====================

    def get_question_item_analysis(
        self, topic_id: Optional[int] = None, min_attempts: int = 5
    ) -> ItemAnalysisListResponse:
        """Calculates statistical empirical difficulty, discrimination index, and review flags for questions."""
        q_stmt = select(Question).options(joinedload(Question.topic))
        if topic_id:
            q_stmt = q_stmt.where(Question.topic_id == topic_id)
        questions = list(self.db.scalars(q_stmt).all())

        items: List[ItemAnalysisItem] = []

        for q in questions:
            ans_stmt = (
                select(
                    func.count(AttemptAnswer.id).label("total_att"),
                    func.sum(case((AttemptAnswer.is_correct == True, 1), else_=0)).label("corr"),
                    func.sum(case((AttemptAnswer.is_correct == False, 1), else_=0)).label("incorr"),
                    func.avg(
                        case(
                            (Attempt.attempted_count > 0, Attempt.time_taken_seconds * (1.0 / Attempt.attempted_count)),
                            else_=0.0,
                        )
                    ).label("avg_time"),
                )
                .select_from(AttemptAnswer)
                .join(AttemptAnswer.attempt)
                .where(AttemptAnswer.question_id == q.id)
            )

            ans_row = self.db.execute(ans_stmt).one()
            tot_att = ans_row.total_att or 0
            corr = ans_row.corr or 0
            incorr = ans_row.incorr or 0
            avg_t = round(float(ans_row.avg_time or 0.0), 2)

            success_rate = round((corr / tot_att * 100.0), 2) if tot_att > 0 else 0.0
            emp_diff = round(1.0 - (corr / tot_att), 2) if tot_att > 0 else 1.0

            if tot_att < min_attempts:
                diff_class = "INSUFFICIENT_DATA"
                disc_index = 0.0
                flag = False
                reason = None
            else:
                if success_rate >= 80.0:
                    diff_class = "EASY"
                elif success_rate >= 50.0:
                    diff_class = "MODERATE"
                elif success_rate >= 25.0:
                    diff_class = "HARD"
                else:
                    diff_class = "VERY_HARD"

                # Estimate discrimination index (top 27% vs bottom 27% score groups)
                attempts_scores = list(
                    self.db.execute(
                        select(AttemptAnswer.is_correct, Attempt.percentage)
                        .select_from(AttemptAnswer)
                        .join(AttemptAnswer.attempt)
                        .where(AttemptAnswer.question_id == q.id, Attempt.status.in_(["SUBMITTED", "EXPIRED"]))
                        .order_by(Attempt.percentage.desc())
                    ).all()
                )

                if len(attempts_scores) >= 4:
                    cut = max(1, int(len(attempts_scores) * 0.27))
                    top_group = attempts_scores[:cut]
                    bottom_group = attempts_scores[-cut:]

                    top_succ = sum(1 for a in top_group if a.is_correct) / len(top_group)
                    bot_succ = sum(1 for a in bottom_group if a.is_correct) / len(bottom_group)
                    disc_index = round(top_succ - bot_succ, 2)
                else:
                    disc_index = 0.0

                flag = False
                reason = None

                if disc_index < -0.1:
                    flag = True
                    reason = f"Negative discrimination index ({disc_index}): Weaker students answer this question correctly more often than top-performing students."
                elif success_rate == 0.0 and tot_att >= min_attempts:
                    flag = True
                    reason = f"100% failure rate across {tot_att} student attempts. Review answer key accuracy or option formatting."

            items.append(
                ItemAnalysisItem(
                    question_id=q.id,
                    topic_id=q.topic_id,
                    topic_name=q.topic.name if q.topic else f"Topic {q.topic_id}",
                    question_type=q.type,
                    difficulty_author=q.difficulty,
                    total_attempts=tot_att,
                    correct_attempts=corr,
                    incorrect_attempts=incorr,
                    empirical_success_rate=success_rate,
                    empirical_difficulty=emp_diff,
                    difficulty_classification=diff_class,
                    discrimination_index=disc_index,
                    average_time_seconds=avg_t,
                    review_flag=flag,
                    review_reason=reason,
                )
            )

        return ItemAnalysisListResponse(items=items, total=len(items))

    def get_question_option_analysis(self, question_id: str) -> OptionDistractorAnalysisResponse:
        """Performs MCQ option selection distribution and distractor diagnostic analysis."""
        q = self.db.get(Question, question_id)
        if not q:
            raise NotFoundException(f"Question {question_id} not found")

        answers = list(
            self.db.scalars(
                select(AttemptAnswer).where(AttemptAnswer.question_id == question_id)
            ).all()
        )

        tot_resp = len(answers)
        freq_map: Dict[str, int] = {}
        for ans in answers:
            sel = ans.selected_answer or "UNANSWERED"
            freq_map[sel] = freq_map.get(sel, 0) + 1

        options_data: List[OptionFrequencyItem] = []

        if isinstance(q.options, dict):
            opts_dict = q.options
        elif isinstance(q.options, list):
            opts_dict = {str(idx): str(val) for idx, val in enumerate(q.options)}
        else:
            opts_dict = {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}

        for opt_key, opt_text in opts_dict.items():
            cnt = freq_map.get(opt_key, 0)
            pct = round((cnt / tot_resp * 100.0), 2) if tot_resp > 0 else 0.0
            is_corr = str(opt_key).strip().upper() == str(q.correct_answer).strip().upper()

            if is_corr:
                diag = "CORRECT_ANSWER"
            elif cnt == 0 and tot_resp >= 5:
                diag = "UNUSED"
            elif pct < 5.0 and tot_resp >= 5:
                diag = "WEAK_DISTRACTOR"
            elif pct > 35.0:
                diag = "MISCONCEPTION_MAGNET"
            else:
                diag = "NORMAL"

            options_data.append(
                OptionFrequencyItem(
                    option_key=opt_key,
                    option_text=opt_text,
                    is_correct=is_corr,
                    selection_count=cnt,
                    selection_percentage=pct,
                    distractor_diagnostic=diag,
                )
            )

        summary = f"Total responses: {tot_resp}. Options evaluated: {len(options_data)}."
        return OptionDistractorAnalysisResponse(
            question_id=q.id,
            question_text=q.question_text,
            question_type=q.type,
            correct_answer=q.correct_answer,
            total_responses=tot_resp,
            options=options_data,
            diagnostic_summary=summary,
        )

    def get_content_anomalies(self, min_attempts: int = 5) -> ContentHealthAnomalyResponse:
        """Scans question bank for items exhibiting statistical anomalies (0% success, negative discrimination, etc.)."""
        item_analysis = self.get_question_item_analysis(min_attempts=min_attempts)
        anomalies: List[ContentHealthAnomalyItem] = []

        for item in item_analysis.items:
            if item.review_flag and item.review_reason:
                anomaly_type = (
                    "ZERO_PERCENT_SUCCESS" if item.empirical_success_rate == 0.0 else "NEGATIVE_DISCRIMINATION"
                )
                severity = "ERROR" if item.empirical_success_rate == 0.0 else "WARNING"

                anomalies.append(
                    ContentHealthAnomalyItem(
                        question_id=item.question_id,
                        topic_id=item.topic_id,
                        topic_name=item.topic_name,
                        anomaly_type=anomaly_type,
                        severity=severity,
                        attempts_count=item.total_attempts,
                        success_rate=item.empirical_success_rate,
                        details=item.review_reason,
                    )
                )

        return ContentHealthAnomalyResponse(items=anomalies, total=len(anomalies))
