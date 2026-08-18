# Gandheevijaya FastAPI Backend

The core REST API server and backend foundation for the Gandheevijaya Assessment Platform.

## Features
- **Framework**: FastAPI (Python 3.12+)
- **Database ORM**: SQLAlchemy 2.x with `psycopg3` driver & connection pooling
- **Migrations**: Alembic (`alembic upgrade head`)
- **Settings**: Strongly-typed `pydantic-settings` with startup validation
- **Observability**: Request correlation ID tracking (`X-Request-ID`), access latency logging, and health/readiness endpoints (`/health`, `/api/v1/health`, `/api/v1/health/db`)
- **Architecture**: Clean modular monolith layers (Routers -> Services -> Repositories -> Models)

## Run Locally
```bash
py -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run Tests
```bash
py -m pytest backend/tests
```
