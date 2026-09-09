from fastapi.testclient import TestClient


def test_recommendations_match_symptoms(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={"message": "I feel stressed and cannot sleep", "limit": 3},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"]
    assert body["recommendations"][0]["slug"] == "lavender"
    assert {"stress", "sleep"} <= set(body["detected_symptoms"])
    assert "not medical advice" in body["reply"].lower()


def test_recommendations_no_match_returns_safe_fallback(client: TestClient) -> None:
    response = client.post("/api/v1/recommendations", json={"message": "I want something purple"})

    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"] == []
    assert body["detected_symptoms"] == []
    assert "not medical advice" in body["reply"].lower()
