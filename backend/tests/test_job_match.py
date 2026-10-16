"""Tests for job description matching and skill gap analysis."""
from unittest.mock import patch

from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "jobmatcher@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _upload_test_pdf(client: TestClient, headers: dict[str, str]) -> str:
    fake_pdf = b"%PDF-1.4 mock pdf content"
    files = {"file": ("resume.pdf", fake_pdf, "application/pdf")}

    with patch(
        "app.services.resume_service.extract_text_from_pdf",
        return_value="Jane Doe\nEmail: jane@example.com\nSkills: Python, SQL, FastAPI, React",
    ):
        response = client.post("/api/v1/resumes", headers=headers, files=files)
        assert response.status_code == 201
        return response.json()["id"]


def test_job_match_requires_auth(client: TestClient) -> None:
    response = client.post("/api/v1/job-match", json={"jd_text": "We need a Python Developer."})
    assert response.status_code == 401


def test_job_match_404_if_no_resume(client: TestClient) -> None:
    headers = _auth_headers(client)
    response = client.post(
        "/api/v1/job-match",
        headers=headers,
        json={"jd_text": "We are seeking a senior Python developer experienced with FastAPI and Docker."},
    )
    assert response.status_code == 404
    assert "No resume found" in response.json()["detail"]


def test_job_match_success(client: TestClient) -> None:
    headers = _auth_headers(client)
    resume_id = _upload_test_pdf(client, headers)

    jd_text = (
        "We are looking for a Senior Python Backend Engineer. "
        "Required skills include Python, SQL, FastAPI, Docker, AWS, and Git. "
        "Experience building REST APIs is essential."
    )

    response = client.post(
        "/api/v1/job-match",
        headers=headers,
        json={
            "jd_text": jd_text,
            "resume_id": resume_id,
            "role_title": "Python Backend Engineer",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["resume_id"] == resume_id
    assert body["role_title"] == "Python Backend Engineer"
    assert "Python" in body["extracted_jd_skills"]
    assert "skill_gap" in body
    assert body["skill_gap"]["skill_match_percentage"] > 0.0
    assert body["semantic_similarity_score"] > 0.0
    assert body["overall_fit_score"] > 0.0
    assert len(body["recommendations"]) > 0
    assert body["method_map"]["skill_match"] == "heuristic:set_intersection"
    assert body["method_map"]["semantic_similarity"] == "ml:tfidf_cosine"
