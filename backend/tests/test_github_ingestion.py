"""GitHub ingestion tests."""

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.schemas import SignalIngest
from app.services.github_collector import GitHubCollector


def test_github_endpoint_ingests_collected_repositories(monkeypatch):
    def fake_collect(self, query=None, limit=10):
        return [
            SignalIngest(
                title="openai/agents-sdk",
                content="Build AI agents with a lightweight developer SDK.",
                source_type="github",
                source_url="https://github.com/openai/agents-sdk",
                source_id="123",
                author="openai",
                upvotes=1200,
                comments=44,
                shares=88,
                keywords=["ai", "developer tools", "python"],
                category="ai_saas",
            )
        ]

    monkeypatch.setattr(GitHubCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=1")

    assert response.status_code == 201
    payload = response.json()
    assert payload["source_type"] == "github"
    assert payload["fetched_signals"] == 1
    assert payload["processed_signals"] == 1
    assert payload["trends"][0]["category"] == "ai_saas"
    assert payload["trends"][0]["trend_score"] > 50


def test_github_endpoint_handles_empty_collection(monkeypatch):
    monkeypatch.setattr(GitHubCollector, "collect", lambda self, query=None, limit=10: [])

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=3")

    assert response.status_code == 201
    payload = response.json()
    assert payload["processed_signals"] == 0
    assert payload["fetched_signals"] == 0
    assert payload["skipped_signals"] == 3


def test_github_endpoint_returns_bad_gateway_on_fetch_error(monkeypatch):
    def fail_collect(self, query=None, limit=10):
        raise httpx.ConnectError("network unavailable")

    monkeypatch.setattr(GitHubCollector, "collect", fail_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=3")

    assert response.status_code == 502
    assert response.json()["detail"] == "Could not fetch GitHub repositories. Try again later."


def test_github_repo_maps_to_signal():
    collector = GitHubCollector(base_url="https://example.test")
    signal = collector._repo_to_signal(
        {
            "id": 123,
            "full_name": "openai/agents-sdk",
            "html_url": "https://github.com/openai/agents-sdk",
            "description": "Build AI agents with a lightweight developer SDK.",
            "owner": {"login": "openai"},
            "language": "Python",
            "topics": ["ai", "agents", "sdk"],
            "stargazers_count": 1200,
            "open_issues_count": 44,
            "forks_count": 88,
            "pushed_at": "2026-06-06T12:00:00Z",
        }
    )

    assert signal.source_type == "github"
    assert signal.source_id == "123"
    assert signal.upvotes == 1200
    assert signal.shares == 88
    assert signal.category == "ai_saas"
    assert "developer tools" in signal.keywords
