"""
Authentication API router backward-compatibility shim.
Re-exports router from backend.app.api.v1.auth.
"""
from backend.app.api.v1.auth import router

__all__ = ["router"]
