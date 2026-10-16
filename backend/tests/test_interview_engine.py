from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_interview_requires_authentication(client: TestClient) -> None:
    response = client.post(
        "/api/v1/interviews",
        json={"role": "Python Developer", "interview_type": "technical", "difficulty": "beginner"},
    )

    assert response.status_code == 401


def test_create_interview_starts_active(client: TestClient) -> None:
    headers = _auth_headers(client)

    response = client.post(
        "/api/v1/interviews",
        json={
            "role": "Python Developer",
            "interview_type": "technical",
            "difficulty": "beginner",
            "question_count": 3,
        },
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "active"
    assert body["target_question_count"] == 3
    assert body["current_difficulty"] == "beginner"
    assert body["questions"] == []


def test_next_question_comes_from_the_question_bank(client: TestClient, seeded_bank: None) -> None:
    headers = _auth_headers(client)
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Python Developer", "interview_type": "technical", "difficulty": "beginner"},
        headers=headers,
    ).json()

    response = client.post(f"/api/v1/interviews/{interview['id']}/next", headers=headers)

    assert response.status_code == 201
    body = response.json()
    assert body["source"] == "bank"
    assert body["position"] == 1
    assert body["prompt"]
    assert body["difficulty"] == "beginner"


def test_interview_does_not_repeat_bank_questions(client: TestClient, seeded_bank: None) -> None:
    headers = _auth_headers(client)
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Backend Developer", "interview_type": "technical", "difficulty": "intermediate", "question_count": 5},
        headers=headers,
    ).json()

    first = client.post(f"/api/v1/interviews/{interview['id']}/next", headers=headers).json()
    second = client.post(f"/api/v1/interviews/{interview['id']}/next", headers=headers).json()

    assert first["prompt"] != second["prompt"]
    assert first["position"] == 1
    assert second["position"] == 2


def test_next_question_without_bank_or_provider_returns_service_unavailable(client: TestClient) -> None:
    headers = _auth_headers(client)
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Astronaut", "interview_type": "technical", "difficulty": "advanced"},
        headers=headers,
    ).json()

    response = client.post(f"/api/v1/interviews/{interview['id']}/next", headers=headers)

    assert response.status_code == 503


def test_complete_interview_marks_it_completed(client: TestClient) -> None:
    headers = _auth_headers(client)
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Python Developer", "interview_type": "technical"},
        headers=headers,
    ).json()

    response = client.post(f"/api/v1/interviews/{interview['id']}/complete", headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["completed_at"] is not None


def test_user_cannot_access_another_users_interview(client: TestClient) -> None:
    owner_headers = _auth_headers(client)
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Python Developer", "interview_type": "technical"},
        headers=owner_headers,
    ).json()

    other = client.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "password": "strongpass123"},
    ).json()
    other_headers = {"Authorization": f"Bearer {other['access_token']}"}

    response = client.get(f"/api/v1/interviews/{interview['id']}", headers=other_headers)

    assert response.status_code == 404
