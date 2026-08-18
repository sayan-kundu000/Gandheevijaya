from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    raw_password = "SecretPassword123!"
    hashed = get_password_hash(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_token_creation_and_decoding():
    user_id = "user_uuid_12345"
    role = "STUDENT"
    token = create_access_token(subject=user_id, role=role)
    payload = decode_token(token)

    assert payload.get("sub") == user_id
    assert payload.get("role") == role
    assert "exp" in payload


def test_refresh_token():
    user_id = "user_uuid_999"
    token = create_refresh_token(subject=user_id)
    payload = decode_token(token)

    assert payload.get("sub") == user_id
    assert payload.get("type") == "refresh"


def test_invalid_token_returns_empty_dict():
    assert decode_token("invalid.token.payload") == {}
