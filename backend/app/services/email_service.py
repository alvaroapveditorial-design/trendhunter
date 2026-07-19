"""Transactional email helpers."""

import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def send_login_code_email(email: str, code: str) -> bool:
    """Send a login code email through Resend when configured."""
    if not settings.RESEND_API_KEY:
        logger.info("Login code for %s: %s", email, code)
        return False

    payload = {
        "from": settings.SENDER_EMAIL,
        "to": [email],
        "subject": "Tu codigo de acceso a AI Trend Hunter",
        "text": (
            "Tu codigo de acceso a AI Trend Hunter es "
            f"{code}. Caduca en 10 minutos. Si no lo has solicitado, ignora este email."
        ),
    }

    with httpx.Client(timeout=10) as client:
        response = client.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    if response.status_code >= 400:
        logger.error("Resend failed with status %s: %s", response.status_code, response.text)
        return False
    return True
