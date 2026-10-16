"""Tests for Scikit-Learn question difficulty classification."""
from fastapi.testclient import TestClient

from app.ml.difficulty_classifier import difficulty_classifier


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "mlexpert@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_classifier_direct_predictions() -> None:
    # Beginner test
    res_beg = difficulty_classifier.predict("What is a list in Python?")
    assert res_beg["predicted_difficulty"] == "beginner"

    # Advanced test
    res_adv = difficulty_classifier.predict(
        "Design a distributed rate limiter that handles 100k requests per second across regions."
    )
    assert res_adv["predicted_difficulty"] == "advanced"
    assert res_adv["confidence"] > 0.3


def test_predict_difficulty_api_requires_auth(client: TestClient) -> None:
    response = client.post(
        "/api/v1/ml/predict-difficulty",
        json={"prompt": "What is Python?"},
    )
    assert response.status_code == 401


def test_predict_difficulty_api_success(client: TestClient) -> None:
    headers = _auth_headers(client)

    prompt = "How does React virtual DOM reconciliation work under the hood?"
    response = client.post(
        "/api/v1/ml/predict-difficulty",
        headers=headers,
        json={"prompt": prompt},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["prompt"] == prompt
    assert body["predicted_difficulty"] in ["beginner", "intermediate", "advanced"]
    assert 0.0 <= body["confidence"] <= 1.0
    assert "class_probabilities" in body
    assert body["method"].startswith("ml:")
