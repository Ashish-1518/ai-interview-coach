"""End-to-end flow test — walks through a full user journey.

This uses the existing TestClient + SQLite in-memory fixture from conftest.py.
AI calls are not configured (no API key), so LLM-based scores will be None
while NLP/deterministic features still run.
"""

from fastapi.testclient import TestClient


# ── helpers ───────────────────────────────────────────────────────────────────

def _register_and_get_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "e2e@example.com", "password": "strongpass123"},
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── tests ─────────────────────────────────────────────────────────────────────

def test_full_interview_journey(client: TestClient, seeded_bank: None) -> None:
    """Register → profile → interview → answer → complete → report → analytics."""

    # 1. Register
    headers = _register_and_get_headers(client)

    # 2. Verify auth — GET /me
    me = client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "e2e@example.com"

    # 3. Create profile
    profile = client.post(
        "/api/v1/profile",
        json={
            "full_name": "E2E Tester",
            "target_role": "Python Developer",
            "experience_level": "intermediate",
            "bio": "Testing the full flow.",
        },
        headers=headers,
    )
    assert profile.status_code == 201
    assert profile.json()["full_name"] == "E2E Tester"

    # 4. Read profile back
    get_profile = client.get("/api/v1/profile", headers=headers)
    assert get_profile.status_code == 200
    assert get_profile.json()["target_role"] == "Python Developer"

    # 5. Create interview
    interview = client.post(
        "/api/v1/interviews",
        json={
            "role": "Python Developer",
            "interview_type": "technical",
            "difficulty": "beginner",
            "question_count": 3,
        },
        headers=headers,
    )
    assert interview.status_code == 201
    interview_data = interview.json()
    interview_id = interview_data["id"]
    assert interview_data["status"] == "active"
    assert interview_data["target_question_count"] == 3

    # 6. List interviews
    interviews_list = client.get("/api/v1/interviews", headers=headers)
    assert interviews_list.status_code == 200
    assert len(interviews_list.json()) == 1

    # 7. Get next question
    q1 = client.post(f"/api/v1/interviews/{interview_id}/next", headers=headers)
    assert q1.status_code == 201
    q1_data = q1.json()
    question_id = q1_data["id"]
    assert q1_data["position"] == 1
    assert q1_data["prompt"]

    # 8. Submit answer
    answer = client.post(
        f"/api/v1/interviews/{interview_id}/questions/{question_id}/answers",
        json={
            "content": (
                "A list is mutable and allows changes after creation. "
                "A tuple is immutable and cannot be modified. "
                "Lists use square brackets while tuples use parentheses. "
                "Tuples are generally faster for iteration due to immutability."
            ),
        },
        headers=headers,
    )
    assert answer.status_code == 201
    answer_data = answer.json()
    assert answer_data["answer_id"]
    assert answer_data["word_count"] > 0
    assert answer_data["evaluation"]["text_features"]["word_count"] > 0

    # 9. Complete interview
    complete = client.post(
        f"/api/v1/interviews/{interview_id}/complete",
        headers=headers,
    )
    assert complete.status_code == 200
    assert complete.json()["status"] == "completed"
    assert complete.json()["completed_at"] is not None

    # 10. Get interview report
    report = client.get(
        f"/api/v1/interviews/{interview_id}/report",
        headers=headers,
    )
    assert report.status_code == 200
    report_data = report.json()
    assert report_data["summary"]["questions_asked"] == 1
    assert report_data["summary"]["questions_answered"] == 1
    assert len(report_data["items"]) == 1
    assert report_data["items"][0]["answer_content"] is not None

    # 11. Get analytics summary
    analytics = client.get("/api/v1/analytics/summary", headers=headers)
    assert analytics.status_code == 200
    analytics_data = analytics.json()
    assert analytics_data["total_interviews"] == 1
    assert analytics_data["completed_interviews"] == 1
    assert analytics_data["total_questions_answered"] == 1


def test_voice_analysis_flow(client: TestClient) -> None:
    """Register → voice analysis — validates the voice endpoint works end-to-end."""

    headers = _register_and_get_headers(client)

    response = client.post(
        "/api/v1/voice/analyze",
        json={
            "transcript": (
                "Well um I think basically the main difference is that "
                "a list is mutable and you know a tuple is immutable. "
                "So um basically you can change a list after creating it "
                "but you can't change a tuple."
            ),
            "duration_seconds": 18.5,
        },
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["speaking_pace_wpm"] > 0
    assert body["pace_status"] in ("too_slow", "optimal", "too_fast")
    assert body["clarity_score"] >= 0
    assert body["text_features"]["filler_total"] > 0  # "um", "basically", "you know"
    assert body["method_map"]["speaking_pace"] == "deterministic:wpm_ratio"


def test_multiple_interviews_analytics(client: TestClient, seeded_bank: None) -> None:
    """Two completed interviews should both appear in analytics."""

    headers = _register_and_get_headers(client)

    for i in range(2):
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

        q = client.post(
            f"/api/v1/interviews/{interview['id']}/next",
            headers=headers,
        ).json()

        client.post(
            f"/api/v1/interviews/{interview['id']}/questions/{q['id']}/answers",
            json={"content": f"Answer number {i + 1} — some technical explanation."},
            headers=headers,
        )

        client.post(
            f"/api/v1/interviews/{interview['id']}/complete",
            headers=headers,
        )

    analytics = client.get("/api/v1/analytics/summary", headers=headers)
    assert analytics.status_code == 200
    assert analytics.json()["total_interviews"] == 2
    assert analytics.json()["completed_interviews"] == 2
    assert analytics.json()["total_questions_answered"] == 2
