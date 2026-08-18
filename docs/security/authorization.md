# Authorization & RBAC Architecture

## Conceptual Role Model
Gandheevijaya enforces role-based authorization using explicit server-side role models:
- **`STUDENT`**: Default role for learners taking quizzes, viewing study materials, and managing personal attempt histories.
- **`ADMIN`**: Privileged role for platform administrators creating content, managing quizzes, importing questions, and toggling user account statuses.

```
USER
 ├── STUDENT
 └── ADMIN
```

## Authorization Dependencies
Authorization logic is centralized in `backend/app/api/deps.py`:
- `require_authenticated_user()`: Ensures user is authenticated and `is_active`.
- `require_student()`: Restricts endpoint access to `STUDENT` and `ADMIN`.
- `require_admin()`: Restricts endpoint access exclusively to `ADMIN` (returns 403 Forbidden).

## Resource Ownership & IDOR Protection
To prevent Insecure Direct Object Reference (IDOR) vulnerabilities, the server enforces strict ownership checks via `verify_owner_or_admin(resource_user_id, current_user)`:
- If `current_user.id == resource_user_id`: Access Granted.
- If `current_user.role == "ADMIN"`: Access Granted.
- Otherwise: `403 Forbidden` ("Access denied. You do not own this resource.").

## Authorization Matrix

| Resource / Endpoint | STUDENT | ADMIN | Enforcement Mechanism |
| :--- | :--- | :--- | :--- |
| Public Exams & Subjects | READ | READ | `require_student` / `get_current_user` |
| Quizzes & Study Materials | READ | CRUD | `require_student` (read) / `require_admin` (write) |
| Question Management | NO | CRUD | `require_admin` |
| Content Imports | NO | YES | `require_admin` |
| Own Attempts & Results | CRUD* | READ | `verify_owner_or_admin` |
| Other Students' Attempts | NO | READ | `verify_owner_or_admin` (Blocks cross-user access) |
| Own Profile | READ/EDIT | READ | `verify_owner_or_admin` |
| User Status Administration | NO | YES | `require_admin` |
