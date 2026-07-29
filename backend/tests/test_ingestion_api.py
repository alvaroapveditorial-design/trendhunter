"""MVP ingestion API tests."""

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


def test_demo_ingestion_creates_or_updates_trends():
    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/demo")

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 2
    assert payload["created_trends"] + payload["updated_trends"] == 2
    assert payload["trends"]


def test_ingestion_mutations_require_key_when_configured(monkeypatch):
    monkeypatch.setenv("INGESTION_API_KEY", "test-ingestion-key")
    get_settings.cache_clear()

    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/ingestion/demo")
            authed_response = client.post(
                "/api/v1/ingestion/demo",
                headers={"X-Ingestion-Key": "test-ingestion-key"},
            )
    finally:
        get_settings.cache_clear()

    assert response.status_code == 401
    assert response.json()["detail"] == "Ingestion key required."
    assert authed_response.status_code == 201


def test_manual_signal_ingestion_returns_scored_trend():
    signal_title = "AI assistants for restaurant inventory planning"

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": signal_title,
                        "content": "Operators are asking for AI tools that predict ingredient demand and reduce waste.",
                        "source_type": "manual_test",
                        "source_id": "restaurant-inventory-ai-test",
                        "upvotes": 88,
                        "comments": 17,
                        "shares": 9,
                        "keywords": ["restaurant inventory AI", "demand planning"],
                        "category": "ai_saas",
                    }
                ]
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 1
    assert payload["trends"][0]["trend_score"] > 50
    assert payload["trends"][0]["category"] == "ai_saas"


def test_off_topic_hackernews_signal_via_raw_endpoint_is_skipped():
    """Regression test: found live -- 'Half-Life ported to Mac OS 9' became a
    trend despite HackerNewsCollector's own relevance filter rejecting it,
    because it arrived through the raw /ingestion/signals endpoint, which
    bypasses collector-level filtering entirely. DetectorService must enforce
    the same relevance gate as a choke point, not just the collectors."""
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "Half-Life ported to Mac OS 9",
                        "content": "A hobbyist project porting the 1998 game to a 2001 operating system.",
                        "source_type": "hackernews",
                        "source_id": "off-topic-regression-test",
                        "upvotes": 200,
                        "comments": 40,
                    }
                ]
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 1
    assert payload["created_trends"] == 0
    assert payload["updated_trends"] == 0
    assert payload["trends"] == []


def test_non_english_signal_via_raw_endpoint_is_skipped():
    """Regression test for the same class of bug as the off-topic one above,
    but for language: the raw /ingestion/signals endpoint has no source-type
    dependent filter at all, so without a central gate any source_type could
    carry non-English content straight through."""
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "开源持续推理基准研究平台的最新更新",
                        "content": "这是一个关于开源推理平台的中文描述内容测试",
                        "source_type": "github",
                        "source_id": "non-english-regression-test",
                        "upvotes": 100,
                        "comments": 5,
                    }
                ]
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["created_trends"] == 0
    assert payload["updated_trends"] == 0


def test_signal_keywords_drop_filler_words():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "Now you can automate onboarding workflows",
                        "content": "Some teams want AI onboarding flows that reduce manual setup.",
                        "source_type": "manual_test",
                        "source_id": "filler-keywords-test",
                        "upvotes": 40,
                        "comments": 4,
                        "keywords": ["now", "you", "some", "onboarding automation"],
                    }
                ]
            },
        )

    assert response.status_code == 201
    keywords = response.json()["trends"][0]["keywords"]
    assert "now" not in keywords
    assert "you" not in keywords
    assert "some" not in keywords
    assert "onboarding automation" in keywords


def test_existing_filler_keywords_are_cleaned_on_update():
    with TestClient(app) as client:
        client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "Privacy analytics for onboarding funnels",
                        "content": "EU founders want privacy analytics for activation.",
                        "source_type": "manual_test",
                        "source_id": "privacy-cleanup-seed",
                        "upvotes": 20,
                        "comments": 2,
                        "keywords": ["privacy analytics", "now", "you"],
                        "category": "privacy",
                    }
                ]
            },
        )
        response = client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "Privacy analytics for onboarding funnels",
                        "content": "Cookie-light onboarding analytics for EU SaaS teams.",
                        "source_type": "manual_test",
                        "source_id": "privacy-cleanup-update",
                        "upvotes": 30,
                        "comments": 3,
                        "keywords": ["privacy analytics", "some", "want"],
                        "category": "privacy",
                    }
                ]
            },
        )

    assert response.status_code == 201
    keywords = response.json()["trends"][0]["keywords"]
    assert "now" not in keywords
    assert "you" not in keywords
    assert "some" not in keywords
    assert "want" not in keywords
    assert "privacy analytics" in keywords


def test_generic_ai_keyword_does_not_become_title():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "Show HN: AI copilot for database migrations",
                        "content": "Developers are testing migration copilots for production databases.",
                        "source_type": "hackernews",
                        "source_id": "generic-title-test",
                        "upvotes": 77,
                        "comments": 12,
                        "keywords": ["ai"],
                        "category": "ai_saas",
                    }
                ]
            },
        )

    assert response.status_code == 201
    assert response.json()["trends"][0]["title"] == "Hn AI Copilot Database Migrations"


def test_ingested_trend_is_queryable():
    with TestClient(app) as client:
        client.post(
            "/api/v1/ingestion/signals",
            json={
                "signals": [
                    {
                        "title": "Compliance copilots for EU marketplace sellers",
                        "content": "Marketplace sellers need help tracking VAT, product safety, and listing compliance changes.",
                        "source_type": "manual_test",
                        "source_id": "eu-marketplace-compliance-copilot",
                        "upvotes": 54,
                        "comments": 11,
                        "keywords": ["compliance copilot", "marketplace sellers"],
                        "category": "ai_saas",
                    }
                ]
            },
        )
        response = client.get("/api/v1/trends?q=compliance")

    assert response.status_code == 200
    assert any("Compliance" in trend["title"] for trend in response.json())


def test_ingestion_runs_are_listed():
    with TestClient(app) as client:
        client.post("/api/v1/ingestion/demo")
        response = client.get("/api/v1/ingestion/runs")

    assert response.status_code == 200
    runs = response.json()
    assert runs
    assert runs[0]["agent_name"] == "mvp_heuristic_detector"
