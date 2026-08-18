import json
import os
from typing import List, Optional, Union


from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Gandheevijaya API"
    PROJECT_NAME: str = "GANDHEEVIJAYA"
    APP_ENV: str = "development"  # development | testing | production
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database Configuration: PostgreSQL (psycopg3) or SQLite fallback for local development
    DATABASE_URL: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'gandheevijaya.db')}"

    # JWT Authentication Security
    JWT_SECRET_KEY: str = "super_secret_jwt_signature_key_change_in_production_12345"
    JWT_SECRET: str = "super_secret_jwt_signature_key_change_in_production_12345"  # Alias for backward compatibility
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    RESET_TOKEN_EXPIRE_MINUTES: int = 30

    # Cookie Security Settings
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"
    COOKIE_DOMAIN: Optional[str] = None

    # Password Policy Settings
    PASSWORD_MIN_LENGTH: int = 8

    # CORS Origins (JSON list of strings or comma-separated string)
    ALLOWED_CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # Trusted Hosts
    TRUSTED_HOSTS: Union[str, List[str]] = ["*"]


    @field_validator("PORT", mode="before")
    @classmethod
    def assemble_port(cls, v: Union[str, int]) -> int:
        if isinstance(v, str):
            return int(v)
        return v

    @field_validator("ALLOWED_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            if v.strip().startswith("["):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def assemble_trusted_hosts(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            if v.strip().startswith("["):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @field_validator("JWT_SECRET", mode="before")
    @classmethod
    def sync_jwt_secrets(cls, v: str) -> str:
        return v

    @model_validator(mode="after")
    def validate_production_environment(self) -> "Settings":
        # Keep JWT_SECRET and JWT_SECRET_KEY in sync
        if self.JWT_SECRET_KEY and not self.JWT_SECRET:
            self.JWT_SECRET = self.JWT_SECRET_KEY
        elif self.JWT_SECRET and not self.JWT_SECRET_KEY:
            self.JWT_SECRET_KEY = self.JWT_SECRET

        # Production safety checks
        if self.APP_ENV == "production":
            self.COOKIE_SECURE = True
            insecure_defaults = [
                "super_secret_jwt_signature_key_change_in_production_12345",
                "replace-me",
                "secret",
                "changeme"
            ]
            if self.JWT_SECRET_KEY in insecure_defaults or len(self.JWT_SECRET_KEY) < 16:
                raise ValueError("Insecure JWT_SECRET_KEY detected for production environment. Please provide a strong secret.")
            if "sqlite" in self.DATABASE_URL.lower():
                raise ValueError("Production environment must use a PostgreSQL database URL.")
        return self


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()


