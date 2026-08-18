from fastapi.testclient import TestClient

from backend.app.core.config import settings


def test_openapi_contract_generation(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/openapi.json")
    assert response.status_code == 200
    schema = response.json()

    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == settings.APP_NAME
    assert schema["info"]["version"] == settings.VERSION

    # Verify registered paths
    paths = schema["paths"]
    assert "/health" in paths or f"{settings.API_V1_STR}/health" in paths
    assert f"{settings.API_V1_STR}/health" in paths
    assert f"{settings.API_V1_STR}/health/db" in paths
    assert f"{settings.API_V1_STR}/auth/login" in paths
    assert f"{settings.API_V1_STR}/auth/register" in paths
