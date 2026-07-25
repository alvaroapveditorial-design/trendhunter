"""Server-side Plausible custom events (Plausible Events API).

Used for conversion events that happen inside a Stripe webhook, where there
is no browser to fire a client-side Plausible event from -- mirrors the
pattern already used for Meta's Conversions API in meta_capi.py.
"""

import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

PLAUSIBLE_EVENTS_URL = "https://plausible.io/api/event"


def send_plausible_event(
    event_name: str,
    *,
    path: str,
    props: dict | None = None,
) -> bool:
    """Send a server-side Plausible custom event. Never raises."""
    if not settings.ANALYTICS_ENABLED or not settings.PLAUSIBLE_DOMAIN:
        return False

    payload = {
        "name": event_name,
        "url": f"{settings.APP_URL.rstrip('/')}{path}",
        "domain": settings.PLAUSIBLE_DOMAIN,
    }
    if props:
        payload["props"] = props

    try:
        with httpx.Client(timeout=5) as client:
            response = client.post(
                PLAUSIBLE_EVENTS_URL,
                json=payload,
                headers={"User-Agent": "AI-Trend-Hunter-Backend/1.0"},
            )
    except httpx.HTTPError:
        logger.warning("Plausible event %s failed to send", event_name, exc_info=True)
        return False

    if response.status_code >= 400:
        logger.warning(
            "Plausible event %s failed with status %s: %s",
            event_name,
            response.status_code,
            response.text,
        )
        return False
    return True
