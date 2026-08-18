from fastapi.testclient import TestClient


def test_request_id_generated_and_returned_in_header(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"].startswith("req_")
    assert "X-Process-Time" in response.headers


def test_custom_request_id_propagated(client: TestClient):
    custom_req_id = "test-custom-request-id-12345"
    response = client.get("/health", headers={"X-Request-ID": custom_req_id})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == custom_req_id


def test_error_response_contains_request_id_and_structure(client: TestClient):
    # Requesting a non-existent endpoint to trigger standard 404 handler
    response = client.get("/api/v1/non_existent_route")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"
    assert "message" in data["error"]
    assert "request_id" in data["error"]
    assert data["error"]["request_id"] is not None
