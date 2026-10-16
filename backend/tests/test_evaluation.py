from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "student@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_interview_and_question(client: TestClient, headers: dict[str, str]) -> tuple[str, str]:
    """Helper: create interview + ask first question, return (interview_id, question_id)."""
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Python Developer", "interview_type": "technical", "difficulty": "beginner"},
        headers=headers,
    ).json()
    question = client.post(f"/api/v1/interviews/{interview['id']}/next", headers=headers).json()
    return interview["id"], question["id"]


def test_submit_answer_returns_evaluation_with_text_features(client: TestClient, seeded_bank: None) -> None:
    headers = _auth_headers(client)
    interview_id, question_id = _create_interview_and_question(client, headers)

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/{question_id}/answers",
        json={"content": "A list is mutable and a tuple is immutable. Lists use square brackets and tuples use parentheses."},
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["answer_id"]
    assert body["word_count"] > 0

    evaluation = body["evaluation"]
    assert evaluation["text_features"]["word_count"] > 0
    assert evaluation["method_map"]["text_features"] == "nlp:deterministic"

    # No LLM provider configured in tests, so LLM scores should be None
    assert evaluation["overall_score"] is None
    assert evaluation["strengths"] == []


def test_submit_answer_rejects_duplicate(client: TestClient, seeded_bank: None) -> None:
    headers = _auth_headers(client)
    interview_id, question_id = _create_interview_and_question(client, headers)
    payload = {"content": "A list is mutable and a tuple is immutable."}

    first = client.post(
        f"/api/v1/interviews/{interview_id}/questions/{question_id}/answers",
        json=payload,
        headers=headers,
    )
    second = client.post(
        f"/api/v1/interviews/{interview_id}/questions/{question_id}/answers",
        json=payload,
        headers=headers,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_submit_answer_to_nonexistent_question_returns_404(client: TestClient, seeded_bank: None) -> None:
    headers = _auth_headers(client)
    interview = client.post(
        "/api/v1/interviews",
        json={"role": "Python Developer", "interview_type": "technical"},
        headers=headers,
    ).json()

    response = client.post(
        f"/api/v1/interviews/{interview['id']}/questions/nonexistent-id/answers",
        json={"content": "Some answer."},
        headers=headers,
    )

    assert response.status_code == 404
