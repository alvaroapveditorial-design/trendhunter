# Backend Configuration & Setup

## Installation

### Local Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server.
# Uses SQLite by default and seeds demo trends on first startup.
uvicorn app.main:app --reload --port 8000
```

### MVP Endpoints

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/trends
curl http://localhost:8000/api/v1/trends/meta/categories
curl http://localhost:8000/api/v1/trends/ai-copilots-vertical-saas
curl http://localhost:8000/api/v1/ingestion/runs
curl -X POST http://localhost:8000/api/v1/ingestion/demo
curl -X POST "http://localhost:8000/api/v1/ingestion/hackernews?feed=top&limit=10"
```

The frontend dashboard expects the API at `http://localhost:8000`.

### Ingest Signals

```bash
curl -X POST http://localhost:8000/api/v1/ingestion/signals \
  -H "Content-Type: application/json" \
  -d '{
    "signals": [
      {
        "title": "Compliance copilots for EU marketplace sellers",
        "content": "Marketplace sellers need help tracking VAT, product safety, and listing compliance changes.",
        "source_type": "manual",
        "source_id": "eu-marketplace-compliance-copilot",
        "upvotes": 54,
        "comments": 11,
        "keywords": ["compliance copilot", "marketplace sellers"],
        "category": "ai_saas"
      }
    ]
  }'
```

The MVP detector logs each run in `agent_executions`, stores source evidence in `trend_sources`, and recalculates trend, opportunity, saturation, and momentum scores.

### Hacker News Source

Hacker News ingestion does not require an API key:

```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/hackernews?feed=top&limit=10"
```

Supported feeds are `top`, `new`, `best`, `ask`, `show`, and `job`.

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/
│   │       └── trends.py
│   ├── core/             # Configuration & core
│   │   ├── config.py
│   │   ├── security.py
│   │   └── constants.py
│   ├── models/           # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── trend.py
│   │   └── alert.py
│   ├── schemas/          # Pydantic schemas
│   │   ├── trend.py
│   │   └── user.py
│   ├── services/         # Business logic and local seed data
│   │   ├── trend_service.py
│   │   └── seed.py
│   ├── agents/           # AI agent orchestration
│   │   ├── base_agent.py
│   │   ├── source_collector.py
│   │   └── orchestrator.py
│   ├── tasks/            # Celery tasks
│   │   ├── ingestion.py
│   │   └── report_generation.py
│   ├── utils/            # Utilities
│   │   ├── logging.py
│   │   └── validators.py
│   └── main.py           # FastAPI app
├── requirements.txt
└── README.md
```

## API Documentation

### Auto-generated Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

For the MVP, tables are created automatically on startup when `AUTO_CREATE_TABLES=true`.
Alembic is also configured for migration-based startup:

```bash
alembic upgrade head
```

Docker sets `AUTO_CREATE_TABLES=false` and runs Alembic before Uvicorn.

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/api/test_trends.py -v
```

## Development

### Code Quality

```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Run Agent Locally

```bash
python -m app.agents.source_collector
```

## Deployment

See [../docs/RAILWAY_DEPLOYMENT.md](../docs/RAILWAY_DEPLOYMENT.md) for the selected production setup.
