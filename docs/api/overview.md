# Gandheevijaya REST API Documentation Overview

The Gandheevijaya REST API subsystem provides an intermediate-level, production-conscious API layer designed for Gandheevijaya (GATE CS, SSC, Banking exam preparation platform).

## Architecture Highlights
- **Base URL**: `/api/v1`
- **Authentication**: Dual-token OAuth2 Bearer scheme (60-minute Access Token, 7-day Refresh Token with family rotation).
- **Format**: JSON (`Content-Type: application/json`).
- **Framework**: FastAPI + Pydantic v2 + SQLAlchemy 2.x + PostgreSQL.

## Core Modules
1. **Health**: `/api/v1/health`, `/api/v1/health/db`
2. **Auth & Sessions**: `/api/v1/auth/*`
3. **Users**: `/api/v1/users/*`
4. **Exams & Categories**: `/api/v1/exams/*`
5. **Subjects**: `/api/v1/subjects/*`
6. **Topics & Subtopics**: `/api/v1/topics/*`, `/api/v1/subtopics/*`
7. **Questions**: `/api/v1/questions/*` (Role-segmented response contracts preventing answer leakage)
8. **Quizzes & Attempts**: `/api/v1/quizzes/*`, `/api/v1/attempts/*`
9. **Results & Review**: `/api/v1/results/*`
10. **Study Materials**: `/api/v1/materials/*`
11. **Performance Analytics**: `/api/v1/analytics/*`, `/api/v1/leaderboard`
12. **Admin Operations**: `/api/v1/admin/*`
