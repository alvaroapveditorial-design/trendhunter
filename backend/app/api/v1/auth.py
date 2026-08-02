"""Email code authentication and subscription paywall helpers."""

import random
from datetime import timedelta
from uuid import uuid4

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    decode_token,
    hash_login_code,
    verify_login_code_hash,
)
from app.models.base import LoginCode, Subscription, _utcnow
from app.models.database import get_db
from app.schemas.schemas import (
    AuthSessionResponse,
    LoginCodeRequest,
    LoginCodeResponse,
    LoginVerifyRequest,
)
from app.services.email_service import send_login_code_email
from app.services.plausible_events import send_plausible_event

router = APIRouter()
settings = get_settings()
SESSION_COOKIE_NAME = "trendhunter_session"
ACTIVE_SUBSCRIPTION_STATUSES = {"active", "trialing"}


def _active_subscription_for_email(db: Session, email: str) -> Subscription | None:
    return (
        db.query(Subscription)
        .filter(
            Subscription.email == email,
            Subscription.status.in_(ACTIVE_SUBSCRIPTION_STATUSES),
        )
        .order_by(Subscription.created_at.desc())
        .first()
    )


def _session_response(email: str, db: Session) -> AuthSessionResponse:
    subscription = _active_subscription_for_email(db, email)
    latest_subscription = (
        db.query(Subscription)
        .filter(Subscription.email == email)
        .order_by(Subscription.created_at.desc())
        .first()
    )
    return AuthSessionResponse(
        email=email,
        subscription_status=latest_subscription.status if latest_subscription else None,
        has_active_subscription=subscription is not None,
    )


@router.post("/request-code", response_model=LoginCodeResponse)
def request_login_code(payload: LoginCodeRequest, db: Session = Depends(get_db)):
    """Create a short-lived login code for an email address."""
    code = f"{random.SystemRandom().randint(0, 999999):06d}"
    login_code = LoginCode(
        id=str(uuid4()),
        email=payload.email,
        code_hash=hash_login_code(payload.email, code),
        expires_at=_utcnow() + timedelta(minutes=10),
    )
    db.add(login_code)
    db.commit()
    sent = send_login_code_email(payload.email, code)
    send_plausible_event("Login Code Requested", path="/login")

    # Returning the code only in non-production keeps local testing friction low
    # without exposing codes in deployed environments.
    return LoginCodeResponse(ok=sent or not settings.is_production, code=None if settings.is_production else code)


@router.post("/verify-code", response_model=AuthSessionResponse)
def verify_login_code(
    payload: LoginVerifyRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """Verify a login code and issue a session cookie."""
    now = _utcnow()
    candidates = (
        db.query(LoginCode)
        .filter(
            LoginCode.email == payload.email,
            LoginCode.consumed_at.is_(None),
            LoginCode.expires_at > now,
        )
        .order_by(LoginCode.created_at.desc())
        .limit(5)
        .all()
    )
    login_code = next(
        (
            candidate
            for candidate in candidates
            if verify_login_code_hash(payload.email, payload.code, candidate.code_hash)
        ),
        None,
    )
    if not login_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired login code.",
        )

    login_code.consumed_at = now
    db.commit()

    token = create_access_token(
        {"sub": payload.email},
        expires_delta=timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES),
    )
    response.set_cookie(
        SESSION_COOKIE_NAME,
        token,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        max_age=settings.SESSION_TIMEOUT_MINUTES * 60,
        path="/",
    )
    return _session_response(payload.email, db)


@router.post("/logout")
def logout(response: Response):
    """Clear the browser session cookie."""
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me", response_model=AuthSessionResponse)
def current_session(
    trendhunter_session: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    db: Session = Depends(get_db),
):
    """Return current authenticated user and subscription state."""
    if not trendhunter_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    payload = decode_token(trendhunter_session)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session.")
    return _session_response(email, db)
