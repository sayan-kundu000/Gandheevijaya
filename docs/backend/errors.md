# Gandheevijaya Error Handling & Exception Architecture

## 1. Unified Error Contract

All error responses across the Gandheevijaya API adhere to a consistent structure:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found.",
    "details": null,
    "request_id": "req_84f932aa7b194d6e"
  }
}
```

---

## 2. Standard Error Codes & Status Mappings

| Exception Class | HTTP Status | Error Code | Example Scenario |
|---|---|---|---|
| `NotFoundException` | `404 Not Found` | `RESOURCE_NOT_FOUND` | Exam or Question ID does not exist |
| `ValidationException` | `422 Unprocessable Entity` | `VALIDATION_ERROR` | Request payload fails business rules |
| `ConflictException` | `409 Conflict` | `RESOURCE_CONFLICT` | Unique email duplicate, quiz duplicate |
| `UnauthorizedException` | `401 Unauthorized` | `UNAUTHORIZED` | Missing, invalid, or expired JWT |
| `ForbiddenException` | `403 Forbidden` | `FORBIDDEN` | Student attempting admin action |
| `IntegrityError` | `409 Conflict` | `RESOURCE_CONFLICT` | Database foreign key or unique constraint |
| `DatabaseException` / `SQLAlchemyError` | `500 Internal Server Error` | `DATABASE_ERROR` | Unexpected database connectivity issue |
| `Exception` (catch-all) | `500 Internal Server Error` | `INTERNAL_SERVER_ERROR` | Unhandled server exception |

---

## 3. Production Sanitization

In `production` mode (`APP_ENV="production"`):
- Internal stack traces, raw SQL queries, and sensitive filesystem paths are never leaked in error response `details`.
- All errors are logged server-side tagged with the corresponding `request_id` for investigation.
