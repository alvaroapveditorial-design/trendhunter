"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import ingestion, trends
from app.core.config import get_settings
from app.core.rate_limit import InMemoryRateLimiter
from app.models.base import Base
from app.models.database import engine
from app.services.seed import seed_database

settings = get_settings()

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)
rate_limiter = InMemoryRateLimiter(
    max_requests=settings.RATE_LIMIT_REQUESTS,
    period_seconds=settings.RATE_LIMIT_PERIOD,
)
RATE_LIMITED_PREFIXES = ("/api/v1/ingestion",)

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
    """Rate limit ingestion writes for the MVP."""
    should_limit = (
        settings.RATE_LIMIT_ENABLED
        and request.method not in {"GET", "HEAD", "OPTIONS"}
        and request.url.path.startswith(RATE_LIMITED_PREFIXES)
    )

    if should_limit:
        forwarded_for = request.headers.get("x-forwarded-for")
        client_host = forwarded_for.split(",")[0].strip() if forwarded_for else None
        if not client_host and request.client:
            client_host = request.client.host
        key = f"{client_host or 'unknown'}:{request.url.path}"
        decision = rate_limiter.check(key)

        if not decision.allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Try again later.",
                    "retry_after": decision.retry_after,
                },
                headers={
                    "Retry-After": str(decision.retry_after),
                    "X-RateLimit-Limit": str(settings.RATE_LIMIT_REQUESTS),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(decision.remaining)
        return response

    return await call_next(request)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
