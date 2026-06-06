# Railway Deployment

Railway is the selected deployment target for the MVP.

The repo is an isolated monorepo, so deploy it as three Railway services:

- `trendhunter-backend`: root directory `backend`
- `trendhunter-frontend`: root directory `frontend`
- `Postgres`: Railway managed PostgreSQL

Railway does not run `docker-compose.yml` directly in production. Map each Compose service to a Railway service instead.

## 1. Prepare Git

Commit the current working tree before connecting Railway:

```bash
git add .
git commit -m "Prepare MVP for Railway deploy"
```

Push the repo to GitHub, then import it in Railway.

## 2. Create Railway Project

1. Create an empty Railway project.
2. Add a PostgreSQL database service.
3. Add the backend service from the GitHub repo.
4. Add the frontend service from the same GitHub repo.

For each app service, set the service root directory:

- Backend root directory: `backend`
- Frontend root directory: `frontend`

If Railway asks for config-as-code path, use:

- Backend: `/backend/railway.toml`
- Frontend: `/frontend/railway.toml`

## 3. Backend Variables

Set these variables on `trendhunter-backend`:

```bash
ENVIRONMENT=production
DEBUG=false
AUTO_CREATE_TABLES=false
DATABASE_URL=${{Postgres.DATABASE_URL}}
CORS_ORIGINS=https://${{trendhunter-frontend.RAILWAY_PUBLIC_DOMAIN}}
HACKERNEWS_API_URL=https://hacker-news.firebaseio.com/v0
HACKERNEWS_DEFAULT_LIMIT=20
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
JWT_SECRET=<generate-a-strong-secret>
SECRET_KEY=<generate-a-strong-secret>
```

Generate a public domain for the backend after the first deploy. The backend uses Railway's `PORT` automatically through the Dockerfile.

## 4. Frontend Variables

Set these variables on `trendhunter-frontend` after the backend has a public domain:

```bash
API_URL=https://${{trendhunter-backend.RAILWAY_PUBLIC_DOMAIN}}
NEXT_PUBLIC_API_URL=https://${{trendhunter-backend.RAILWAY_PUBLIC_DOMAIN}}
```

Then generate a public domain for the frontend and redeploy both services so CORS and client-side fetches use the final URLs.

## 5. Smoke Test

After deploy:

```bash
curl https://<backend-domain>/health
curl https://<backend-domain>/api/v1/trends
curl -X POST https://<backend-domain>/api/v1/ingestion/demo
curl -X POST "https://<backend-domain>/api/v1/ingestion/hackernews?feed=top&limit=10"
```

Then open the frontend domain and verify:

- Dashboard loads trends.
- `Run demo ingestion` creates or updates trends.
- `Pull Hacker News` creates or updates trends.
- `Recent pipeline runs` shows successful runs.

## 6. Known Production Gaps

This is suitable for an MVP demo, not a public beta yet.

Before external users:

- Add authentication.
- Keep PostgreSQL as the production database.
- Replace in-memory rate limiting with Redis or provider-level protection if running multiple replicas.
- Add a second public source, preferably RSS or GitHub.
- Add frontend smoke tests.

## References

- Railway monorepo deployment: https://docs.railway.com/deployments/monorepo
- Railway Docker Compose mapping: https://docs.railway.com/guides/docker-compose
- Railway PostgreSQL variables: https://docs.railway.com/databases/postgresql
- Railway config-as-code: https://docs.railway.com/config-as-code
