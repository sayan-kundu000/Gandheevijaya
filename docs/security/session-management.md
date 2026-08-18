# Session Management & Multi-Device Control

## Overview
Gandheevijaya tracks active login sessions per user across devices using the `refresh_tokens` database table.

## Cookie Configuration
Authentication credentials utilize HttpOnly secure cookies where possible:
- `HttpOnly`: True (prevents XSS cookie theft via JavaScript `document.cookie`).
- `Secure`: True in production environments (`APP_ENV == "production"`).
- `SameSite`: Lax (prevents CSRF during cross-site requests).

## Single & Multi-Session Revocation
- **Logout Current Session**: `POST /api/v1/auth/logout` revokes the specific refresh session bound to the request's refresh cookie.
- **Logout All Sessions**: `POST /api/v1/auth/logout-all` revokes every active refresh session for the user across desktop, mobile, and secondary devices.
- **Account Disablement**: Administrative account deactivation (`PATCH /api/v1/users/{user_id}/status` with `is_active=False`) instantly revokes all active sessions for the target user.
