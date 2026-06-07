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
    assert "primary_source_type" in trends[0]


def test_list_trends_can_filter_by_source_type():
    with TestClient(app) as client:
        client.post("/api/v1/ingestion/demo")
        response = client.get("/api/v1/trends?source_type=demo")

    assert response.status_code == 200
    trends = response.json()
    assert trends
    assert all(trend["source_count"] >= 1 for trend in trends)


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


def test_list_sources():
    with TestClient(app) as client:
        client.post("/api/v1/ingestion/demo")
        response = client.get("/api/v1/trends/meta/sources")

    assert response.status_code == 200
    assert "demo" in response.json()
