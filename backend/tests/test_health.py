from fastapi.testclient import TestClient


def test_health_check_returns_service_status(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_name": "AI Interview Coach Test",
        "environment": "test",
        "database": "available",
    }
