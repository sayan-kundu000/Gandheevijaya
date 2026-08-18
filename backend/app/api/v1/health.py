from fastapi import APIRouter, Response, status

from backend.app.core.config import settings
from backend.app.core.database import check_db_connected
from backend.app.schemas.health import DBHealthResponse, HealthResponse

router = APIRouter(prefix="/health", tags=["Health & Observability"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Application Health Status",
    description="Returns the current operational status, environment, and version of the Gandheevijaya API."
)
def get_health() -> HealthResponse:
    """Check application status and operational metadata."""
    return HealthResponse(
        status="ok",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.APP_ENV
    )


@router.get(
    "/db",
    response_model=DBHealthResponse,
    responses={
        200: {"description": "Database is reachable and responding to queries"},
        503: {"description": "Database connection failed or is unresponsive"}
    },
    summary="Database Connectivity Readiness Check",
    description="Performs an actual ping query against the underlying database engine."
)
def get_db_health(response: Response) -> DBHealthResponse:
    """Readiness probe: validates real database connectivity."""
    is_healthy, error_msg = check_db_connected()
    if not is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return DBHealthResponse(
            status="unhealthy",
            service=settings.PROJECT_NAME,
            database="disconnected",
            version=settings.VERSION,
            error=error_msg
        )

    return DBHealthResponse(
        status="ok",
        service=settings.PROJECT_NAME,
        database="connected",
        version=settings.VERSION,
        error=None
    )
