# Gandheevijaya

Gandheevijaya is a multi-exam preparation, quiz assessment, solution review, and performance analysis platform. Designed as a modular monolith, it supports diverse exam taxonomies (GATE, SSC, Banking) using a robust relational schema.

---

## Backend Documentation Suite

The complete backend architectural details, API specifications, and developer guides are available in the `docs/backend/` folder:

* [Architecture Guide](docs/backend/architecture.md): Modular Monolith Architecture, Layers, and Principles.
* [API Specification](docs/backend/api.md): REST API endpoints, versioning (`/api/v1`), health checks, and correlation headers.
* [Configuration Guide](docs/backend/configuration.md): Pydantic Settings, environment variables, and production validation.
* [Database Architecture](docs/backend/database.md): SQLAlchemy 2.x, PostgreSQL/psycopg3, connection pooling, and Alembic migrations.
* [Error Handling](docs/backend/errors.md): Centralized exception hierarchy and production error response sanitization.
* [Logging & Correlation](docs/backend/logging.md): `X-Request-ID` correlation tracking and structured logging.
* [Testing Guide](docs/backend/testing.md): Pytest test runner, test database isolation, and fixtures.
* [Development & Deployment](docs/backend/development.md): Local startup and Render deployment configuration.

---

## Quickstart Guide

### 1. Prerequisites
* **Python 3.12+** (`py` or `python`)
* **Node.js (v18+) & npm** (For the React frontend UI)
* **PostgreSQL** (Optional locally; the system falls back to SQLite `gandheevijaya.db` if not configured)

---

### 2. Local Backend Setup

1. **Create and Activate Virtual Environment**:
   ```bash
   py -m venv .venv
   # Windows (PowerShell / Command Prompt):
   .\.venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate
   ```

2. **Install Backend Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure Environment Variables**:
   ```bash
   # Windows (Command Prompt / PowerShell):
   copy .env.example .env
   # macOS / Linux / Bash:
   cp .env.example .env
   ```

4. **Run Database Migrations**:
   ```bash
   py -m alembic -c backend/alembic.ini upgrade head
   ```

5. **Start FastAPI Backend Development Server**:
   ```bash
   py -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

### 3. Local Frontend Setup

1. **Navigate to Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```

3. **Start Vite Frontend Development Server**:
   ```bash
   npm run dev
   ```

---

## 🔗 Localhost Service Links

| Service / View | Description | Localhost Link |
|---|---|---|
| **React Frontend App** | User & Admin UI | [http://localhost:3000](http://localhost:3000) |
| **FastAPI Swagger Docs** | Interactive OpenAPI Specification | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc API Documentation** | Detailed API Blueprint | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| **Backend Root Health** | Liveness Check Endpoint | [http://localhost:8000/health](http://localhost:8000/health) |
| **Backend API Health** | Application Status Endpoint | [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) |
| **Database Health Check** | Database Connectivity Check | [http://localhost:8000/api/v1/health/db](http://localhost:8000/api/v1/health/db) |

---

## 🧪 Running Automated Tests

### Backend Test Suite (Pytest)
```bash
py -m pytest backend/tests
```

### Frontend Test Suite (Vitest)
```bash
cd frontend
npm test
```

---

## 🛠 CLI & Data Generation Tools

```bash
# Run question generation CLI
py scripts/cli.py --help
py scripts/cli.py --init-db
py scripts/cli.py --run-pilot
py scripts/cli.py --status

# Bulk content ingestion tool
py scripts/import_questions.py --help
```
