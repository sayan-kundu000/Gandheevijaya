# Gandheevijaya Testing Guide

## 1. Test Architecture

The testing suite is organized into distinct categories:

```text
backend/tests/
├── conftest.py                             # Reusable DB and FastAPI TestClient fixtures
├── test_db_and_import.py                  # Model creation & validation functions
├── unit/
│   ├── test_config.py                      # Pydantic Settings & environment validation
│   ├── test_exceptions.py                  # Domain exception properties and status codes
│   ├── test_security.py                    # Argon2 hashing & JWT encoding/decoding
│   └── test_repository_and_service.py      # BaseRepository CRUD & BaseService transactions
└── integration/
    ├── test_health.py                      # Health, liveness, and database ping endpoints
    ├── test_middleware.py                  # Request correlation and timing headers
    └── test_openapi_contract.py            # OpenAPI schema generation and path registry
```

---

## 2. Test Database Isolation

All database-backed tests use an **in-memory SQLite database** with `StaticPool`, wrapped in a per-function transaction fixture that automatically rolls back after each test run. This guarantees:
- Complete test isolation
- Fast execution (<2 seconds for entire suite)
- Zero contamination of development or production databases

---

## 3. Running the Test Suite

Run the full pytest suite from the project root:

```bash
py -m pytest backend/tests
```

Run unit tests only:
```bash
py -m pytest backend/tests/unit
```

Run integration tests only:
```bash
py -m pytest backend/tests/integration
```

Run with verbose output:
```bash
py -m pytest backend/tests -v
```
