from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class SubjectPerformanceItem(BaseModel):
    subject_id: int
    subject_name: str
    total_quizzes_taken: int
    average_score: float
    completion_rate: float
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class TopicPerformanceItem(BaseModel):
    topic_id: int
    topic_name: str
    total_questions_attempted: int
    correct_attempts: int
    accuracy_percentage: float
    average_time_per_question: float
    weakness_score: float
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPerformanceSummary(BaseModel):
    user_id: str
    user_name: Optional[str] = None
    overall_accuracy: float
    total_quizzes_completed: int
    total_questions_attempted: int
    subject_performance: List[SubjectPerformanceItem] = []
    weak_topics: List[TopicPerformanceItem] = []
    score_trend: List[float] = []


class LeaderboardEntryResponse(BaseModel):
    rank: int
    user_id: str
    user_name: str
    quizzes_taken: int
    average_score: float
    total_score: float


class AdminStatsResponse(BaseModel):
    total_users: int
    total_students: int
    total_admins: int
    total_exams: int
    total_subjects: int
    total_topics: int
    total_questions: int
    total_quizzes: int
    total_attempts: int
