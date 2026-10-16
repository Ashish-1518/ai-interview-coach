"""Tests for voice and speech analytics."""
from fastapi.testclient import TestClient


def _auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "speaker@example.com", "password": "strongpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_voice_requires_auth(client: TestClient) -> None:
    response = client.post(
        "/api/v1/voice/analyze",
        json={"transcript": "Testing voice.", "duration_seconds": 5.0},
    )
    assert response.status_code == 401


def test_voice_analysis_optimal_pace(client: TestClient) -> None:
    headers = _auth_headers(client)

    # 135 words spoken over 60 seconds = 135 WPM (Optimal pace 110-160)
    words = ["word"] * 135
    transcript = " ".join(words) + "."

    response = client.post(
        "/api/v1/voice/analyze",
        headers=headers,
        json={"transcript": transcript, "duration_seconds": 60.0},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["speaking_pace_wpm"] == 135.0
    assert body["pace_status"] == "optimal"
    assert body["clarity_score"] >= 90.0
    assert body["method_map"]["speaking_pace"] == "deterministic:wpm_ratio"


def test_voice_analysis_fast_pace_with_fillers(client: TestClient) -> None:
    headers = _auth_headers(client)

    # Fast pace (> 160 WPM) with filler words like "um", "like", "basically"
    transcript = "So basically I um like built a model and um like deployed it on AWS literally."

    response = client.post(
        "/api/v1/voice/analyze",
        headers=headers,
        json={"transcript": transcript, "duration_seconds": 3.0},  # ~15 words in 3 sec = 300 WPM
    )

    assert response.status_code == 200
    body = response.json()
    assert body["speaking_pace_wpm"] > 160.0
    assert body["pace_status"] == "too_fast"
    assert body["text_features"]["filler_total"] > 0
    assert body["clarity_score"] < 100.0  # Penalized for fillers and extreme WPM
