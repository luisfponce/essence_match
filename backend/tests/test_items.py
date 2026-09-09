from fastapi.testclient import TestClient


def test_list_items_returns_catalog(client: TestClient) -> None:
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 6
    assert {item["slug"] for item in body} >= {"lavender", "peppermint"}


def test_create_item(client: TestClient) -> None:
    response = client.post(
        "/api/v1/items",
        json={
            "slug": "cedarwood",
            "name": "Cedarwood",
            "description": "A warm, woodsy essence for steady evening routines.",
            "symptoms": ["grounding", "sleep"],
            "uses": ["Diffuse during evening quiet time"],
            "safety_notes": ["Dilute before topical use"],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["slug"] == "cedarwood"
    assert body["name"] == "Cedarwood"
    assert body["symptoms"] == ["grounding", "sleep"]
