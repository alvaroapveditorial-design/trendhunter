# Next Steps

## Siguiente P0/P1

1. Hacer commit inicial del estado actual.
2. Desplegar en Railway siguiendo `docs/RAILWAY_DEPLOYMENT.md`.
3. Mantener smoke test Playwright verde: dashboard, demo ingestion, Hacker News, RSS, GitHub y runs.
4. Añadir `GITHUB_TOKEN` en Railway para mejorar rate limits de GitHub.
5. Añadir migraciones incrementales cuando cambie el schema.
6. Preparar auth para beta privada.
7. Añadir rate limiting distribuido antes de beta pública.

## Siguiente P2

- Mejorar copy del dashboard.
- Añadir timestamp legible para runs.
- Añadir endpoint de stats.
- Añadir tests para servicios con DB aislada temporal.

## Hecho

- Añadido smoke automático en GitHub Actions.
- Añadido filtro por source en dashboard y API.
- Limpieza de keywords para descartar palabras flojas.

## Puede Esperar

- Auth/billing.
- Qdrant/vector search.
- Celery/Redis scheduling.
- LangGraph completo.
- PDF reports.
