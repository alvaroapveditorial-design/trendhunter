"""GitHub repository collector for public trend signals."""

from datetime import datetime, timezone
from typing import Any

import httpx

from app.core.config import get_settings
from app.schemas.schemas import SignalIngest


class GitHubCollector:
    """Collect public GitHub repositories and map them to trend signals."""

    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        settings = get_settings()
        self.base_url = (base_url or settings.GITHUB_API_URL).rstrip("/")
        self.timeout = timeout

    def collect(self, query: str | None = None, limit: int | None = None) -> list[SignalIngest]:
        """Collect repository signals from GitHub search."""
        settings = get_settings()
        search_query = query or settings.GITHUB_SEARCH_QUERY
        max_items = limit or settings.GITHUB_DEFAULT_LIMIT
        headers = {"Accept": "application/vnd.github+json"}
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        with httpx.Client(timeout=self.timeout, headers=headers) as client:
            response = client.get(
                f"{self.base_url}/search/repositories",
                params={
                    "q": search_query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": max_items,
                },
            )
            response.raise_for_status()
            payload = response.json()

        return [self._repo_to_signal(repo) for repo in payload.get("items", [])[:max_items]]

    def _repo_to_signal(self, repo: dict[str, Any]) -> SignalIngest:
        name = repo.get("full_name") or repo.get("name") or "unknown/repository"
        description = repo.get("description") or f"Public GitHub repository: {name}"
        topics = [str(topic).lower() for topic in repo.get("topics") or [] if topic]
        language = (repo.get("language") or "").lower()
        keywords = self._keywords(name, description, topics, language)
        pushed_at = self._parse_datetime(repo.get("pushed_at") or repo.get("updated_at"))

        return SignalIngest(
            title=name,
            content=description,
            source_type="github",
            source_url=repo.get("html_url"),
            source_id=str(repo.get("id") or name),
            author=(repo.get("owner") or {}).get("login"),
            upvotes=int(repo.get("stargazers_count") or 0),
            comments=int(repo.get("open_issues_count") or 0),
            shares=int(repo.get("forks_count") or 0),
            category=self._category(keywords),
            keywords=keywords,
            published_at=pushed_at,
        )

    def _parse_datetime(self, value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed.astimezone(timezone.utc).replace(tzinfo=None)

    def _keywords(self, name: str, description: str, topics: list[str], language: str) -> list[str]:
        lowered = f"{name} {description} {' '.join(topics)} {language}".lower()
        keywords = list(topics[:5])
        if language:
            keywords.append(language)
        if any(term in lowered for term in ["ai", "llm", "agent", "copilot", "openai"]):
            keywords.append("ai")
        if any(term in lowered for term in ["api", "sdk", "developer", "database", "github"]):
            keywords.append("developer tools")
        if any(term in lowered for term in ["saas", "startup", "founder"]):
            keywords.append("startup")
        return sorted(set(keyword for keyword in keywords if keyword))[:8]

    def _category(self, keywords: list[str]) -> str:
        keyword_set = set(" ".join(keywords).split())
        if {"ai", "llm", "agent", "copilot"}.intersection(keyword_set):
            return "ai_saas"
        return "developer_tools"
