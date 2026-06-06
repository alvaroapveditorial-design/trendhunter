# Next Steps

## Siguiente P0/P1

1. Hacer commit inicial del estado actual.
2. Desplegar en Railway siguiendo `docs/RAILWAY_DEPLOYMENT.md`.
3. Ejecutar smoke test Railway completo: health, trends, demo ingestion, Hacker News, RSS y dashboard.
4. Añadir migraciones incrementales cuando cambie el schema.
5. Añadir tests frontend/smoke automatizado.
6. Validar RSS en Railway y después añadir GitHub trending/search como tercera fuente.
7. Añadir auth y rate limiting distribuido antes de beta pública.

## Siguiente P2

- Mejorar copy del dashboard.
- Añadir timestamp legible para runs.
- Añadir endpoint de stats.
- Añadir filtros por source.
- Añadir tests para servicios con DB aislada temporal.

## Puede Esperar

- Auth/billing.
- Qdrant/vector search.
- Celery/Redis scheduling.
- LangGraph completo.
- PDF reports.
