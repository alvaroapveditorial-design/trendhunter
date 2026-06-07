"""Signal ingestion API for the MVP detector."""

from xml.etree import ElementTree

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.base import AgentExecution
from app.models.database import get_db
from app.schemas.schemas import (
    AgentExecutionResponse,
    IngestionRunResponse,
    SignalBatchIngest,
    SourceIngestionResponse,
)
from app.services.detector_service import DetectorService
from app.services.github_collector import GitHubCollector
from app.services.hackernews_collector import HackerNewsCollector
from app.services.rss_collector import RSSCollector

router = APIRouter()


@router.get("/runs", response_model=list[AgentExecutionResponse])
def list_ingestion_runs(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """List recent detector and ingestion runs."""
    return (
        db.query(AgentExecution)
        .order_by(AgentExecution.started_at.desc())
        .limit(limit)
        .all()
    )


@router.post("/signals", response_model=IngestionRunResponse, status_code=status.HTTP_201_CREATED)
def ingest_signals(payload: SignalBatchIngest, db: Session = Depends(get_db)):
    """Analyze raw public signals and create or update trends."""
    return DetectorService(db).ingest_batch(payload)


@router.post("/demo", response_model=IngestionRunResponse, status_code=status.HTTP_201_CREATED)
def run_demo_ingestion(db: Session = Depends(get_db)):
    """Run a deterministic demo ingestion batch."""
    return DetectorService(db).run_demo()


@router.post("/hackernews", response_model=SourceIngestionResponse, status_code=status.HTTP_201_CREATED)
def ingest_hackernews(
    feed: str = Query(default="top", pattern="^(top|new|best|ask|show|job)$"),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Collect public Hacker News stories and analyze them as trend signals."""
    try:
        signals = HackerNewsCollector().collect(feed=feed, limit=limit)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not fetch Hacker News stories. Try again later.",
        ) from exc

    if not signals:
        return SourceIngestionResponse(
            processed_signals=0,
            created_trends=0,
            updated_trends=0,
            trend_ids=[],
            trends=[],
            source_type="hackernews",
            fetched_signals=0,
            skipped_signals=limit,
        )

    result = DetectorService(db).ingest_batch(SignalBatchIngest(signals=signals))
    return SourceIngestionResponse(
        **result.model_dump(),
        source_type="hackernews",
        fetched_signals=len(signals),
        skipped_signals=max(0, limit - len(signals)),
    )


@router.get("/rss/feeds", response_model=list[str])
def list_rss_feeds():
    """List configured public RSS feeds."""
    return RSSCollector().available_feeds()


@router.post("/rss", response_model=SourceIngestionResponse, status_code=status.HTTP_201_CREATED)
def ingest_rss(
    feed: str | None = Query(default=None, min_length=2, max_length=80),
    limit: int = Query(default=10, ge=1, le=30),
    db: Session = Depends(get_db),
):
    """Collect public RSS/Atom feed items and analyze them as trend signals."""
    try:
        signals = RSSCollector().collect(feed=feed, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except (httpx.HTTPError, ElementTree.ParseError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not fetch RSS feed. Try again later.",
        ) from exc

    if not signals:
        return SourceIngestionResponse(
            processed_signals=0,
            created_trends=0,
            updated_trends=0,
            trend_ids=[],
            trends=[],
            source_type="rss",
            fetched_signals=0,
            skipped_signals=limit,
        )

    result = DetectorService(db).ingest_batch(SignalBatchIngest(signals=signals))
    return SourceIngestionResponse(
        **result.model_dump(),
        source_type="rss",
        fetched_signals=len(signals),
        skipped_signals=max(0, limit - len(signals)),
    )


@router.post("/github", response_model=SourceIngestionResponse, status_code=status.HTTP_201_CREATED)
def ingest_github(
    q: str | None = Query(default=None, min_length=2, max_length=160),
    limit: int = Query(default=10, ge=1, le=30),
    db: Session = Depends(get_db),
):
    """Collect public GitHub repositories and analyze them as trend signals."""
    try:
        signals = GitHubCollector().collect(query=q, limit=limit)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not fetch GitHub repositories. Try again later.",
        ) from exc

    if not signals:
        return SourceIngestionResponse(
            processed_signals=0,
            created_trends=0,
            updated_trends=0,
            trend_ids=[],
            trends=[],
            source_type="github",
            fetched_signals=0,
            skipped_signals=limit,
        )

    result = DetectorService(db).ingest_batch(SignalBatchIngest(signals=signals))
    return SourceIngestionResponse(
        **result.model_dump(),
        source_type="github",
        fetched_signals=len(signals),
        skipped_signals=max(0, limit - len(signals)),
    )
