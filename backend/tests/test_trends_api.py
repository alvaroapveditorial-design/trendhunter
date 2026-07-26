"""MVP API contract tests."""

from fastapi.testclient import TestClient

from app.core.config import get_settings
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


def test_create_trend_requires_ingestion_key_when_configured(monkeypatch):
    monkeypatch.setenv("INGESTION_API_KEY", "test-ingestion-key")
    get_settings.cache_clear()

    payload = {"title": "Manual trend", "slug": "manual-trend-key-test", "category": "ai_saas"}
    try:
        with TestClient(app) as client:
            unauthed = client.post("/api/v1/trends", json=payload)
            authed = client.post(
                "/api/v1/trends",
                json=payload,
                headers={"X-Ingestion-Key": "test-ingestion-key"},
            )
    finally:
        get_settings.cache_clear()

    assert unauthed.status_code == 401
    assert authed.status_code == 201


def test_ingestion_produces_opportunity_brief():
    with TestClient(app) as client:
        demo = client.post("/api/v1/ingestion/demo")
        assert demo.status_code == 201
        slug = demo.json()["trends"][0]["slug"]
        response = client.get(f"/api/v1/trends/{slug}")

    assert response.status_code == 200
    brief = response.json()["opportunity_brief"]
    assert brief is not None
    assert brief["icp"]
    assert brief["problem"]
    assert brief["mvp_recommendation"]
    assert brief["monetization_models"]
    assert brief["risks"]
    assert set(brief["scores"]) == {"market", "competition", "urgency", "viability", "potential"}


def test_trend_spotlight_returns_decision_bundle():
    with TestClient(app) as client:
        client.post("/api/v1/ingestion/demo")
        response = client.get("/api/v1/trends/spotlight")

    assert response.status_code == 200
    payload = response.json()
    assert payload["best_opportunity"] is not None
    assert payload["best_opportunity"]["opportunity_brief"] is not None
    assert len(payload["top_opportunities"]) >= 1
    assert len(payload["emerging_markets"]) >= 1
    assert len(payload["accelerating"]) >= 1
    # the hero trend shouldn't also be duplicated in the top_opportunities list
    best_id = payload["best_opportunity"]["id"]
    assert best_id not in {trend["id"] for trend in payload["top_opportunities"]}


def test_trend_reads_require_internal_key_when_configured(monkeypatch):
    monkeypatch.setenv("BACKEND_INTERNAL_KEY", "test-internal-key")
    get_settings.cache_clear()

    try:
        with TestClient(app) as client:
            unauthed = client.get("/api/v1/trends")
            authed = client.get("/api/v1/trends", headers={"X-Internal-Key": "test-internal-key"})
    finally:
        get_settings.cache_clear()

    assert unauthed.status_code == 401
    assert authed.status_code == 200
