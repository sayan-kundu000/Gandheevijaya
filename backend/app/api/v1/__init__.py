from fastapi import APIRouter

from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.analytics import router as analytics_router
from backend.app.api.v1.attempts import router as attempts_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.dashboard import router as dashboard_router
from backend.app.api.v1.exams import router as exams_router
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.intelligence import router as intelligence_router
from backend.app.api.v1.leaderboard import router as leaderboard_router
from backend.app.api.v1.materials import router as materials_router
from backend.app.api.v1.questions import router as questions_router
from backend.app.api.v1.quizzes import router as quizzes_router
from backend.app.api.v1.results import router as results_router
from backend.app.api.v1.subjects import router as subjects_router
from backend.app.api.v1.topics import router as topics_router
from backend.app.api.v1.users import router as users_router

v1_router = APIRouter()

# Register v1 domain sub-routers under /api/v1
v1_router.include_router(health_router)
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(exams_router)
v1_router.include_router(subjects_router)
v1_router.include_router(topics_router)
v1_router.include_router(questions_router)
v1_router.include_router(quizzes_router)
v1_router.include_router(attempts_router)
v1_router.include_router(results_router)
v1_router.include_router(dashboard_router)
v1_router.include_router(intelligence_router)
v1_router.include_router(materials_router)
v1_router.include_router(analytics_router)
v1_router.include_router(leaderboard_router)
v1_router.include_router(admin_router)

__all__ = ["v1_router"]
