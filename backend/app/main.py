"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import auth, beta, billing, ingestion, support, trends
from app.core.config import get_settings
from app.core.rate_limit import InMemoryRateLimiter
from app.models.base import Base
from app.models.database import engine
from app.services.seed import seed_database

settings = get_settings()

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

if settings.SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
    )
    logger.info("Sentry error tracking enabled")
rate_limiter = InMemoryRateLimiter(
    max_requests=settings.RATE_LIMIT_REQUESTS,
    period_seconds=settings.RATE_LIMIT_PERIOD,
)
RATE_LIMITED_PREFIXES = ("/api/v1/ingestion", "/api/v1/trends")
# Billing writes are rate limited individually, not by prefix, so that
# /api/v1/billing/webhook (called by Stripe's own servers, potentially in
# bursts after any downtime) is never throttled.
RATE_LIMITED_PATHS = {"/api/v1/billing/checkout", "/api/v1/billing/portal", "/api/v1/support/contact"}

auth_code_rate_limiter = InMemoryRateLimiter(
    max_requests=settings.AUTH_CODE_RATE_LIMIT_REQUESTS,
    period_seconds=settings.AUTH_CODE_RATE_LIMIT_PERIOD,
)
AUTH_CODE_RATE_LIMITED_PATH = "/api/v1/auth/request-code"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    if settings.AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)
    logger.info(f"Starting AI Trend Hunter API (env: {settings.ENVIRONMENT})")
    logger.info(f"Debug mode: {settings.DEBUG}")
    seed_database()
    yield
    logger.info("Shutting down AI Trend Hunter API")


# Initialize FastAPI app
app = FastAPI(
    title="AI Trend Hunter API",
    description="AI-powered trend detection platform for early-stage opportunity discovery",
    version="0.1.0",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    # docs_url/redoc_url only hide the UI pages -- the raw schema stays served
    # at /openapi.json unless it is disabled too, exposing the full API surface.
    openapi_url=None if settings.is_production else "/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Request-ID"],
)


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    """Rate limit ingestion writes and login code requests for the MVP."""
    is_write = request.method not in {"GET", "HEAD", "OPTIONS"}
    if not settings.RATE_LIMIT_ENABLED or not is_write:
        return await call_next(request)

    if request.url.path == AUTH_CODE_RATE_LIMITED_PATH:
        limiter, limit = auth_code_rate_limiter, settings.AUTH_CODE_RATE_LIMIT_REQUESTS
    elif request.url.path in RATE_LIMITED_PATHS or request.url.path.startswith(RATE_LIMITED_PREFIXES):
        limiter, limit = rate_limiter, settings.RATE_LIMIT_REQUESTS
    else:
        return await call_next(request)

    forwarded_for = request.headers.get("x-forwarded-for")
    client_host = forwarded_for.split(",")[0].strip() if forwarded_for else None
    if not client_host and request.client:
        client_host = request.client.host
    key = f"{client_host or 'unknown'}:{request.url.path}"
    decision = limiter.check(key)

    if not decision.allowed:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Try again later.",
                "retry_after": decision.retry_after,
            },
            headers={
                "Retry-After": str(decision.retry_after),
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
            },
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(decision.remaining)
    return response


@app.middleware("http")
async def security_headers_middleware(request, call_next):
    """Attach baseline security headers to every response."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


# ===== HEALTH CHECK =====
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
    }


@app.get("/", tags=["Root"])
def root():
    """Root endpoint."""
    return {
        "name": "AI Trend Hunter API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }

# ===== FUTURE API ROUTES (to be implemented) =====
# Import and include routers here as they're created:
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
# app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(trends.router, prefix="/api/v1/trends", tags=["Trends"])
app.include_router(ingestion.router, prefix="/api/v1/ingestion", tags=["Ingestion"])
app.include_router(beta.router, prefix="/api/v1/beta", tags=["Beta"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["Billing"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(support.router, prefix="/api/v1/support", tags=["Support"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
