# Token Security & Rotation Strategy

## Dual Token Model

### Access Token
- **Lifetime**: 60 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Signing Algorithm**: HS256 (configurable)
- **Secret Management**: Loaded exclusively from environment (`JWT_SECRET_KEY`). Production startup fails fast if insecure default secrets are detected.
- **Claims Payload**:
  ```json
  {
    "sub": "<user_id>",
    "role": "STUDENT",
    "type": "access",
    "jti": "<unique_jwt_id>",
    "iat": 1723630000,
    "exp": 1723633600
  }
  ```

### Refresh Token & Rotation
- **Lifetime**: 7 days (`REFRESH_TOKEN_EXPIRE_DAYS`)
- **Storage**: Raw refresh token strings are NEVER saved in the database. PostgreSQL stores a SHA-256 fingerprint (`token_hash`) in table `refresh_tokens`.
- **Rotation Mechanism**: Every `/api/v1/auth/refresh` invocation revokes the current refresh token (`revoked_at = now`) and issues a new access token + new refresh token in the same `family_id`.

## Token Reuse Detection
If a previously revoked refresh token is presented again (indicating token theft or replay attack):
1. The backend immediately detects token reuse (`token_record.revoked_at is not None`).
2. The entire token family (`family_id`) associated with that session is immediately revoked in PostgreSQL.
3. A security audit event `TOKEN_REUSE_DETECTED` is logged with the user ID, IP address, and family ID.
4. The client receives a `401 Unauthorized` response.
