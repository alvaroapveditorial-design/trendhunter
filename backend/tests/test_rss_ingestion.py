"""RSS ingestion tests."""

from datetime import datetime

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.schemas import SignalIngest
from app.services.rss_collector import RSSCollector


def test_rss_endpoint_ingests_collected_signals(monkeypatch):
    def fake_collect(self, feed=None, limit=10):
        return [
            SignalIngest(
                title="AI tools for founder research workflows",
                content="Founders are using AI to monitor markets and validate SaaS ideas.",
                source_type="rss",
                source_url="https://example.com/ai-founder-research",
                source_id="https://example.com/ai-founder-research",
                author="Reporter",
                keywords=["ai", "startup"],
                published_at=datetime.utcnow(),
            )
        ]

    monkeypatch.setattr(RSSCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/rss?feed=techcrunch_startups&limit=1")

    assert response.status_code == 201
    payload = response.json()
    assert payload["source_type"] == "rss"
    assert payload["fetched_signals"] == 1
    assert payload["processed_signals"] == 1
    assert payload["trends"][0]["trend_score"] >= 45
    assert payload["trends"][0]["category"] == "ai_saas"
    assert payload["trends"][0]["title"] == "Ai Tools Founder Research Workflows"


def test_rss_endpoint_lists_configured_feeds():
    with TestClient(app) as client:
        response = client.get("/api/v1/ingestion/rss/feeds")

    assert response.status_code == 200
    assert "techcrunch_startups" in response.json()


def test_rss_endpoint_handles_empty_collection(monkeypatch):
    monkeypatch.setattr(RSSCollector, "collect", lambda self, feed=None, limit=10: [])

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/rss?limit=3")

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 0
    assert payload["fetched_signals"] == 0
    assert payload["skipped_signals"] == 3


def test_rss_endpoint_returns_bad_request_for_unknown_feed(monkeypatch):
    def fail_collect(self, feed=None, limit=10):
        raise ValueError("Unknown RSS feed: nope")

    monkeypatch.setattr(RSSCollector, "collect", fail_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/rss?feed=nope&limit=3")

    assert response.status_code == 400
    assert response.json()["detail"] == "Unknown RSS feed: nope"


def test_rss_endpoint_returns_bad_gateway_on_fetch_error(monkeypatch):
    def fail_collect(self, feed=None, limit=10):
        raise httpx.ConnectError("network unavailable")

    monkeypatch.setattr(RSSCollector, "collect", fail_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/rss?limit=3")

    assert response.status_code == 502
    assert response.json()["detail"] == "Could not fetch RSS feed. Try again later."


def test_rss_collector_maps_rss_item_to_signal():
    xml = """
    <rss version="2.0">
      <channel>
        <item>
          <title>AI agents for SaaS finance teams</title>
          <link>https://example.com/ai-agents</link>
          <description><![CDATA[Founders are building <b>workflow</b> agents.]]></description>
          <pubDate>Sat, 06 Jun 2026 12:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>
    """

    signals = RSSCollector()._parse(
        xml,
        feed_key="techcrunch_startups",
        feed_url="https://example.com/feed",
        limit=5,
    )

    assert len(signals) == 1
    signal = signals[0]
    assert signal.source_type == "rss"
    assert signal.source_id == "https://example.com/ai-agents"
    assert signal.content == "Founders are building workflow agents."
    assert signal.category == "ai_saas"
    assert signal.upvotes > 0
    assert "ai" in signal.keywords
    assert "startup" in signal.keywords


def test_rss_collector_maps_atom_entry_to_signal():
    xml = """
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>Developer API trends</title>
        <link href="https://example.com/api-trends" />
        <summary>Database and GitHub tooling are getting attention.</summary>
        <updated>2026-06-06T12:00:00Z</updated>
      </entry>
    </feed>
    """

    signals = RSSCollector()._parse(
        xml,
        feed_key="hn_frontpage",
        feed_url="https://example.com/feed",
        limit=5,
    )

    assert len(signals) == 1
    assert signals[0].source_url == "https://example.com/api-trends"
    assert signals[0].category == "developer_tools"
    assert "developer tools" in signals[0].keywords


def test_rss_collector_uses_feed_category_fallbacks():
    xml = """
    <rss version="2.0">
      <channel>
        <item>
          <title>Fox Issue Tracker</title>
          <link>https://example.com/issue-tracker</link>
          <description>Track, plan, and release.</description>
        </item>
      </channel>
    </rss>
    """

    signals = RSSCollector()._parse(
        xml,
        feed_key="producthunt",
        feed_url="https://example.com/feed",
        limit=5,
    )

    assert len(signals) == 1
    assert signals[0].category == "product"


def test_rss_collector_removes_producthunt_boilerplate():
    xml = """
    <rss version="2.0">
      <channel>
        <item>
          <title>Manus Shopify Connector</title>
          <link>https://example.com/shopify</link>
          <description>Build and manage Shopify stores from one chat Discussion | Link</description>
        </item>
      </channel>
    </rss>
    """

    signal = RSSCollector()._parse(
        xml,
        feed_key="producthunt",
        feed_url="https://example.com/feed",
        limit=1,
    )[0]

    assert signal.content == "Build and manage Shopify stores from one chat"


def test_rss_ingestion_uses_article_title_not_feed_name(monkeypatch):
    def fake_collect(self, feed=None, limit=10):
        return [
            SignalIngest(
                title="Startup founders use AI copilots for sales research",
                content="Teams are automating prospect research workflows.",
                source_type="rss",
                source_url="https://example.com/sales-research",
                source_id="https://example.com/sales-research",
                upvotes=0,
                comments=0,
                shares=0,
                keywords=["startup news", "ai", "startup"],
                category="ai_saas",
            )
        ]

    monkeypatch.setattr(RSSCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/rss?feed=techcrunch_startups&limit=1")

    assert response.status_code == 201
    trend = response.json()["trends"][0]
    assert trend["title"] == "Startup Founders Ai Copilots Sales"
    assert trend["slug"] == "startup-founders-ai-copilots-sales"
    assert trend["trend_score"] >= 45
