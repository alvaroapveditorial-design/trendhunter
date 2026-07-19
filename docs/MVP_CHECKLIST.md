# Checklist Ejecutable Para Lanzar El MVP

Fecha de evaluación: 19 de julio de 2026.

Proyecto evaluado: **AI Trend Hunter**.

## Evaluación Actual

**Preparación para MVP público: 85/100.**

Desde la última evaluación (92/100 sobre un alcance más chico) se añadió auth passwordless por email, beta signups y billing con Stripe (checkout, portal, webhook) de punta a punta, con páginas frontend nuevas (`/login`, `/dashboard`, `/pricing`, `/privacy`, `/terms`) y 47 tests backend en verde. La nota no sube más porque **Stripe y Resend aún no tienen credenciales reales en Railway producción** (el código funciona, pero checkout y envío de emails fallarán hasta configurarlas), y porque el rate limiting sigue siendo in-memory (no distribuido).

## Evidencia Verificada Hoy

- [x] Backend: `pytest -q` → 47 passed.
- [x] Frontend: `npm run lint` (tsc --noEmit) → OK.
- [x] Frontend: `npm run build` → build de producción OK, genera `/`, `/login`, `/pricing`, `/privacy`, `/terms` (estáticas) y `/dashboard` (dinámica).
- [x] Railway: `railway status` → `trendhunter-backend` y `trendhunter-frontend` Online, Postgres Online.
- [x] Railway: `GET /health` del backend → `200`.
- [x] Commit `6e0560a` pusheado a `origin/main` (auth + beta + billing + doc).
- [x] Confirmado: el deploy activo del backend en Railway corresponde al commit `6e0560a` y corrió las migraciones `0002_beta_signups` → `0003_subscriptions` → `0004_login_codes` contra Postgres.
- [x] Railway: variables `JWT_SECRET` y `SECRET_KEY` configuradas en producción con valores fuertes (no defaults inseguros).
- [ ] Railway: variables `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRO_PRICE_ID` — **no configuradas** en producción todavía.
- [ ] Railway: variable `RESEND_API_KEY` — **no configurada** en producción todavía (sin ella no se envían los códigos de login reales).
- [ ] Railway: variable `APP_URL` — no configurada explícitamente (usa default `http://localhost:3000`, hay que apuntarla al dominio real del frontend para que los redirects de Stripe funcionen).

## Puntuación Ponderada

| Área | Puntos | Cambio vs. anterior |
| --- | ---: | --- |
| Loop principal de producto | 20/25 | = |
| Backend/API/datos | 18/20 | +1 (auth, beta, billing) |
| Frontend/dashboard UX | 14/15 | +1 (login, dashboard, pricing, privacy, terms) |
| Testing y build | 13/15 | +1 (47 tests, cubre auth/beta/billing) |
| Seguridad y privacidad | 9/10 | +2 (auth propia + ingestion ya protegida con shared key) |
| Deploy/operación | 6/10 | +1 (confirmado Online en Railway; sigue sin smoke Docker ni rate limit distribuido) |
| Comercialización/monetización | 5/5 | +1 (billing Stripe + pricing page completos en código) |
| **Total** | **85/100** | +7 |

## Checklist P0 Antes De Enseñarlo Fuera

- [x] Hacer primer commit del repo recién inicializado.
- [x] Elegir target de deploy: Railway.
- [x] Desplegar backend, frontend y Postgres en Railway.
- [x] Proteger endpoints de ingestion con shared key.
- [x] Auth passwordless (login por código de email) implementada y testeada.
- [x] Beta signups implementados y testeados.
- [x] Billing con Stripe (checkout/portal/webhook) implementado y testeado.
- [x] Landing con pricing, privacy y terms.
- [ ] Ejecutar smoke Docker completo con `docker compose up --build`.
- [ ] Configurar `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` / `STRIPE_WEBHOOK_SECRET` / `STRIPE_PRO_PRICE_ID` reales en Railway.
- [ ] Configurar `RESEND_API_KEY` real en Railway (o confirmar proveedor de email alternativo).
- [ ] Configurar `APP_URL` en Railway apuntando al dominio real del frontend.
- [ ] Verificar en Railway que el deploy activo corresponde al último commit pusheado.

