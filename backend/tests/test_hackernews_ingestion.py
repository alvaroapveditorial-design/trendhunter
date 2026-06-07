"""Hacker News ingestion tests."""

from datetime import datetime

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.schemas import SignalIngest
from app.services.hackernews_collector import HackerNewsCollector


def test_hackernews_endpoint_ingests_collected_signals(monkeypatch):
    def fake_collect(self, feed="top", limit=20):
        return [
            SignalIngest(
                title="Open source AI agent framework for SaaS teams",
                content="Developers are discussing agent frameworks for workflow automation.",
                source_type="hackernews",
                source_url="https://news.ycombinator.com/item?id=123",
                source_id="123",
                author="hn_user",
                upvotes=120,
                comments=44,
                keywords=["ai", "developer tools"],
                published_at=datetime.utcnow(),
            )
        ]

    monkeypatch.setattr(HackerNewsCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/hackernews?feed=top&limit=1")

    assert response.status_code == 201
    payload = response.json()
    assert payload["source_type"] == "hackernews"
    assert payload["fetched_signals"] == 1
    assert payload["processed_signals"] == 1
    assert payload["trends"][0]["trend_score"] > 50


def test_hackernews_endpoint_handles_empty_collection(monkeypatch):
    monkeypatch.setattr(HackerNewsCollector, "collect", lambda self, feed="top", limit=20: [])

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/hackernews?feed=new&limit=3")

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 0
    assert payload["fetched_signals"] == 0
    assert payload["skipped_signals"] == 3


def test_hackernews_endpoint_returns_bad_gateway_on_fetch_error(monkeypatch):
    def fail_collect(self, feed="top", limit=20):
        raise httpx.ConnectError("network unavailable")

    monkeypatch.setattr(HackerNewsCollector, "collect", fail_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/hackernews?feed=top&limit=3")

    assert response.status_code == 502
    assert response.json()["detail"] == "Could not fetch Hacker News stories. Try again later."


def test_hackernews_item_maps_to_signal():
    collector = HackerNewsCollector(base_url="https://example.test")
    signal = collector._item_to_signal(
        {
            "id": 42,
            "title": "Show HN: AI copilot for database migrations",
            "url": "https://example.com/migrations",
            "by": "founder",
            "score": 77,
            "descendants": 12,
            "time": 1_700_000_000,
            "text": "Developers &amp; founders<br>are testing migration copilots.",
        }
    )

    assert signal is not None
    assert signal.source_type == "hackernews"
    assert signal.source_id == "42"
    assert signal.upvotes == 77
    assert signal.comments == 12
    assert signal.content == "Developers & founders are testing migration copilots."
    assert "ai" in signal.keywords
    assert "developer tools" in signal.keywords


def test_hackernews_item_truncates_long_text():
    collector = HackerNewsCollector(base_url="https://example.test")
    signal = collector._item_to_signal(
        {
            "id": 43,
            "title": "Ask HN: Long launch post",
            "text": "A" * 2500,
        }
    )

    assert signal is not None
    assert signal.content is not None
    assert len(signal.content) == 2000
