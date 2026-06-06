"""Application constants."""

# ===== TREND SCORING =====
TREND_SCORE_MIN = 0
TREND_SCORE_MAX = 100
OPPORTUNITY_SCORE_MIN = 0
OPPORTUNITY_SCORE_MAX = 100
SATURATION_SCORE_MIN = 0
SATURATION_SCORE_MAX = 100

# ===== TREND CATEGORIES =====
TREND_CATEGORIES = {
    "technology": "🔬 Technology",
    "ai_ml": "🤖 AI & Machine Learning",
    "web3": "⛓️ Web3 & Blockchain",
    "startup": "🚀 Startup Ideas",
    "content": "📝 Content & Creator",
    "saas": "💼 SaaS Opportunities",
    "marketing": "📢 Marketing & Growth",
    "ecommerce": "🛍️ E-Commerce",
    "health": "⚕️ Health & Wellness",
    "finance": "💰 Finance & Trading",
    "gaming": "🎮 Gaming",
    "education": "📚 Education",
    "social": "👥 Social & Community",
}

# ===== TREND SOURCES =====
TREND_SOURCES = {
    "reddit": "Reddit",
    "github": "GitHub",
    "hackernews": "Hacker News",
    "producthunt": "Product Hunt",
    "youtube": "YouTube",
    "twitter": "Twitter/X",
    "news": "News APIs",
    "rss": "RSS Feeds",
}

# ===== AGENT STATUSES =====
AGENT_STATUS_PENDING = "pending"
AGENT_STATUS_RUNNING = "running"
AGENT_STATUS_SUCCESS = "success"
AGENT_STATUS_FAILED = "failed"
AGENT_STATUS_TIMEOUT = "timeout"

AGENT_STATUSES = [
    AGENT_STATUS_PENDING,
    AGENT_STATUS_RUNNING,
    AGENT_STATUS_SUCCESS,
    AGENT_STATUS_FAILED,
    AGENT_STATUS_TIMEOUT,
]

# ===== USER ROLES =====
USER_ROLE_ADMIN = "admin"
USER_ROLE_USER = "user"
USER_ROLE_VIEWER = "viewer"

# ===== SUBSCRIPTION PLANS =====
SUBSCRIPTION_FREE = "free"
SUBSCRIPTION_PRO = "pro"
SUBSCRIPTION_ENTERPRISE = "enterprise"

SUBSCRIPTION_PLANS = [SUBSCRIPTION_FREE, SUBSCRIPTION_PRO, SUBSCRIPTION_ENTERPRISE]

# ===== PAGINATION =====
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ===== API RATE LIMITS =====
RATE_LIMIT_ANONYMOUS = "100/hour"
RATE_LIMIT_USER = "1000/hour"
RATE_LIMIT_PREMIUM = "10000/hour"

# ===== DATA RETENTION =====
# Default retention periods in days
DEFAULT_RETENTION_DAYS = 90
LOG_RETENTION_DAYS = 30
