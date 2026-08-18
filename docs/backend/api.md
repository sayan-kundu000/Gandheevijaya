# Gandheevijaya API Specification & Guidelines

## 1. API Versioning

All business endpoints are version-namespaced under:
```text
/api/v1
```

The process liveness probe is available at the root level:
```text
GET /health
```

### Future Domain Namespaces
- `/api/v1/auth` - Authentication & token management
- `/api/v1/users` - Student and instructor profiles
- `/api/v1/exams` - Exam categories and exam hierarchies
- `/api/v1/subjects` - Subject metadata and syllabus tree
- `/api/v1/topics` - Topic and subtopic breakdown
- `/api/v1/materials` - Study materials and notes
- `/api/v1/questions` - Question bank repository
- `/api/v1/quizzes` - Quiz configuration and question sets
- `/api/v1/attempts` - Student quiz attempts and live session
- `/api/v1/results` - Scoring, analytics, and attempt reviews
- `/api/v1/analytics` - Performance metrics and weakness index
- `/api/v1/leaderboard` - Platform leaderboards
- `/api/v1/admin` - Administrative management & import audit

---

## 2. Health & Observability Endpoints

### 2.1 Process Liveness Probe
- **Endpoint**: `GET /health`
- **Response**: `200 OK`
```json
{
  "status": "ok",
  "app": "GANDHEEVIJAYA"
}
```

### 2.2 Application Health Probe
- **Endpoint**: `GET /api/v1/health`
- **Response**: `200 OK`
```json
{
  "status": "ok",
  "service": "GANDHEEVIJAYA",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2.3 Database Readiness Probe
- **Endpoint**: `GET /api/v1/health/db`
- **Response**: `200 OK` (or `503 Service Unavailable` if database is unreachable)
```json
{
  "status": "ok",
  "service": "GANDHEEVIJAYA",
  "database": "connected",
  "version": "1.0.0",
  "error": null
}
```

---

## 3. Standard Request Headers

| Header | Description | Required |
|---|---|---|
| `Content-Type` | `application/json` | Yes (for POST/PUT/PATCH) |
| `Authorization` | `Bearer <access_token>` | For protected routes |
| `X-Request-ID` | Client correlation ID (generated if omitted) | Optional |

---

## 4. Standard Response Headers

| Header | Description |
|---|---|
| `X-Request-ID` | Correlation ID for tracing logs across the request lifecycle |
| `X-Process-Time` | Request execution latency (e.g. `0.0042s`) |
