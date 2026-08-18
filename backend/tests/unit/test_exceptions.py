from backend.app.core.exceptions import (
    ConflictException,
    DatabaseException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)


def test_custom_exceptions():
    exc = NotFoundException(message="Exam not found", details={"exam_id": 42})
    assert exc.status_code == 404
    assert exc.code == "RESOURCE_NOT_FOUND"
    assert exc.message == "Exam not found"
    assert exc.details == {"exam_id": 42}

    val_exc = ValidationException(message="Invalid format")
    assert val_exc.status_code == 422
    assert val_exc.code == "VALIDATION_ERROR"

    conflict_exc = ConflictException(message="User already exists")
    assert conflict_exc.status_code == 409
    assert conflict_exc.code == "RESOURCE_CONFLICT"

    unauth_exc = UnauthorizedException()
    assert unauth_exc.status_code == 401
    assert unauth_exc.code == "UNAUTHORIZED"

    forbid_exc = ForbiddenException()
    assert forbid_exc.status_code == 403
    assert forbid_exc.code == "FORBIDDEN"

    db_exc = DatabaseException()
    assert db_exc.status_code == 500
    assert db_exc.code == "DATABASE_ERROR"
