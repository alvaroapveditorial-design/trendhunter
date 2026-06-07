"""MVP ingestion API tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_demo_ingestion_creates_or_updates_trends():
    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/demo")

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 2
    assert payload["created_trends"] + payload["updated_trends"] == 2
    assert payload["trends"]


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
