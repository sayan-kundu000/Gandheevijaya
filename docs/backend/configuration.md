# Gandheevijaya Configuration Guide

Configuration management uses **Pydantic Settings v2** (`pydantic-settings`). Settings are loaded from environment variables or a local `.env` file with strong typing and automated startup validation.

---

## 1. Environment Variables Reference

| Variable | Type | Default | Description |
|---|---|---|---|
| `APP_NAME` | `str` | `"Gandheevijaya API"` | Human-readable application title |
| `PROJECT_NAME` | `str` | `"GANDHEEVIJAYA"` | System project identifier |
| `APP_ENV` | `str` | `"development"` | Runtime environment: `development`, `testing`, or `production` |
| `DEBUG` | `bool` | `True` | Debug flag; enables verbose logging and auto-reload in dev |
| `PORT` | `int` | `8000` | Server listening port (Render provides this via `$PORT`) |
| `HOST` | `str` | `"0.0.0.0"` | Bind address |
| `API_V1_STR` | `str` | `"/api/v1"` | Base prefix for version 1 API endpoints |
| `DATABASE_URL` | `str` | SQLite local path | Database connection URL |
| `JWT_SECRET_KEY` | `str` | Default placeholder | 256-bit secret key for signing JWT tokens |
| `JWT_ALGORITHM` | `str` | `"HS256"` | Algorithm used for JWT encoding/decoding |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | `60` | Lifetime of access tokens |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `int` | `7` | Lifetime of refresh tokens |
| `ALLOWED_CORS_ORIGINS` | `list[str]` | `["http://localhost:5173", ...]` | Allowed frontend origin URLs |

---

## 2. Production Safety Invariants

When `APP_ENV="production"`, the configuration validator enforces:
1. **Strong JWT Secret**: If `JWT_SECRET_KEY` is set to a default placeholder or is shorter than 16 characters, the application refuses to start.
2. **PostgreSQL Required**: If `DATABASE_URL` refers to SQLite, startup raises an immediate configuration error.
