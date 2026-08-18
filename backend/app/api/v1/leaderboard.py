from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.schemas.analytics import LeaderboardEntryResponse
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=List[LeaderboardEntryResponse])
def get_leaderboard(
    limit: int = Query(50, ge=1, le=100, description="Top N rankings to return"),
    db: Session = Depends(get_db),
):
    """Retrieve top performing student rankings based on assessment scores."""
    service = AnalyticsService(db)
    return service.get_leaderboard(limit=limit)
