# API Standards & Conventions

## 1. Response Contracts

### Paginated Collections
All list endpoints support standard pagination query parameters:
- `page`: Integer >= 1 (Default: 1)
- `page_size`: Integer >= 1 and <= 100 (Default: 20)

```json
{
  "items": [...],
  "total": 120,
  "page": 1,
  "page_size": 20,
  "total_pages": 6
}
```

### Error Responses
Standardized error shape returned across 4xx and 5xx responses:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Question with ID 'GCS27-ALGO-E-MCQ-999' not found.",
    "details": null,
    "request_id": "req-9b8a7c6d"
  }
}
```

## 2. HTTP Status Code Conventions
- `200 OK`: Successful read or update.
- `201 Created`: Resource successfully created.
- `204 No Content`: Successful request with empty body response.
- `400 Bad Request`: Malformed parameters or invalid client input.
- `401 Unauthorized`: Missing or invalid Bearer access token.
- `403 Forbidden`: Insufficient role permissions or IDOR violation.
- `404 Not Found`: Resource does not exist.
- `409 Conflict`: Duplicate key error or invalid state transition (e.g., re-submitting an already submitted quiz attempt).
- `422 Unprocessable Entity`: Pydantic validation failure.
- `500 Internal Server Error`: Unhandled server exception.

## 3. Answer Protection & Solution Isolation
- `GET /api/v1/questions` and `GET /api/v1/quizzes/{id}/start` return sanitized question payloads without `correct_answer` or `explanation`.
- `QuestionAdminResponse` (with full solution keys) is only returned to authenticated `ADMIN` users or via `GET /api/v1/results/{attempt_id}` post-submission.
