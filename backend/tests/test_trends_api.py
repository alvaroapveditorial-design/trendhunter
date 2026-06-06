"""MVP API contract tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_seeded_trends():
    with TestClient(app) as client:
        response = client.get("/api/v1/trends")

    assert response.status_code == 200
    trends = response.json()
    assert len(trends) >= 3
    assert trends[0]["trend_score"] >= trends[-1]["trend_score"]


def test_get_trend_detail_by_slug():
    with TestClient(app) as client:
        response = client.get("/api/v1/trends/ai-copilots-vertical-saas")

    assert response.status_code == 200
    trend = response.json()
    assert trend["slug"] == "ai-copilots-vertical-saas"
    assert trend["sources"]


def test_list_categories():
    with TestClient(app) as client:
        response = client.get("/api/v1/trends/meta/categories")

    assert response.status_code == 200
    assert "ai_saas" in response.json()
