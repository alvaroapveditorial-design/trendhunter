"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ===== USER SCHEMAS =====
class UserBase(BaseModel):
    """Base user schema."""

    email: str
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str


class UserLogin(BaseModel):
    """User login schema."""

    email: str
    password: str


class UserResponse(UserBase):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    is_verified: bool
    subscription_plan: str
    created_at: datetime


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ===== TREND SCHEMAS =====
class TrendSourceBase(BaseModel):
    """Base trend source schema."""

    source_type: str
    source_url: Optional[str] = None
    title: Optional[str] = None


class TrendSourceResponse(TrendSourceBase):
    """Trend source response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    upvotes: int = 0
    comments: int = 0
    published_at: Optional[datetime] = None


class TrendBase(BaseModel):
    """Base trend schema."""

    title: str
    description: Optional[str] = None
    category: str


class TrendCreate(TrendBase):
    """Trend creation schema."""

    slug: str
    keywords: Optional[list[str]] = None
    tags: Optional[list[str]] = None


class TrendResponse(TrendBase):
    """Trend response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    trend_score: float
    opportunity_score: float
    saturation_score: float
    momentum: float
    category: str
    keywords: list[str]
    tags: list[str]
    mentions_count: int
    engagement_count: int
    source_count: int
    is_active: bool
    is_verified: bool
    detected_at: datetime
    last_updated_at: datetime


class TrendDetailResponse(TrendResponse):
    """Detailed trend response with sources."""

    ai_insights: Optional[str] = None
    saas_opportunities: list[str] = []
    sources: list[TrendSourceResponse] = []


# ===== INGESTION SCHEMAS =====
class SignalIngest(BaseModel):
    """Public signal submitted to the MVP trend detector."""

    title: str = Field(min_length=3, max_length=180)
    content: Optional[str] = Field(default=None, max_length=2000)
    source_type: str = Field(default="manual", min_length=2, max_length=40)
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    author: Optional[str] = None
    upvotes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    category: Optional[str] = None
    keywords: list[str] = []
    published_at: Optional[datetime] = None


class SignalBatchIngest(BaseModel):
    """Batch of signals to analyze."""

    signals: list[SignalIngest] = Field(min_length=1, max_length=50)


class IngestionRunResponse(BaseModel):
    """Summary returned after an ingestion run."""

    processed_signals: int
    created_trends: int
    updated_trends: int
    trend_ids: list[str]
    trends: list[TrendResponse]


class SourceIngestionResponse(IngestionRunResponse):
    """Ingestion response enriched with source collection details."""

    source_type: str
    fetched_signals: int
    skipped_signals: int = 0


class AgentExecutionResponse(BaseModel):
    """Agent/workflow execution log response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    agent_name: str
    agent_type: str
    status: str
    records_processed: int
    records_created: int
    records_updated: int
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None


# ===== ALERT SCHEMAS =====
class AlertBase(BaseModel):
    """Base alert schema."""

    name: str
    keywords: list[str]
    categories: Optional[list[str]] = None
    min_score: float = Field(default=50.0, ge=0, le=100)


class AlertCreate(AlertBase):
    """Alert creation schema."""

    notification_channel: str = "email"
    notify_frequency: str = "instant"


class AlertResponse(AlertBase):
    """Alert response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    is_active: bool
    created_at: datetime
    last_triggered_at: Optional[datetime] = None


# ===== SEARCH SCHEMAS =====
class TrendSearchQuery(BaseModel):
    """Trend search query schema."""

    q: Optional[str] = None
    category: Optional[str] = None
    min_score: float = Field(default=0, ge=0, le=100)
    max_score: float = Field(default=100, ge=0, le=100)
    sort_by: str = Field(default="trend_score", pattern="^(trend_score|detected_at|momentum)$")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Paginated response schema."""

    total: int
    skip: int
    limit: int
    items: list


# ===== REPORT SCHEMAS =====
class ReportBase(BaseModel):
    """Base report schema."""

    title: str
    report_type: str


class ReportCreate(ReportBase):
    """Report creation schema."""

    pass


class ReportResponse(ReportBase):
    """Report response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
