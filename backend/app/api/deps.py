"""Shared FastAPI dependencies for authentication and service-to-service auth."""

from fastapi import Cookie, Header, HTTPException, status

from app.core.config import get_settings
from app.core.security import decode_token

SESSION_COOKIE_NAME = "trendhunter_session"


def require_session_email(
    trendhunter_session: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> str:
    """Resolve the authenticated user's email from the signed session cookie.

    Used anywhere an endpoint must act on "the current user", never on an
    email supplied by the client body -- that pattern is how an attacker can
    request another customer's Stripe billing portal by guessing their email.
    """
    if not trendhunter_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    payload = decode_token(trendhunter_session)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session.")
    return email


def require_ingestion_key(x_ingestion_key: str | None = Header(default=None)) -> None:
    """Require a shared secret for ingestion mutations when configured."""
    expected_key = get_settings().INGESTION_API_KEY
    if expected_key and x_ingestion_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ingestion key required.",
        )


def require_internal_key(x_internal_key: str | None = Header(default=None)) -> None:
    """Require the shared backend-internal secret when configured.

    Fails open (allows the request) while BACKEND_INTERNAL_KEY is unset, so
    this can be rolled out safely: set the variable on both services once
    the header is wired up on the caller side, and it starts enforcing.
    """
    expected_key = get_settings().BACKEND_INTERNAL_KEY
    if expected_key and x_internal_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Internal key required.",
        )
