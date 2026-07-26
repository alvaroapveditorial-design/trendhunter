"""GitHub ingestion tests."""

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.schemas import SignalIngest
from app.services.github_collector import GitHubCollector
from app.services.text_filters import looks_non_english


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


def test_github_distinct_repos_never_merge_into_one_trend(monkeypatch):
    """Regression test: two unrelated repos must never collapse into one trend,
    even if their titles happen to guess the same or a generic word."""

    def fake_collect(self, query=None, limit=10):
        return [
            SignalIngest(
                title="Snailclimb/JavaGuide",
                content="Java interview & backend guide covering fundamentals and system design.",
                source_type="github",
                source_url="https://github.com/Snailclimb/JavaGuide",
                source_id="132464395",
                upvotes=156000,
                comments=59,
                keywords=["java", "interview"],
                category="ai_saas",
            ),
            SignalIngest(
                title="langgenius/dify",
                content="Production-ready platform for agentic workflow development.",
                source_type="github",
                source_url="https://github.com/langgenius/dify",
                source_id="626805178",
                upvotes=144000,
                comments=741,
                keywords=["agent", "workflow"],
                category="ai_saas",
            ),
        ]

    monkeypatch.setattr(GitHubCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=2")

    assert response.status_code == 201
    trends = response.json()["trends"]
    trend_ids = {trend["id"] for trend in trends}
    assert len(trend_ids) == 2, "each repo must land on its own trend, not merge into one"


def test_github_same_repo_maps_to_same_trend_across_runs(monkeypatch):
    """Regression test: re-ingesting the same repo (same source_id) must always
    update the trend it was already attached to, even if the title heuristic
    would guess something different on a later run."""

    def first_run(self, query=None, limit=10):
        return [
            SignalIngest(
                title="Snailclimb/JavaGuide",
                content="Java interview & backend guide.",
                source_type="github",
                source_url="https://github.com/Snailclimb/JavaGuide",
                source_id="132464395",
                upvotes=156000,
                comments=59,
                keywords=["java", "interview"],
                category="ai_saas",
            )
        ]

    monkeypatch.setattr(GitHubCollector, "collect", first_run)
    with TestClient(app) as client:
        first = client.post("/api/v1/ingestion/github?limit=1")
        first_trend = first.json()["trends"][0]

        def second_run(self, query=None, limit=10):
            return [
                SignalIngest(
                    title="Snailclimb/JavaGuide",
                    content="Now trending with AI application development sections added.",
                    source_type="github",
                    source_url="https://github.com/Snailclimb/JavaGuide",
                    source_id="132464395",
                    upvotes=160000,
                    comments=61,
                    keywords=["agent", "ai"],
                    category="ai_saas",
                )
            ]

        monkeypatch.setattr(GitHubCollector, "collect", second_run)
        second = client.post("/api/v1/ingestion/github?limit=1")
        second_trend = second.json()["trends"][0]

    assert second_trend["id"] == first_trend["id"]
    assert second_trend["title"] == first_trend["title"]


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


def test_distinct_repos_get_distinct_scores(monkeypatch):
    """Regression test: within the stars:50..3000 range, different repos must
    not collapse onto the exact same trend_score. A linear velocity divisor
    used to saturate its cap for any repo past a few hundred stars, making
    unrelated trends look identically scored -- the opposite of what a
    scoring system is supposed to signal."""

    def fake_collect(self, query=None, limit=10):
        return [
            SignalIngest(
                title="acme/small-tool",
                content="A small emerging developer tool.",
                source_type="github",
                source_url="https://github.com/acme/small-tool",
                source_id="201",
                upvotes=60,
                comments=2,
                shares=3,
                keywords=["developer tools"],
                category="developer_tools",
            ),
            SignalIngest(
                title="acme/big-tool",
                content="A much more established developer tool.",
                source_type="github",
                source_url="https://github.com/acme/big-tool",
                source_id="202",
                upvotes=2800,
                comments=90,
                shares=400,
                keywords=["developer tools"],
                category="developer_tools",
            ),
        ]

    monkeypatch.setattr(GitHubCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=2")

    assert response.status_code == 201
    trends = {trend["title"]: trend for trend in response.json()["trends"]}
    assert trends["Small Tool"]["trend_score"] != trends["Big Tool"]["trend_score"]
    assert trends["Big Tool"]["trend_score"] > trends["Small Tool"]["trend_score"]


def test_non_english_repo_is_filtered_out(monkeypatch):
    """Regression test: a repo with a non-English description must never
    become a trend -- there's no translation step, so it would just show up
    broken to an English-only audience."""

    def fake_collect(self, query=None, limit=10):
        response_items = [
            {
                "id": 1,
                "full_name": "acme/lanhu-mcp",
                "html_url": "https://github.com/acme/lanhu-mcp",
                "description": "⚡需求分析效率提升 200%！全球首个为 AI 编程时代设计的团队协作 MCP 服务器",
                "owner": {"login": "acme"},
                "topics": ["ai", "mcp"],
                "stargazers_count": 900,
                "open_issues_count": 10,
                "forks_count": 20,
            },
            {
                "id": 2,
                "full_name": "acme/agent-runtime",
                "html_url": "https://github.com/acme/agent-runtime",
                "description": "Production runtime for deploying AI agents.",
                "owner": {"login": "acme"},
                "topics": ["ai", "agents"],
                "stargazers_count": 800,
                "open_issues_count": 12,
                "forks_count": 40,
            },
        ]
        collector = GitHubCollector(base_url="https://example.test")
        return [
            collector._repo_to_signal(repo)
            for repo in response_items
            if not collector._looks_like_reference_content(repo)
            and not looks_non_english(repo.get("description") or "")
        ]

    monkeypatch.setattr(GitHubCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=2")

    assert response.status_code == 201
    titles = [trend["title"] for trend in response.json()["trends"]]
    assert not any("lanhu" in title.lower() for title in titles)


def test_reference_content_is_filtered_out(monkeypatch):
    """Regression test: interview guides / awesome-lists / course material
    tagged "ai" must never become a trend, even though they match the
    topic:ai search -- they aren't SaaS opportunities."""

    def fake_collect(self, query=None, limit=10):
        response_items = [
            {
                "id": 1,
                "full_name": "Snailclimb/JavaGuide",
                "html_url": "https://github.com/Snailclimb/JavaGuide",
                "description": "Java interview guide covering fundamentals, databases, and AI application development.",
                "owner": {"login": "Snailclimb"},
                "topics": ["java", "interview", "guide"],
                "stargazers_count": 156000,
                "open_issues_count": 59,
                "forks_count": 900,
            },
            {
                "id": 2,
                "full_name": "acme/agent-runtime",
                "html_url": "https://github.com/acme/agent-runtime",
                "description": "Production runtime for deploying AI agents.",
                "owner": {"login": "acme"},
                "topics": ["ai", "agents"],
                "stargazers_count": 800,
                "open_issues_count": 12,
                "forks_count": 40,
            },
        ]
        collector = GitHubCollector(base_url="https://example.test")
        return [
            collector._repo_to_signal(repo)
            for repo in response_items
            if not collector._looks_like_reference_content(repo)
        ]

    monkeypatch.setattr(GitHubCollector, "collect", fake_collect)

    with TestClient(app) as client:
        response = client.post("/api/v1/ingestion/github?limit=2")

    assert response.status_code == 201
    titles = [trend["title"] for trend in response.json()["trends"]]
    assert not any("guide" in title.lower() for title in titles)
    assert response.json()["fetched_signals"] == 1