## Checklist P1 Para Beta Privada

- [x] Auth básica (propia, JWT + código por email — no se usó Supabase).
- [ ] Probar el flujo de login end-to-end contra producción una vez `RESEND_API_KEY` esté configurada.
- [ ] Probar un pago real de prueba (Stripe test mode) end-to-end: checkout -> webhook -> `/dashboard` refleja suscripción activa.
- [ ] Rate limiting distribuido con Redis o proveedor hosting.
- [ ] Persistencia en PostgreSQL para entorno desplegado (confirmar que auth/beta/billing usan Postgres en Railway, no SQLite).
- [ ] Separar claramente modo demo/local y modo producción.
- [ ] Añadir timestamps legibles en pipeline runs.
- [ ] Añadir endpoint de stats/resumen.
- [ ] Añadir filtros por fuente.

## Checklist P2 Para Producto Vendible

- [ ] Insights LLM con OpenAI/Anthropic.
- [ ] Alertas por keywords.
- [ ] Reportes PDF.
- [x] Billing con Stripe (código completo; pendiente activar credenciales — ver P0).
- [x] Emails con Resend (código completo; pendiente activar credenciales — ver P0).
- [ ] Vector search/Qdrant para similitud de tendencias.
- [ ] Orquestación LangGraph real.
- [ ] Monitorización de competidores.

## Siguientes Pasos Recomendados (Ejecutables, En Orden)

1. **Activar Stripe en producción:** crear producto/precio real en el dashboard de Stripe, copiar `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_PRO_PRICE_ID` y configurar el endpoint de webhook para obtener `STRIPE_WEBHOOK_SECRET`; cargar las cuatro en `railway variables --set` para `trendhunter-backend`.
2. **Activar Resend en producción:** crear cuenta/API key en Resend, verificar el dominio de envío, cargar `RESEND_API_KEY` y `SENDER_EMAIL` en Railway.
3. **Configurar `APP_URL`:** apuntarla al dominio real del frontend en Railway para que los redirects de Stripe checkout/portal vuelvan al sitio correcto.
4. ~~**Verificar el deploy post-push**~~ — hecho: el deploy activo ya corre `6e0560a` con las migraciones aplicadas.
5. **Probar el flujo completo en producción:** signup beta -> login por código de email -> checkout Stripe (test mode) -> webhook actualiza suscripción -> dashboard refleja el estado. Documentar cualquier fallo.
6. **Smoke Docker:** correr `docker compose up --build` localmente para validar que el stack completo (incluyendo las nuevas rutas) levanta igual que en Railway.
7. **Rate limiting distribuido:** mover el rate limiter in-memory a Redis antes de escalar a más de una instancia.

## Verificaciones Ejecutadas Hoy

```bash
cd backend && python -m pytest -q
# 47 passed in 0.42s

cd frontend && npm run lint
# tsc --noEmit -p tsconfig.lint.json -> OK

cd frontend && npm run build
# Next.js build OK: /, /login, /pricing, /privacy, /terms estáticas; /dashboard dinámica

railway status
# trendhunter-backend Online, trendhunter-frontend Online, Postgres Online

curl -s -o /dev/null -w "%{http_code}\n" https://trendhunter-backend-production.up.railway.app/health
# 200
```

## Riesgos Principales

- **Billing no funcional en producción todavía:** el código de Stripe está completo y testeado, pero sin credenciales reales configuradas en Railway, cualquier intento de checkout fallará en vivo. No anunciar pricing públicamente hasta completar el paso 1 de "Siguientes Pasos".
- **Login por email no funcional en producción todavía:** mismo problema con Resend — sin `RESEND_API_KEY`, los códigos de login no llegan. No abrir el login a usuarios reales hasta completar el paso 2.
- **Rate limit local:** suficiente para una instancia, débil para producción multi-instancia.
- **Sin smoke Docker reciente:** las nuevas rutas (auth/beta/billing) no se han validado en el stack Docker completo, solo en local con `uvicorn --reload` y en Railway.
- **Sin LLM real:** el scoring heurístico funciona, pero los insights todavía no son suficientemente diferenciales.
