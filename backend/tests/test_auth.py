from fastapi.testclient import TestClient


def test_register_creates_user_and_returns_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "Student@Example.com", "password": "strongpass123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["user"]["email"] == "student@example.com"
    assert data["user"]["is_active"] is True


def test_register_rejects_duplicate_email(client: TestClient) -> None:
    payload = {"email": "student@example.com", "password": "strongpass123"}
    first_response = client.post("/api/v1/auth/register", json=payload)
    second_response = client.post("/api/v1/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_returns_token_for_valid_credentials(client: TestClient) -> None:
    payload = {"email": "student@example.com", "password": "strongpass123"}
    client.post("/api/v1/auth/register", json=payload)

    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_rejects_wrong_password(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "strongpass123"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401


def test_me_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_returns_current_user_with_valid_token(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "strongpass123"},
    )
    token = register_response.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == "student@example.com"
