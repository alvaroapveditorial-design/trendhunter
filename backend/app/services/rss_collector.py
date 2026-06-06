"""RSS/Atom collector for public trend signals."""

import html
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

import httpx

from app.core.config import get_settings
from app.schemas.schemas import SignalIngest

FEED_KEYWORDS = {
    "hn_frontpage": "hacker news",
    "producthunt": "product hunt",
    "techcrunch_startups": "startup news",
}


class RSSCollector:
    """Collect RSS or Atom feed entries and map them to trend signals."""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def collect(self, feed: str | None = None, limit: int = 10) -> list[SignalIngest]:
        """Collect signals from one configured RSS feed."""
        settings = get_settings()
        feeds = settings.rss_feeds
        feed_key = feed or settings.RSS_DEFAULT_FEED
        feed_url = feeds.get(feed_key)
        if not feed_url:
            raise ValueError(f"Unknown RSS feed: {feed_key}")

        with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
            response = client.get(feed_url)
            response.raise_for_status()

        return self._parse(response.text, feed_key=feed_key, feed_url=feed_url, limit=limit)

    def available_feeds(self) -> list[str]:
        """Return configured RSS feed keys."""
        return sorted(get_settings().rss_feeds)

    def _parse(self, xml_text: str, feed_key: str, feed_url: str, limit: int) -> list[SignalIngest]:
        root = ElementTree.fromstring(xml_text)
        items = root.findall(".//item")
        if not items:
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

        signals = []
        for item in items[:limit]:
            signal = self._item_to_signal(item, feed_key=feed_key, feed_url=feed_url)
            if signal:
                signals.append(signal)
        return signals

    def _item_to_signal(self, item: ElementTree.Element, feed_key: str, feed_url: str) -> SignalIngest | None:
        title = self._text(item, "title")
        if not title:
            return None

        link = self._link(item) or feed_url
        summary = (
            self._text(item, "description")
            or self._text(item, "summary")
            or self._text(item, "content")
            or title
        )
        published_at = self._published_at(item)
        clean_title = self._clean(title)[:180]
        clean_summary = self._clean(summary)

        return SignalIngest(
            title=clean_title,
            content=clean_summary,
            source_type="rss",
            source_url=link,
            source_id=link,
            author=self._text(item, "creator") or self._text(item, "author"),
            upvotes=self._estimated_upvotes(published_at),
            comments=0,
            shares=3,
            category=self._category(clean_title, clean_summary),
            keywords=self._keywords(clean_title, clean_summary, feed_key),
            published_at=published_at,
        )

    def _text(self, item: ElementTree.Element, tag: str) -> str | None:
        found = item.find(tag)
        if found is None:
            found = item.find(f"{{http://www.w3.org/2005/Atom}}{tag}")
        if found is None:
            found = item.find(f"{{http://purl.org/dc/elements/1.1/}}{tag}")
        if found is None or found.text is None:
            return None
        return found.text.strip()

    def _link(self, item: ElementTree.Element) -> str | None:
        link = self._text(item, "link")
        if link:
            return link
        atom_link = item.find("{http://www.w3.org/2005/Atom}link")
        if atom_link is not None:
            return atom_link.attrib.get("href")
        return None

    def _published_at(self, item: ElementTree.Element) -> datetime | None:
        raw = self._text(item, "pubDate") or self._text(item, "published") or self._text(item, "updated")
        if not raw:
            return None
        try:
            parsed = parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            try:
                parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError:
                return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).replace(tzinfo=None)

    def _clean(self, value: str) -> str:
        without_tags = re.sub(r"<[^>]+>", " ", value)
        normalized = re.sub(r"\s+", " ", html.unescape(without_tags)).strip()
        return normalized[:1800]

    def _keywords(self, title: str, content: str, feed_key: str) -> list[str]:
        lowered = f"{title} {content}".lower()
        keywords = []
        if any(term in lowered for term in ["ai", "llm", "agent", "copilot"]):
            keywords.append("ai")
        if any(term in lowered for term in ["startup", "founder", "saas"]):
            keywords.append("startup")
        if any(term in lowered for term in ["funding", "venture", "investor", "raise", "seed"]):
            keywords.append("funding")
        if any(term in lowered for term in ["privacy", "gdpr", "tracking"]):
            keywords.append("privacy")
        if any(term in lowered for term in ["api", "github", "developer", "database"]):
            keywords.append("developer tools")
        if any(term in lowered for term in ["product", "launch", "app", "platform"]):
            keywords.append("product")
        keywords.append(FEED_KEYWORDS.get(feed_key, feed_key.replace("_", " ")))
        return sorted(set(keywords))[:6]

    def _category(self, title: str, content: str) -> str:
        lowered = f"{title} {content}".lower()
        if any(term in lowered for term in ["ai", "llm", "agent", "copilot", "automation"]):
            return "ai_saas"
        if any(term in lowered for term in ["api", "github", "developer", "database"]):
            return "developer_tools"
        if any(term in lowered for term in ["privacy", "gdpr", "tracking"]):
            return "privacy"
        if any(term in lowered for term in ["startup", "founder", "funding", "venture", "seed"]):
            return "startups"
        if any(term in lowered for term in ["product", "launch", "app", "platform"]):
            return "product"
        return "emerging"

    def _estimated_upvotes(self, published_at: datetime | None) -> int:
        if not published_at:
            return 24
        age_hours = (datetime.now(timezone.utc).replace(tzinfo=None) - published_at).total_seconds() / 3600
        if age_hours <= 24:
            return 48
        if age_hours <= 72:
            return 36
        return 24
