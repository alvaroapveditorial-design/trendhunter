"""Meta Conversions API (server-side) event tracking."""

import hashlib
import logging
import time

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _hash(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()


def send_capi_event(
    event_name: str,
    *,
    email: str | None,
    event_id: str,
    event_source_url: str,
    custom_data: dict | None = None,
) -> bool:
    """Send a server-side conversion event to Meta. Never raises; logs and returns False on failure."""
    if not settings.META_PIXEL_ID or not settings.META_CAPI_ACCESS_TOKEN:
        logger.info("Meta CAPI not configured, skipping %s event", event_name)
        return False

    user_data = {}
    if email:
        user_data["em"] = [_hash(email)]

    payload = {
        "data": [
            {
                "event_name": event_name,
                "event_time": int(time.time()),
                "event_id": event_id,
                "action_source": "website",
                "event_source_url": event_source_url,
                "user_data": user_data,
                "custom_data": custom_data or {},
            }
        ],
    }

    url = f"{settings.META_GRAPH_API_URL.rstrip('/')}/{settings.META_PIXEL_ID}/events"

    with httpx.Client(timeout=10) as client:
        response = client.post(
            url,
            params={"access_token": settings.META_CAPI_ACCESS_TOKEN},
            json=payload,
        )

    if response.status_code >= 400:
        logger.error("Meta CAPI %s event failed with status %s: %s", event_name, response.status_code, response.text)
        return False
    return True
