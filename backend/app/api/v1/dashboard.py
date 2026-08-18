from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, verify_owner_or_admin
from backend.app.models.user import User
from backend.app.schemas.dashboard import (
    AreaInsightListResponse,
    CompactDashboardResponse,
    DashboardOverviewResponse,
    PerformanceTrendListResponse,
    RecentActivityListResponse,
    StudyConsistencyResponse,
    SubjectProgressListResponse,
    TopicProgressListResponse,
)
from backend.app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Student Dashboard & Learning Progress"])


@router.get("", response_model=CompactDashboardResponse)
def get_compact_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves a lightweight, compact one-shot dashboard summary for the current student."""
    service = DashboardService(db)
    return service.get_compact_dashboard(user_id=current_user.id)


@router.get("/overview", response_model=DashboardOverviewResponse)
def get_dashboard_overview(
    exam_id: Optional[int] = Query(None, description="Optional exam scope filter"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves global overview performance metrics for the current student."""
    service = DashboardService(db)
    return service.get_overview(user_id=current_user.id, exam_id=exam_id)


@router.get("/subjects", response_model=SubjectProgressListResponse)
def get_subject_progress(
    exam_id: Optional[int] = Query(None, description="Optional exam scope filter"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves subject-level progress, accuracy, completion rates, and attempt counts."""
    service = DashboardService(db)
    return service.get_subject_progress(user_id=current_user.id, exam_id=exam_id)


@router.get("/topics", response_model=TopicProgressListResponse)
def get_topic_progress(
    subject_id: Optional[int] = Query(None, description="Optional subject scope filter"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves topic-level accuracy, attempted counts, and derived performance status."""
    service = DashboardService(db)
    return service.get_topic_progress(user_id=current_user.id, subject_id=subject_id)


@router.get("/recent-activity", response_model=RecentActivityListResponse)
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50, description="Max recent items to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves recent quiz activity timeline for the current student."""
    service = DashboardService(db)
    return service.get_recent_activity(user_id=current_user.id, limit=limit)


@router.get("/performance-trends", response_model=PerformanceTrendListResponse)
def get_performance_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves daily performance trend time-series metrics."""
    service = DashboardService(db)
    return service.get_performance_trend(user_id=current_user.id, days=days)


@router.get("/weak-areas", response_model=AreaInsightListResponse)
def get_weak_areas(
    threshold: float = Query(60.0, ge=0.0, le=100.0, description="Accuracy threshold below which topics are weak"),
    min_attempts: int = Query(3, ge=1, description="Minimum attempted questions required for classification"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Identifies topics requiring improvement based on accuracy and sample size."""
    service = DashboardService(db)
    return service.get_weak_areas(user_id=current_user.id, threshold=threshold, min_attempts=min_attempts)


@router.get("/strong-areas", response_model=AreaInsightListResponse)
def get_strong_areas(
    threshold: float = Query(80.0, ge=0.0, le=100.0, description="Accuracy threshold above which topics are strong"),
    min_attempts: int = Query(3, ge=1, description="Minimum attempted questions required for classification"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Identifies high-performing topics meeting or exceeding target accuracy."""
    service = DashboardService(db)
    return service.get_strong_areas(user_id=current_user.id, threshold=threshold, min_attempts=min_attempts)


@router.get("/consistency", response_model=StudyConsistencyResponse)
def get_study_consistency(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves active study days, current streak, longest streak, and total study time."""
    service = DashboardService(db)
    return service.get_study_consistency(user_id=current_user.id)
