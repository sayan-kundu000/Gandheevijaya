# API Security & Content Protection

## Answer Protection & Solution Isolation
Quiz question answer leakage is a critical vulnerability for exam platforms.
- **Rule**: The backend NEVER sends correct options, boolean correctness indicators (`is_correct`), or detailed solutions (`explanation`) to student clients while a quiz attempt is active.
- **Enforcement**:
  - `QuestionForQuizStudent` schema explicitly omits `correct_answer` and `explanation`.
  - `QuestionForAdmin` schema is strictly restricted to administrative or post-submission evaluation endpoints.
- **Scoring**: Answers, total marks, percentage, and pass/fail statuses are calculated 100% server-side upon attempt submission. Client-submitted scores are ignored.

## Input Validation & SQL Injection Prevention
- **Pydantic**: All request payloads are strictly validated using Pydantic schemas.
- **SQLAlchemy 2.x**: All database queries use parameterized SQLAlchemy ORM or `select()` constructs. Raw SQL string concatenation is prohibited.

## Defensive Security Headers
Every response includes security headers via `SecurityHeadersMiddleware`:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: geolocation=(), camera=(), microphone=()`

## Request Log Sanitization
Structured logging sanitizes sensitive headers and attributes before output. Authorization headers, cookies, passwords, and tokens are redacted from server logs.
