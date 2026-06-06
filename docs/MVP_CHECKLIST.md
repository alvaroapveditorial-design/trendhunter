# Checklist Ejecutable Para Lanzar El MVP

Fecha de evaluación: 6 de junio de 2026.

Proyecto evaluado: **AI Trend Hunter**.

## Evaluación Actual

**Preparación para MVP público: 78/100.**

Trend Hunter ya no es solo una demo técnica: tiene backend FastAPI, dashboard Next.js, base SQLite local, pipeline heurístico, collectors reales de Hacker News y RSS, historial de ejecuciones, Docker/Alembic, Railway seleccionado y tests que pasan. La nota no sube más porque todavía falta auth, smoke continuo, rate limiting distribuido y una capa de producto/landing más comercial.

## Evidencia Verificada

- [x] Backend tests pasan: `15 passed`.
- [x] Frontend TypeScript pasa con `npm run lint`.
- [x] Frontend production build pasa con `npm run build`.
- [x] Existe dashboard Next.js conectado a la API.
- [x] Existen endpoints de tendencias, detalle, categorías e ingestion.
- [x] Existe ingestion demo/manual.
- [x] Existe collector público de Hacker News.
- [x] Existe collector público RSS/Atom.
- [x] Existe historial básico de ejecuciones.
- [x] Existe rate limiting in-memory para endpoints mutables.
- [x] Existe Docker Compose y Alembic.
- [x] Railway elegido como target de deploy.
- [x] Existe guía Railway en `docs/RAILWAY_DEPLOYMENT.md`.
- [x] El repositorio `trendhunter` ya tiene `.git` inicializado en rama `main`.

## Puntuación Ponderada

| Área | Puntos |
| --- | ---: |
| Loop principal de producto | 20/25 |
| Backend/API/datos | 17/20 |
| Frontend/dashboard UX | 13/15 |
| Testing y build | 12/15 |
| Seguridad y privacidad | 7/10 |
| Deploy/operación | 5/10 |
| Comercialización/monetización | 4/5 |
| **Total** | **78/100** |

## Checklist P0 Antes De Enseñarlo Fuera

- [ ] Hacer primer commit del repo recién inicializado.
- [x] Elegir target de deploy: Railway.
- [ ] Desplegar backend, frontend y Postgres en Railway.
- [ ] Ejecutar smoke Docker completo con `docker compose up --build`.
- [ ] Probar flujo manual completo en navegador: dashboard -> demo ingestion -> Hacker News -> RSS -> run history.
- [x] Añadir una segunda fuente real simple: RSS/Atom.
- [ ] Crear una landing comercial mínima encima o antes del dashboard.
- [ ] Añadir tests frontend/smoke automatizados.
- [ ] Documentar variables finales para deploy.

## Checklist P1 Para Beta Privada

- [ ] Auth básica con Supabase o alternativa elegida.
- [ ] Rate limiting distribuido con Redis o proveedor hosting.
- [ ] Persistencia en PostgreSQL para entorno desplegado.
- [ ] Separar claramente modo demo/local y modo producción.
- [ ] Añadir timestamps legibles en pipeline runs.
- [ ] Añadir endpoint de stats/resumen.
- [ ] Añadir filtros por fuente.
- [ ] Añadir estados vacíos y errores más comerciales en el dashboard.

## Checklist P2 Para Producto Vendible

- [ ] Insights LLM con OpenAI/Anthropic.
- [ ] Alertas por keywords.
- [ ] Reportes PDF.
- [ ] Billing con Stripe.
- [ ] Emails con Resend.
- [ ] Vector search/Qdrant para similitud de tendencias.
- [ ] Orquestación LangGraph real.
- [ ] Monitorización de competidores.

## Siguientes Pasos Recomendados

1. **Commit inicial:** guardar el estado actual en Git para dejar una base segura.
2. **Smoke Docker:** validar que el MVP completo levanta igual fuera del entorno local suelto.
3. **Railway deploy:** crear servicios backend/frontend/Postgres y configurar variables.
4. **Tercera fuente real:** añadir GitHub porque depender solo de Hacker News/RSS limita el valor percibido.
5. **Landing comercial:** explicar en 10 segundos qué oportunidad detecta, para quién y por qué importa.
6. **Auth + beta:** solo después de validar que el dashboard genera valor real.

## Verificaciones Ejecutadas

```bash
cd backend && pytest -q
# 15 passed

cd frontend && npm run lint
# TypeScript OK

cd frontend && npm run build
# Next.js build OK
```

## Riesgos Principales

- **Sin deploy real:** todavía no está probado como producto accesible externamente.
- **Sin auth:** apto para demo, no para usuarios reales con datos propios.
- **Rate limit local:** suficiente para una instancia, débil para producción multi-instancia.
- **Cobertura de fuentes aún limitada:** Hacker News y RSS validan el pipeline, pero falta GitHub/Reddit/Product Hunt para cubrir más mercado.
- **Sin LLM real:** el scoring heurístico funciona, pero los insights todavía no son suficientemente diferenciales.
