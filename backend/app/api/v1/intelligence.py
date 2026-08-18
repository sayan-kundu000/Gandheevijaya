from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user, get_db, require_admin, verify_owner_or_admin
from backend.app.models.user import User
from backend.app.schemas.intelligence import (
    ContentHealthAnomalyResponse,
    ItemAnalysisListResponse,
    OptionDistractorAnalysisResponse,
    PerformanceDeltaResponse,
    PrescriptiveRecommendationListResponse,
    SpeedAccuracyQuadrantResponse,
    StudentIntelligenceProfileResponse,
    TopicPerformanceMatrixResponse,
)
from backend.app.services.intelligence_service import PerformanceIntelligenceService

router = APIRouter(prefix="/intelligence", tags=["Performance Intelligence & Data Science Analytics"])


@router.get("/student/profile", response_model=StudentIntelligenceProfileResponse)
def get_student_intelligence_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves multidimensional learning intelligence profile for the authenticated student."""
    service = PerformanceIntelligenceService(db)
    return service.get_student_profile(user_id=current_user.id)


@router.get("/student/recommendations", response_model=PrescriptiveRecommendationListResponse)
def get_prescriptive_recommendations(
    limit: int = Query(5, ge=1, le=20, description="Max recommendations to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves prioritized, explainable prescriptive study recommendations for the authenticated student."""
    service = PerformanceIntelligenceService(db)
    return service.get_prescriptive_recommendations(user_id=current_user.id, limit=limit)


@router.get("/student/speed-accuracy", response_model=SpeedAccuracyQuadrantResponse)
def get_speed_accuracy_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves Speed vs Accuracy 4-quadrant analysis across topics for the authenticated student."""
    service = PerformanceIntelligenceService(db)
    return service.get_speed_accuracy_analysis(user_id=current_user.id)


@router.get("/student/performance-delta", response_model=PerformanceDeltaResponse)
def get_performance_delta(
    days: int = Query(7, ge=1, le=90, description="Time window in days for delta comparison"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves comparative performance delta between recent period and prior equivalent period."""
    service = PerformanceIntelligenceService(db)
    return service.get_performance_delta(user_id=current_user.id, days=days)


@router.get("/topics/matrix", response_model=TopicPerformanceMatrixResponse)
def get_topic_performance_matrix(
    subject_id: Optional[int] = Query(None, description="Optional subject filter"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves topic-level performance matrix with health status, coverage, and priority scores."""
    service = PerformanceIntelligenceService(db)
    return service.get_topic_performance_matrix(user_id=current_user.id, subject_id=subject_id)


# ==================== ITEM ANALYSIS & ADMIN CONTENT INTELLIGENCE ====================

@router.get("/questions/item-analysis", response_model=ItemAnalysisListResponse)
def get_question_item_analysis(
    topic_id: Optional[int] = Query(None, description="Optional topic filter"),
    min_attempts: int = Query(5, ge=1, description="Minimum attempted threshold for confidence"),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retrieves statistical empirical difficulty, discrimination index, and quality review flags for questions. Administrator privileges required."""
    service = PerformanceIntelligenceService(db)
    return service.get_question_item_analysis(topic_id=topic_id, min_attempts=min_attempts)


@router.get("/questions/{question_id}/option-analysis", response_model=OptionDistractorAnalysisResponse)
def get_question_option_analysis(
    question_id: str,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Retrieves MCQ option selection frequency and distractor diagnostic report. Administrator privileges required."""
    service = PerformanceIntelligenceService(db)
    return service.get_question_option_analysis(question_id=question_id)


@router.get("/content-health/anomalies", response_model=ContentHealthAnomalyResponse)
def get_content_health_anomalies(
    min_attempts: int = Query(5, ge=1, description="Minimum attempts threshold"),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Scans question bank for statistical anomalies (100% failure, negative discrimination). Administrator privileges required."""
    service = PerformanceIntelligenceService(db)
    return service.get_content_anomalies(min_attempts=min_attempts)
