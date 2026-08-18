# Password Security Policy & Architecture

## Hashing Standard
- **Algorithm**: **Argon2id** (via `passlib[argon2]`).
- **Storage**: Passwords are standardly hashed before database persistence. Plaintext passwords or reversible formats are never stored or logged.

## Password Policy
- **Minimum Length**: 8 characters (`PASSWORD_MIN_LENGTH`).
- **Validation**: Non-blank, space-trimmed check enforced via Pydantic validators.

## Password Change & Session Invalidation
- **Endpoint**: `POST /api/v1/auth/change-password`
- **Workflow**:
  1. Authenticates current user.
  2. Verifies current password against stored Argon2id hash.
  3. Validates new password length.
  4. Hashes new password and updates `User.password_hash`.
  5. **Session Invalidation**: Instantly revokes ALL active refresh token sessions for the user (`AuthService.logout_all_sessions`).
  6. Clears auth cookies and returns confirmation.

## Password Reset Architecture
- **Endpoints**: `POST /api/v1/auth/forgot-password` and `POST /api/v1/auth/reset-password`.
- **Token Generation**: Cryptographically random 64-character hex strings (`secrets.token_hex`).
- **Token Persistence**: SHA-256 fingerprint saved in `password_reset_tokens` table.
- **Expiration & One-Time Use**: Reset tokens expire after 30 minutes (`RESET_TOKEN_EXPIRE_MINUTES`) and are marked `used_at` upon consumption.
- **Enumeration Protection**: `/forgot-password` returns a uniform message regardless of email existence.
