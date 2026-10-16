from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_resume_upload_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/resumes")

    assert response.status_code == 401


def test_resume_upload_rejects_non_pdf(client: TestClient) -> None:
    headers = _auth_headers(client)

    response = client.post(
        "/api/v1/resumes",
        headers=headers,
        files={"file": ("resume.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF resumes are supported."
