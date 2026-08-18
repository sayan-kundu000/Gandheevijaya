# Gandheevijaya Backend Architecture

## 1. System Overview

Gandheevijaya is architected as a **modular monolith** using **FastAPI**, **SQLAlchemy 2.x**, and **PostgreSQL** (with psycopg 3). The design prioritizes maintainability, explicit contracts, transparent transaction boundaries, and ease of deployment to platforms like Render.

```text
React / TypeScript Frontend (Vercel)
                 ↓ (REST / JSON + X-Request-ID)
FastAPI Backend (Render)
                 ↓ (Lifespan + Middlewares)
API Routers (api/v1/*)
                 ↓ (Dependency Injection: get_db, get_current_user)
Service Layer (Business rules & Transaction Boundaries)
                 ↓
Repository / Data Access Layer (SQLAlchemy 2.x Queries)
                 ↓
SQLAlchemy 2.x ORM / Connection Pool
                 ↓
PostgreSQL Database (psycopg3)
```

---

## 2. Directory Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Application entrypoint, lifespan, middlewares, exception handlers
│   │
│   ├── core/                        # Infrastructure and global singletons
│   │   ├── config.py                # Strongly typed Pydantic Settings & environment validation
│   │   ├── database.py              # SQLAlchemy engine, session maker, get_db generator, health ping
│   │   ├── security.py              # Argon2 password hashing, JWT creation & decoding
│   │   ├── logging.py               # Structured logging & Request ID ContextVar filter
│   │   ├── exceptions.py            # Centralized domain exception hierarchy
│   │   └── middleware.py            # X-Request-ID and access timing middleware
│   │
│   ├── api/                         # HTTP layer
│   │   ├── deps.py                  # FastAPI dependency injection (current_user, current_admin, get_db)
│   │   ├── router.py                # Central router aggregator
│   │   └── v1/                      # Version 1 API routers
│   │       ├── __init__.py          # V1 sub-router
│   │       ├── health.py            # Liveness, app health, and DB ping readiness probes
│   │       └── auth.py              # Authentication endpoints (login, register, refresh, logout)
│   │
│   ├── models/                      # SQLAlchemy 2.x ORM Declarative Models
│   │   ├── user.py                  # User and authentication entities
│   │   ├── content.py               # ExamCategory, Exam, Subject, Topic, Subtopic, Question
│   │   ├── quiz.py                  # Quiz and QuizQuestion association
│   │   ├── attempt.py               # Attempt and AttemptAnswer submissions
│   │   ├── material.py              # StudyMaterial content
│   │   ├── performance.py           # Subject/Topic performance tracking & snapshots
│   │   └── import_audit.py          # Content import logs and errors
│   │
│   ├── schemas/                     # Pydantic v2 API Boundary Contracts
│   │   ├── common.py                # ErrorResponse, PaginationParams, PaginatedResponse
│   │   ├── health.py                # Health & readiness probe response schemas
│   │   └── user.py                  # User request/response schemas & tokens
│   │
│   ├── repositories/                # Data access layer
│   │   ├── base.py                  # Generic BaseRepository with SQLAlchemy 2.x CRUD methods
│   │   └── ...
│   │
│   ├── services/                    # Business logic and transaction management
│   │   ├── base.py                  # Generic BaseService with execute_in_transaction
│   │   └── ...
│   │
│   └── utils/                       # Shared utility helpers
│
├── tests/                           # Pytest test suite
│   ├── conftest.py                  # Isolated DB session & TestClient fixtures
│   ├── unit/                        # Fast unit tests for config, security, exceptions, repos
│   └── integration/                 # Integration tests for API endpoints, DB readiness, middleware
│
├── migrations/                      # Alembic database migration scripts
├── alembic.ini                      # Alembic configuration file
├── requirements.txt                 # Pinned dependencies
├── pyproject.toml                   # Project metadata, Ruff, MyPy, Pytest configuration
├── .env.example                     # Safe environment template
└── README.md                        # Developer onboarding guide
```

---

## 3. Core Principles

1. **Explicit Layer Separation**:
   - **Router**: Responsible strictly for HTTP protocol concerns (headers, status codes, schema serialization).
   - **Service**: Responsible for domain logic, validation of business rules, and defining explicit database transaction boundaries.
   - **Repository**: Responsible for database queries and data persistence through SQLAlchemy 2.x.
   - **Model**: Declarative database representation.
   - **Schema**: API contracts for client requests and responses.

2. **Synchronous SQLAlchemy with Explicit Transactions**:
   - Predictable transactional lifecycle per request (`get_db()` dependency).
   - Base services encapsulate multi-repository operations inside `execute_in_transaction`.

3. **Production Safety**:
   - Insecure configuration (e.g., default JWT secrets or SQLite URLs in production) fails fast at startup.
   - Database and internal server errors are sanitized before returning to clients.
