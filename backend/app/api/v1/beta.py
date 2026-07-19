"""Public beta signup API endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.base import BetaSignup
from app.models.database import get_db
from app.schemas.schemas import BetaSignupCreate, BetaSignupResponse

router = APIRouter()


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
