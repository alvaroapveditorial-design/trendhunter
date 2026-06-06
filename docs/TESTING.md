# Testing

## Backend

```bash
cd backend
pytest -q
python -m compileall app tests
```

## Frontend

```bash
cd frontend
npm run lint
npm run build
```

## Smoke Test Manual

1. Start backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

2. Start frontend:

```bash
cd frontend
npm run dev
```

3. Open `http://localhost:3000`.
4. Confirm trend cards are visible.
5. Click `Run demo ingestion`.
6. Click `Pull Hacker News`.
7. Confirm the dashboard still loads and `Recent pipeline runs` shows successful runs.

## API Smoke Commands

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/trends
curl http://localhost:8000/api/v1/ingestion/runs
curl -X POST http://localhost:8000/api/v1/ingestion/demo
curl -X POST "http://localhost:8000/api/v1/ingestion/hackernews?feed=top&limit=5"
```

Rate limited endpoints return `429` with `Retry-After` after too many mutation
requests to `/api/v1/ingestion/*`.

## Docker Smoke

```bash
docker compose up --build
```

Then open:

- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

## Migration Smoke

```bash
cd backend
alembic upgrade head
```
