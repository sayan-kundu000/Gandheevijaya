from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DashboardOverviewResponse(BaseModel):
    total_attempts: int = Field(default=0, description="Total quiz attempts started")
    completed_attempts: int = Field(default=0, description="Total completed or submitted attempts")
    active_attempts: int = Field(default=0, description="Attempts currently IN_PROGRESS")
    questions_attempted: int = Field(default=0, description="Total questions answered")
    correct_answers: int = Field(default=0, description="Total questions answered correctly")
    incorrect_answers: int = Field(default=0, description="Total questions answered incorrectly")
    unanswered_questions: int = Field(default=0, description="Total questions left unanswered")
    overall_accuracy: float = Field(default=0.0, description="Overall accuracy percentage (correct / attempted * 100)")
    average_percentage: float = Field(default=0.0, description="Average percentage score across completed quizzes")
    total_study_time_seconds: int = Field(default=0, description="Total study time spent in seconds")
    recent_activity_count: int = Field(default=0, description="Total activity events in last 30 days")


class SubjectProgressItem(BaseModel):
    subject_id: int
    subject_name: str
    exam_id: Optional[int] = None
    questions_attempted: int = Field(default=0)
    correct_answers: int = Field(default=0)
    incorrect_answers: int = Field(default=0)
    accuracy: float = Field(default=0.0)
    average_score: float = Field(default=0.0)
    unique_questions_covered: int = Field(default=0)
    total_available_questions: int = Field(default=0)
    completion_rate: float = Field(default=0.0, description="Unique questions covered / total available questions * 100")
    attempt_count: int = Field(default=0)
    last_activity: Optional[datetime] = None


class SubjectProgressListResponse(BaseModel):
    items: List[SubjectProgressItem]
    total: int


class TopicProgressItem(BaseModel):
    topic_id: int
    topic_name: str
    subject_id: int
    subject_name: Optional[str] = None
    questions_attempted: int = Field(default=0)
    correct_answers: int = Field(default=0)
    incorrect_answers: int = Field(default=0)
    accuracy: float = Field(default=0.0)
    attempt_count: int = Field(default=0)
    performance_status: str = Field(default="NOT_STARTED", description="NOT_STARTED, PRACTICING, WEAK, STRONG")
    last_activity: Optional[datetime] = None


class TopicProgressListResponse(BaseModel):
    items: List[TopicProgressItem]
    total: int


class RecentActivityItem(BaseModel):
    attempt_id: str
    quiz_id: int
    quiz_title: str
    subject_name: Optional[str] = None
    status: str
    score: float
    total_marks: float
    percentage: float
    accuracy: float
    completed_at: Optional[datetime] = None
    started_at: datetime


class RecentActivityListResponse(BaseModel):
    items: List[RecentActivityItem]
    total: int


class PerformanceTrendItem(BaseModel):
    date: str = Field(description="Format: YYYY-MM-DD")
    attempts_count: int = Field(default=0)
    questions_attempted: int = Field(default=0)
    accuracy: float = Field(default=0.0)
    average_percentage: float = Field(default=0.0)
    study_time_seconds: int = Field(default=0)


class PerformanceTrendListResponse(BaseModel):
    items: List[PerformanceTrendItem]


class AreaInsightItem(BaseModel):
    topic_id: int
    topic_name: str
    subject_id: int
    subject_name: str
    accuracy: float
    questions_attempted: int
    incorrect_answers: int
    recommendation_reason: str


class AreaInsightListResponse(BaseModel):
    items: List[AreaInsightItem]
    total: int


class StudyConsistencyResponse(BaseModel):
    active_study_days: int = Field(default=0)
    current_streak_days: int = Field(default=0)
    longest_streak_days: int = Field(default=0)
    total_study_time_seconds: int = Field(default=0)
    last_active_date: Optional[str] = None


class CompactDashboardResponse(BaseModel):
    overview: DashboardOverviewResponse
    recent_activity: List[RecentActivityItem]
    weak_areas: List[AreaInsightItem]
    strong_areas: List[AreaInsightItem]
    consistency: StudyConsistencyResponse
