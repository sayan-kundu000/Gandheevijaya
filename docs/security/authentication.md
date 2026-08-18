# Authentication Subsystem Architecture

## Overview
Gandheevijaya utilizes a modern, stateless-stateful hybrid authentication architecture built on FastAPI, OAuth2 password bearer flow, JSON Web Tokens (JWT), and server-side refresh session tracking in PostgreSQL.

## Registration Flow
- **Endpoint**: `POST /api/v1/auth/register`
- **Input**: `email`, `password` (min 8 chars), `full_name`
- **Security Rule**: Public registration strictly assigns the `STUDENT` role. Role manipulation or self-promotion to `ADMIN` is strictly impossible via API payloads.
- **Normalization**: Emails are stripped of surrounding whitespace and lowercased before persistence. Unique database indexes ensure uniqueness.
- **Password Hashing**: Passwords are hashed before database insertion using **Argon2id**.

## Login Flow
- **Endpoint**: `POST /api/v1/auth/login`
- **Input**: `email`, `password`
- **Account Enumeration Mitigation**: Generic error messages (`"Invalid email or password"`) are returned for both invalid emails and wrong passwords to eliminate account harvesting.
- **Session Issuance**: Upon successful verification:
  1. Issues a short-lived Access JWT (60m duration) containing minimal claims (`sub`, `role`, `type="access"`, `jti`, `iat`, `exp`).
  2. Issues a long-lived Refresh Token (7d duration) saved in PostgreSQL as a SHA-256 fingerprint (`token_hash`) with a family tracking ID (`family_id`).
  3. Returns `Token` JSON response and sets secure `HttpOnly`, `SameSite=Lax` cookies.

## Current User Identification
- **Endpoint**: `GET /api/v1/auth/me`
- **Dependency**: `get_current_user()` inspects `Authorization: Bearer <token>` header or `access_token` cookie, decodes JWT, verifies signature & expiration, fetches `User` from PostgreSQL, and confirms `user.is_active == True`.
