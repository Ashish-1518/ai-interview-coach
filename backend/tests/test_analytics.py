"""Tests for the analytics and report endpoints."""
from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "analyst@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _run_full_interview(client: TestClient, headers: dict[str, str]) -> str:
    """Create an interview, ask a question, answer it, complete it. Return interview_id."""
    interview = client.post(
        "/api/v1/interviews",
        json={
            "role": "Python Developer",
            "interview_type": "technical",
            "difficulty": "beginner",
            "question_count": 1,
        },
        headers=headers,
    ).json()
    interview_id = interview["id"]

    # Ask one question
    question = client.post(
        f"/api/v1/interviews/{interview_id}/next",
        headers=headers,
    ).json()

    # Answer it
    client.post(
        f"/api/v1/interviews/{interview_id}/questions/{question['id']}/answers",
        json={"content": "A list is mutable and a tuple is immutable. Lists use square brackets."},
        headers=headers,
    )

    # Complete
    client.post(f"/api/v1/interviews/{interview_id}/complete", headers=headers)
    return interview_id


# ---------------------------------------------------------------------------
# Report endpoint tests
# ---------------------------------------------------------------------------


def test_report_returns_full_qna(client: TestClient, seeded_bank: None) -> None:
    """GET /interviews/{id}/report should return questions, answers, and evaluations."""
    headers = _auth_headers(client)
    interview_id = _run_full_interview(client, headers)

    response = client.get(
        f"/api/v1/interviews/{interview_id}/report",
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()

    # Top-level structure
    assert body["interview"]["id"] == interview_id
    assert body["interview"]["status"] == "completed"
    assert len(body["items"]) == 1

    # The one item should have question + answer + evaluation
    item = body["items"][0]
    assert item["question"]["prompt"]
    assert item["answer_content"] is not None
    assert item["answer_word_count"] > 0
    assert item["evaluation"] is not None
    assert item["evaluation"]["text_features"]["word_count"] > 0
    assert item["evaluation"]["method_map"]["text_features"] == "nlp:deterministic"

    # Summary
    summary = body["summary"]
    assert summary["questions_asked"] == 1
    assert summary["questions_answered"] == 1
    assert summary["average_word_count"] > 0
    assert len(summary["difficulty_progression"]) == 1


def test_report_404_for_nonexistent_interview(client: TestClient) -> None:
    headers = _auth_headers(client)
    response = client.get(
        "/api/v1/interviews/nonexistent-id/report",
        headers=headers,
    )
    assert response.status_code == 404


def test_report_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/interviews/some-id/report")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Analytics endpoint tests
# ---------------------------------------------------------------------------


def test_analytics_summary_empty(client: TestClient) -> None:
    """Analytics for a user with no interviews should return zeroes."""
    headers = _auth_headers(client)
    response = client.get("/api/v1/analytics/summary", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total_interviews"] == 0
    assert body["completed_interviews"] == 0
    assert body["total_questions_answered"] == 0
    assert body["average_overall_score"] is None
    assert body["history"] == []


def test_analytics_summary_with_data(client: TestClient, seeded_bank: None) -> None:
    """Analytics after completing an interview should reflect the data."""
    headers = _auth_headers(client)
    _run_full_interview(client, headers)

    response = client.get("/api/v1/analytics/summary", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total_interviews"] == 1
    assert body["completed_interviews"] == 1
    assert body["total_questions_answered"] == 1
    assert body["total_practice_time_estimate_minutes"] == 3  # 1 question × 3 min

    # Score trend has one entry (None because no LLM in tests)
    assert len(body["score_trend"]) == 1

    # History has one entry
    assert len(body["history"]) == 1
    h = body["history"][0]
    assert h["role"] == "Python Developer"
    assert h["questions_asked"] == 1
    assert h["questions_answered"] == 1

    # Difficulty distribution
    assert body["difficulty_distribution"]["beginner"] == 1
    assert body["interview_type_distribution"]["technical"] == 1


def test_analytics_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 401
