# Gandheevijaya Threat Model & Mitigations

| Threat | Impact | Mitigation Strategy | Remaining Limitation |
| :--- | :--- | :--- | :--- |
| **Credential Stuffing / Brute-Force** | Account Compromise | Generic timing-safe login errors; audit logging of failed attempts (`LOGIN_FAILURE`). | Distributed IP rate limiting deferred to production proxy (e.g. Cloudflare / Nginx). |
| **JWT Access Token Theft** | Unauthorized API Access | Short access token lifetime (60m); minimal claims; HTTPS transport in production. | Access tokens remain valid until expiration. Instant access token revocation requires token blacklisting. |
| **Refresh Token Theft** | Session Hijacking | Refresh Token Rotation; SHA-256 token hashing in DB; HttpOnly secure cookies. | Requires user interaction to trigger rotation and detect reuse. |
| **Refresh Token Replay (Reuse Attack)** | Unauthorized Session Refresh | Token Family Reuse Detection automatically revokes all tokens in the compromised family. | Attacker gets 1 initial refresh if stolen before legitimate client uses it. |
| **Insecure Direct Object Reference (IDOR)** | Student Data Leakage | Server-side `verify_owner_or_admin` helper validating resource owner against `current_user.id`. | None. Enforced server-side across endpoints. |
| **Privilege Escalation** | Admin Account Takeover | Public registration strictly produces `STUDENT` role; role changes restricted to admin endpoints; CLI bootstrap script. | None. Server-side role enforcement. |
| **Quiz Answer Leakage** | Exam Integrity Compromise | `QuestionForQuizStudent` schema strips `correct_answer` and `explanation`; server-side scoring. | None. Frontend never receives answer key during quiz. |
| **SQL Injection** | Database Breach | SQLAlchemy 2.x parameterized queries; strict type coercion. | None. |
| **XSS Attack** | Cookie / Token Theft | HttpOnly cookies for refresh tokens; `X-Content-Type-Options: nosniff`; React automatic escaping. | HTML rich-text rendering in future features will require DOMPurify sanitization. |
| **Account Enumeration** | User Harvesting | Uniform generic error messages on `/login`, `/register`, `/forgot-password`. | Response timing variances may exist at millisecond scale. |
