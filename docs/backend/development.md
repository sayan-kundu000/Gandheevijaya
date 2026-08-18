# Gandheevijaya Developer & Deployment Guide

## 1. Local Development Setup

### Prerequisites
- Python 3.12 or 3.13
- PostgreSQL (or local SQLite fallback)

### Installation Steps

1. **Clone and create virtual environment**:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure Environment Variables**:
   ```bash
   copy .env.example .env
   ```

4. **Run Database Migrations**:
   ```bash
   py -m alembic -c backend/alembic.ini upgrade head
   ```

5. **Start Local Development Server**:
   ```bash
   py -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Verify Endpoints**:
   - Interactive Swagger API Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
   - Liveness Check: `http://localhost:8000/health`
   - Application Health: `http://localhost:8000/api/v1/health`
   - Database Readiness: `http://localhost:8000/api/v1/health/db`

---

## 2. Render Production Deployment Configuration

### Build Command:
```bash
pip install -r backend/requirements.txt && alembic -c backend/alembic.ini upgrade head
```

### Start Command:
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

### Required Render Environment Variables:
- `APP_ENV=production`
- `DEBUG=false`
- `DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>/<database>`
- `JWT_SECRET_KEY=<generate_strong_random_secret_32_chars_min>`
- `ALLOWED_CORS_ORIGINS=https://your-frontend-domain.vercel.app`
- `PORT=10000` (Render dynamically sets this)
