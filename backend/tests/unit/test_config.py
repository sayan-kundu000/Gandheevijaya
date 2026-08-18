import pytest

from backend.app.core.config import Settings


def test_default_settings():
    settings = Settings()
    assert settings.PROJECT_NAME == "GANDHEEVIJAYA"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PORT == 8000
    assert isinstance(settings.ALLOWED_CORS_ORIGINS, list)


def test_cors_origins_parsing():
    settings = Settings(ALLOWED_CORS_ORIGINS="http://localhost:5173, http://example.com")
    assert "http://localhost:5173" in settings.ALLOWED_CORS_ORIGINS
    assert "http://example.com" in settings.ALLOWED_CORS_ORIGINS


def test_cors_origins_json_parsing():
    settings = Settings(ALLOWED_CORS_ORIGINS='["http://localhost:5173", "https://app.vercel.app"]')
    assert "http://localhost:5173" in settings.ALLOWED_CORS_ORIGINS
    assert "https://app.vercel.app" in settings.ALLOWED_CORS_ORIGINS


def test_production_safety_validation():
    # Should fail if production uses insecure default JWT secret
    with pytest.raises(ValueError, match="Insecure JWT_SECRET_KEY"):
        Settings(
            APP_ENV="production",
            JWT_SECRET_KEY="replace-me",
            DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/db"
        )

    # Should fail if production uses SQLite
    with pytest.raises(ValueError, match="PostgreSQL database URL"):
        Settings(
            APP_ENV="production",
            JWT_SECRET_KEY="very_long_secure_production_secret_key_123456",
            DATABASE_URL="sqlite:///./gandheevijaya.db"
        )
