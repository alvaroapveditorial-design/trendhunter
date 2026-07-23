"""Public beta signup API endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.base import BetaSignup
from app.models.database import get_db
from app.schemas.schemas import BetaSignupCreate, BetaSignupResponse

router = APIRouter()


def require_admin_key(x_admin_key: str | None = Header(default=None)) -> None:
    """Require the admin shared secret. Fails closed: unset key means no access."""
    expected_key = get_settings().ADMIN_API_KEY
    if not expected_key or x_admin_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin key required.",
        )


@router.post("/signups", response_model=BetaSignupResponse, status_code=status.HTTP_201_CREATED)
def create_beta_signup(payload: BetaSignupCreate, db: Session = Depends(get_db)):
    """Capture or return a private beta signup from the public landing."""
    existing = db.query(BetaSignup).filter(BetaSignup.email == payload.email).first()
    if existing:
        response = BetaSignupResponse.model_validate(existing)
        response.already_registered = True
        return response

    signup = BetaSignup(
        id=str(uuid4()),
        email=payload.email,
        role=payload.role,
        interests=payload.interests,
    )
    db.add(signup)
    db.commit()
    db.refresh(signup)
    return signup


@router.get(
    "/signups",
    response_model=list[BetaSignupResponse],
    dependencies=[Depends(require_admin_key)],
)
def list_beta_signups(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """List beta signups for operators, newest first. Requires X-Admin-Key."""
    return (
        db.query(BetaSignup)
        .order_by(BetaSignup.created_at.desc())
        .limit(limit)
        .all()
    )
