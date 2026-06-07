"""Hacker News collector for public trend signals."""

from datetime import datetime, timezone
from html import unescape
import re
from typing import Any

import httpx

from app.core.config import get_settings
from app.schemas.schemas import SignalIngest

MAX_SIGNAL_CONTENT_LENGTH = 2000


class HackerNewsCollector:
    """Collect public Hacker News stories and map them to trend signals."""

    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        settings = get_settings()
        self.base_url = (base_url or settings.HACKERNEWS_API_URL).rstrip("/")
        self.timeout = timeout

    def collect(self, feed: str = "top", limit: int | None = None) -> list[SignalIngest]:
        """Collect story signals from a Hacker News feed."""
        settings = get_settings()
        normalized_feed = self._normalize_feed(feed)
        max_items = limit or settings.HACKERNEWS_DEFAULT_LIMIT

        with httpx.Client(timeout=self.timeout) as client:
            ids_response = client.get(f"{self.base_url}/{normalized_feed}stories.json")
            ids_response.raise_for_status()
            story_ids = ids_response.json()[:max_items]

            signals = []
            for story_id in story_ids:
                item_response = client.get(f"{self.base_url}/item/{story_id}.json")
                item_response.raise_for_status()
                item = item_response.json()
                signal = self._item_to_signal(item)
                if signal:
                    signals.append(signal)

        return signals

    def _normalize_feed(self, feed: str) -> str:
        if feed not in {"top", "new", "best", "ask", "show", "job"}:
            return "top"
        return feed

    def _item_to_signal(self, item: dict[str, Any] | None) -> SignalIngest | None:
        if not item or item.get("deleted") or item.get("dead"):
            return None

        title = item.get("title")
        if not title:
            return None

        published_at = None
        if item.get("time"):
            published_at = datetime.fromtimestamp(item["time"], tz=timezone.utc).replace(tzinfo=None)

        story_url = item.get("url") or f"https://news.ycombinator.com/item?id={item.get('id')}"
        comments = int(item.get("descendants") or 0)
        score = int(item.get("score") or 0)
        keywords = self._keywords_from_title(title)

        return SignalIngest(
            title=title,
            content=self._clean_content(item.get("text")),
            source_type="hackernews",
            source_url=story_url,
            source_id=str(item.get("id")),
            author=item.get("by"),
            upvotes=score,
            comments=comments,
            shares=0,
            category=None,
            keywords=keywords,
            published_at=published_at,
        )

    def _clean_content(self, content: str | None) -> str | None:
        if not content:
            return None

        cleaned = re.sub(r"<[^>]+>", " ", unescape(content))
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if len(cleaned) <= MAX_SIGNAL_CONTENT_LENGTH:
            return cleaned
        return cleaned[:MAX_SIGNAL_CONTENT_LENGTH].rstrip()

    def _keywords_from_title(self, title: str) -> list[str]:
        lowered = title.lower()
        keywords = []
        if any(term in lowered for term in ["ai", "llm", "agent", "copilot"]):
            keywords.append("ai")
        if any(term in lowered for term in ["privacy", "gdpr", "tracking"]):
            keywords.append("privacy")
        if any(term in lowered for term in ["api", "github", "python", "javascript", "database"]):
            keywords.append("developer tools")
        if any(term in lowered for term in ["startup", "saas", "founder"]):
            keywords.append("saas")
        return keywords
