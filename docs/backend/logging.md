# Gandheevijaya Logging & Correlation Tracing

## 1. Request Correlation ID Architecture

To facilitate debugging across distributed requests and concurrent async tasks, Gandheevijaya implements correlation tracking:

1. **Extraction / Generation**:
   `RequestCorrelationMiddleware` checks incoming request headers for `X-Request-ID`. If absent, a unique hexadecimal token (`req_<uuid16>`) is generated.
2. **Context Propagation**:
   The identifier is stored in Python's `contextvars.ContextVar` (`request_id_ctx_var`).
3. **Filter Injection**:
   `RequestIDFilter` injects the correlation ID into every standard `logging.LogRecord`.
4. **Response Attachment**:
   The `X-Request-ID` and `X-Process-Time` headers are returned in the HTTP response.

---

## 2. Log Output Formats

### Development Format:
```text
[2026-08-14 13:45:00] [INFO] [req_84f932aa7b194d6e] gandheevijaya.access - GET /api/v1/health -> 200 (2.15ms)
```

### Production Format (JSON):
When `APP_ENV="production"`, logs are structured as JSON for ingestion into log aggregation services:
```json
{
  "timestamp": "2026-08-14T08:15:00.123456+00:00",
  "level": "INFO",
  "request_id": "req_84f932aa7b194d6e",
  "logger": "gandheevijaya.access",
  "message": "GET /api/v1/health -> 200 (2.15ms)"
}
```

---

## 3. Redaction Guidelines

Never log:
- Plaintext passwords or credentials
- Full JWT token contents
- Sensitive student identifying data
- Database connection strings with embedded passwords
