from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_profile_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/profile")

    assert response.status_code == 401


def test_create_and_read_profile(client: TestClient) -> None:
    headers = _auth_headers(client)
    payload = {
        "full_name": "Asha Student",
        "target_role": "Machine Learning Engineer",
        "experience_level": "Fresher",
        "bio": "Final year CSE AIML student.",
    }

    create_response = client.post("/api/v1/profile", json=payload, headers=headers)
    read_response = client.get("/api/v1/profile", headers=headers)

    assert create_response.status_code == 201
    assert read_response.status_code == 200
    assert read_response.json()["target_role"] == "Machine Learning Engineer"


def test_update_profile(client: TestClient) -> None:
    headers = _auth_headers(client)

    response = client.put(
        "/api/v1/profile",
        json={"full_name": "Asha Student", "target_role": "Backend Developer"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["target_role"] == "Backend Developer"
