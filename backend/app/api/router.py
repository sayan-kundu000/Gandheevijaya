from fastapi import APIRouter

from backend.app.api.v1 import v1_router

api_router = APIRouter()

# Register API v1
api_router.include_router(v1_router)

__all__ = ["api_router"]
