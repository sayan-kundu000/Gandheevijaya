# Security Testing Strategy & Guide

## Overview
The Gandheevijaya test suite includes specialized security regression and functional tests in `backend/tests/security/`.

## Security Test Modules
1. **`test_authentication.py`**:
   - Student self-registration (verifies role defaulted to `STUDENT`).
   - Login with valid credentials (verifies access token, user profile, cookies).
   - Login with invalid password / non-existent email (verifies uniform 401 generic error message).
   - `/auth/me` endpoint authorization.
2. **`test_tokens_and_rotation.py`**:
   - Expired access token rejection (verifies 401 Unauthorized).
   - Refresh token rotation (verifies new access token & new refresh token issued).
   - **Token Reuse Attack Detection** (verifies that presenting a previously rotated refresh token revokes the entire family).
   - Logout and logout-all token revocation.
3. **`test_authorization.py`**:
   - Student vs. Admin role restrictions.
   - Public registration role escalation attempt (`{"role": "ADMIN"}`) rejection.
   - Admin-only endpoint protection (verifies 403 Forbidden for students).
4. **`test_idor.py`**:
   - Student A vs. Student B attempt isolation (verifies Student B cannot view Student A's data).
   - Admin access override verification.
5. **`test_answer_leak.py`**:
   - Student-facing question payload audit (verifies `correct_answer` and `explanation` are absent).
   - Admin-facing question payload verification (verifies complete answer key accessible to admin).
6. **`test_password_and_account.py`**:
   - Argon2id hashing & verification.
   - Password change session invalidation.
   - Account disablement (`is_active=False`) access blocking.

## Running Security Tests
Execute all security tests:
```powershell
py -m pytest backend/tests/security -v
```
