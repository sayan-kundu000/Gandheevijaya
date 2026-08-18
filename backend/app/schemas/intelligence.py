from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SpeedAccuracyTopicItem(BaseModel):
    topic_id: int
    topic_name: str
    subject_id: int
    subject_name: str
    accuracy: float = Field(default=0.0)
    questions_attempted: int = Field(default=0)
    average_time_per_question_seconds: float = Field(default=0.0)
    quadrant: str = Field(
        default="SLOW_INACCURATE",
        description="FAST_ACCURATE, FAST_INACCURATE, SLOW_ACCURATE, SLOW_INACCURATE",
    )


class SpeedAccuracyQuadrantResponse(BaseModel):
    overall_quadrant: str = Field(description="FAST_ACCURATE, FAST_INACCURATE, SLOW_ACCURATE, SLOW_INACCURATE")
    average_speed_seconds_per_question: float = Field(default=0.0)
    overall_accuracy: float = Field(default=0.0)
    topics: List[SpeedAccuracyTopicItem] = []


class PerformanceDeltaResponse(BaseModel):
    window_days: int = Field(default=7)
    current_period_attempts: int = Field(default=0)
    current_period_questions: int = Field(default=0)
    current_period_accuracy: float = Field(default=0.0)
    current_period_avg_score: float = Field(default=0.0)
    prior_period_attempts: int = Field(default=0)
    prior_period_questions: int = Field(default=0)
    prior_period_accuracy: float = Field(default=0.0)
    prior_period_avg_score: float = Field(default=0.0)
    accuracy_delta: float = Field(default=0.0, description="current_accuracy - prior_accuracy")
    score_delta: float = Field(default=0.0, description="current_avg_score - prior_avg_score")
    attempts_delta: int = Field(default=0)
    velocity_status: str = Field(default="INSUFFICIENT_DATA", description="IMPROVING, STABLE, DECLINING, INSUFFICIENT_DATA")


class StudentIntelligenceProfileResponse(BaseModel):
    user_id: str
    overall_accuracy: float = Field(default=0.0)
    syllabus_coverage_percentage: float = Field(default=0.0)
    total_questions_attempted: int = Field(default=0)
    unique_questions_covered: int = Field(default=0)
    total_study_time_seconds: int = Field(default=0)
    active_study_days: int = Field(default=0)
    current_streak_days: int = Field(default=0)
    quadrant_status: str = Field(default="SLOW_INACCURATE")
    delta_7d: PerformanceDeltaResponse


class PrescriptiveRecommendationItem(BaseModel):
    priority_rank: int
    topic_id: int
    topic_name: str
    subject_id: int
    subject_name: str
    exam_id: Optional[int] = None
    priority_score: float
    accuracy: float
    questions_attempted: int
    coverage_percentage: float
    recommended_action: str = Field(description="PRACTICE_WEAK_TOPIC, EXPAND_SYLLABUS_COVERAGE, REVISE_DECLINING_CONCEPT")
    explanation_reason: str = Field(description="Human-explainable rationale string")


class PrescriptiveRecommendationListResponse(BaseModel):
    items: List[PrescriptiveRecommendationItem]
    total: int


class ItemAnalysisItem(BaseModel):
    question_id: str
    topic_id: int
    topic_name: str
    question_type: str
    difficulty_author: str
    total_attempts: int = Field(default=0)
    correct_attempts: int = Field(default=0)
    incorrect_attempts: int = Field(default=0)
    empirical_success_rate: float = Field(default=0.0)
    empirical_difficulty: float = Field(default=0.0, description="1.0 - success_rate")
    difficulty_classification: str = Field(default="INSUFFICIENT_DATA", description="INSUFFICIENT_DATA, EASY, MODERATE, HARD, VERY_HARD")
    discrimination_index: float = Field(default=0.0, description="Estimated point-biserial / top vs bottom 27% difference")
    average_time_seconds: float = Field(default=0.0)
    review_flag: bool = Field(default=False, description="Flagged for review if negative discrimination or 100% failure")
    review_reason: Optional[str] = None


class ItemAnalysisListResponse(BaseModel):
    items: List[ItemAnalysisItem]
    total: int


class OptionFrequencyItem(BaseModel):
    option_key: str
    option_text: Optional[str] = None
    is_correct: bool = False
    selection_count: int = Field(default=0)
    selection_percentage: float = Field(default=0.0)
    distractor_diagnostic: str = Field(default="NORMAL", description="CORRECT_ANSWER, WEAK_DISTRACTOR, MISCONCEPTION_MAGNET, UNUSED")


class OptionDistractorAnalysisResponse(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    correct_answer: str
    total_responses: int = Field(default=0)
    options: List[OptionFrequencyItem] = []
    diagnostic_summary: str


class TopicPerformanceMatrixItem(BaseModel):
    topic_id: int
    topic_name: str
    subject_id: int
    subject_name: str
    questions_attempted: int = Field(default=0)
    correct_answers: int = Field(default=0)
    accuracy: float = Field(default=0.0)
    unique_coverage_percentage: float = Field(default=0.0)
    average_time_per_question_seconds: float = Field(default=0.0)
    quadrant: str = Field(default="SLOW_INACCURATE")
    health_status: str = Field(default="NOT_STARTED", description="STRONG, STABLE, WEAK, DECLINING, IMPROVING, NOT_STARTED, INSUFFICIENT_DATA")
    priority_score: float = Field(default=0.0)


class TopicPerformanceMatrixResponse(BaseModel):
    items: List[TopicPerformanceMatrixItem]
    total: int


class ContentHealthAnomalyItem(BaseModel):
    question_id: str
    topic_id: int
    topic_name: str
    anomaly_type: str = Field(description="ZERO_PERCENT_SUCCESS, HUNDRED_PERCENT_SUCCESS, NEGATIVE_DISCRIMINATION, HIGH_TIME_OUTLIER")
    severity: str = Field(description="WARNING, ERROR")
    attempts_count: int
    success_rate: float
    details: str


class ContentHealthAnomalyResponse(BaseModel):
    items: List[ContentHealthAnomalyItem]
    total: int
