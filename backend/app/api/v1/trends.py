"""Trend API endpoints for the MVP."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.schemas import TrendCreate, TrendDetailResponse, TrendResponse
from app.services.trend_service import TrendService

router = APIRouter()


@router.get("", response_model=list[TrendResponse])
def list_trends(
    q: str | None = Query(default=None, description="Search in title, description, or keywords"),
    category: str | None = Query(default=None),
    source_type: str | None = Query(default=None, min_length=2, max_length=40),
    min_score: float = Query(default=0, ge=0, le=100),
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0, description="Number of results to skip for pagination"),
    db: Session = Depends(get_db),
):
    """List detected trends ordered by trend score."""
    return TrendService(db).list_trends(
        q=q,
        category=category,
        source_type=source_type,
        min_score=min_score,
        limit=limit,
        skip=skip,
    )


@router.get("/meta/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    """List categories available in the database."""
    return TrendService(db).list_categories()


@router.get("/meta/sources", response_model=list[str])
def list_sources(db: Session = Depends(get_db)):
    """List source types available in the database."""
    return TrendService(db).list_sources()


@router.get("/{trend_id_or_slug}", response_model=TrendDetailResponse)
def get_trend(trend_id_or_slug: str, db: Session = Depends(get_db)):
    """Get one trend by id or slug."""
    trend = TrendService(db).get_trend(trend_id_or_slug)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found",
        )
    return trend


@router.post("", response_model=TrendResponse, status_code=status.HTTP_201_CREATED)
def create_trend(payload: TrendCreate, db: Session = Depends(get_db)):
    """Create a trend manually."""
    return TrendService(db).create_trend(payload)
