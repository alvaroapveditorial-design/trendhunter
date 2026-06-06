# Execution Plan

## Estado Actual

AI Trend Hunter es un MVP SaaS en marcha para detectar tendencias emergentes a partir de señales públicas.

Stack real actual:
- Backend: FastAPI, SQLAlchemy, Pydantic, SQLite local por defecto.
- Frontend: Next.js 16, React 18, TypeScript, CSS propio.
- Fuente real integrada: Hacker News API pública.
- IA/LLM: configurado como futuro, sin llamadas reales todavía.
- Auth/billing/queues/vector DB: documentados como visión, no implementados en el MVP actual.

## Terminado

- API FastAPI arrancable localmente.
- SQLite local y creación automática de tablas.
- Seeds de tendencias.
- CRUD mínimo/listado/detalle de tendencias.
- Pipeline heurística de ingestion.
- Ingestion manual de señales.
- Ingestion demo.
- Collector Hacker News sin API key.
- Registro de ejecuciones en `agent_executions`.
- Dashboard Next.js con filtros, detalle, acciones de ingestion e historial reciente.
- Tests backend de endpoints principales.
- Build frontend verificado.

## Incompleto

- Landing comercial separada.
- Auth real.
- Deploy a un proveedor concreto.
- Reportes, alertas y favoritos.
- Integraciones Reddit/GitHub/Product Hunt/RSS.
- Scoring calibrado con datos reales.
- Capa LLM para insights avanzados.

## Roto o Riesgoso

- `create_all` sigue activo por defecto para local, pero Docker usa Alembic.
- Endpoints de ingestion tienen rate limiting local; falta auth y rate limiting distribuido.
- Frontend depende de que backend esté en `NEXT_PUBLIC_API_URL`.
- Hacker News puede fallar por red externa; el frontend todavía no muestra error fino para server actions.
- No hay tests frontend con navegador.

## Prioridades Reales

### P0

- Mantener instalación, tests y builds verdes.
- Mantener `.env.example` alineado con config real.
- Evitar que dependencias externas bloqueen el flujo local.

### P1

- Completar flujo principal: dashboard, acción principal, resultado, historial.
- Añadir endpoint/UI de historial de runs.
- Documentar prueba manual end-to-end.
- Base Docker/Alembic creada; falta target de deploy concreto.

### P2

- Tests frontend/smoke automatizado.
- Mejorar copy y navegación.
- Validaciones adicionales en ingestion.
- Limpieza de dependencias no usadas del backend.

### P3

- Auth, billing, rate limiting distribuido, vector DB, Celery, Qdrant, agentes complejos, reportes PDF.

## Decisiones Técnicas

- SQLite por defecto para acelerar desarrollo local.
- FastAPI sigue como backend principal.
- Next.js dashboard es la primera pantalla usable; landing separada puede esperar.
- Detector heurístico antes de LLM para mantener MVP funcional sin credenciales.
- Hacker News como primera fuente real porque no necesita API key.

## Orden Recomendado

1. Cerrar loop MVP: fuente real -> ingestion -> scoring -> dashboard -> historial.
2. Añadir smoke test automatizado de frontend/API.
3. Elegir target de deploy y ajustar variables.
4. Añadir segunda fuente pública.
5. Añadir auth solo cuando haya un flujo beta claro.
