from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.api.router import api_router
from backend.app.core.config import settings
from backend.app.core.exceptions import AppException
from backend.app.core.logging import request_id_ctx_var, setup_logging
from backend.app.core.middleware import RequestCorrelationMiddleware, SecurityHeadersMiddleware
from backend.app.schemas.health import LivenessResponse

# Initialize structured logging
logger = setup_logging(
    log_level="DEBUG" if settings.DEBUG else "INFO",
    is_production=settings.APP_ENV == "production"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management for startup and graceful shutdown."""
    logger.info(f"Starting {settings.APP_NAME} in [{settings.APP_ENV}] mode (v{settings.VERSION})")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    description="Gandheevijaya Multi-Exam Assessment Platform Backend REST APIs",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 1. Register Request Correlation & Timing Middleware
app.add_middleware(RequestCorrelationMiddleware)

# 2. Register Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# 3. Register CORS Middleware
if settings.ALLOWED_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )



# -----------------------------------------------------------------------------
# Global Exception Handlers
# -----------------------------------------------------------------------------

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handles domain-level application exceptions."""
    request_id = request_id_ctx_var.get()
    logger.warning(f"Domain exception [{exc.code}] on {request.method} {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic request schema validation failures."""
    request_id = request_id_ctx_var.get()
    encoded_errors = jsonable_encoder(exc.errors())
    logger.info(f"Validation error on {request.method} {request.url.path}: {encoded_errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed. Please check your request parameters.",
                "details": encoded_errors,
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles standard HTTPExceptions."""
    request_id = request_id_ctx_var.get()
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
                "details": None,
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handles database unique constraint and foreign key violations safely."""
    request_id = request_id_ctx_var.get()
    logger.error(f"Database integrity error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": {
                "code": "RESOURCE_CONFLICT",
                "message": "A database integrity conflict occurred (e.g. duplicate key or foreign key violation).",
                "details": None if settings.APP_ENV == "production" else str(exc.orig),
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handles generic database exceptions without leaking query details."""
    request_id = request_id_ctx_var.get()
    logger.error(f"SQLAlchemy error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database operation failed.",
                "details": None if settings.APP_ENV == "production" else str(exc),
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all handler for unhandled exceptions."""
    request_id = request_id_ctx_var.get()
    logger.critical(f"Unhandled server error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal server error occurred.",
                "details": None if settings.APP_ENV == "production" else str(exc),
                "request_id": request_id,
            }
        },
    )


# -----------------------------------------------------------------------------
# Base Endpoints & Routers
# -----------------------------------------------------------------------------

@app.get("/health", response_model=LivenessResponse, tags=["Health & Observability"])
def root_liveness_check() -> LivenessResponse:
    """Root liveness probe to verify FastAPI process is running."""
    return LivenessResponse(status="ok", app=settings.PROJECT_NAME)


# Mount versioned API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG and settings.APP_ENV == "development"
    )
