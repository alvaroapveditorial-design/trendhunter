# Checklist Ejecutable Para Lanzar El MVP

Fecha de evaluación: 19 de julio de 2026.

Proyecto evaluado: **AI Trend Hunter**.

## Evaluación Actual

**Preparación para MVP público: 87/100.**

Sobre la evaluación anterior (85/100) se resolvieron tres huecos operativos detectados en la revisión de lanzamiento: endpoint admin para ver beta signups, error tracking (Sentry) listo para activarse, y analytics (Plausible) conectado al frontend. La nota no sube más porque **quedan acciones que solo el usuario puede hacer** (credenciales reales de Stripe/Resend/Sentry/Plausible en Railway, dominio propio, revisión legal) y porque el rate limiting sigue siendo in-memory.

## Resuelto Hoy (Código)

- [x] **Admin endpoint para beta signups**: `GET /api/v1/beta/signups` ([beta.py](../backend/app/api/v1/beta.py)), protegido con header `X-Admin-Key` contra `ADMIN_API_KEY`. Falla cerrado: si la key no está configurada, deniega todo (no expone emails por defecto). 3 tests nuevos.
- [x] **Sentry gateado por config**: [main.py](../backend/app/main.py) inicializa `sentry_sdk` solo si `SENTRY_DSN` está configurada; sin ella, no cambia nada. Verificado que arranca con y sin DSN.
- [x] **Plausible conectado**: [layout.tsx](../frontend/src/app/layout.tsx) inyecta el script de Plausible solo si `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` está configurada en el build del frontend.
- [x] Backend: `pytest -q` → **50 passed** (47 + 3 nuevos de `list_beta_signups`).
- [x] Frontend: `npm run lint` y `npm run build` → OK (requiere Node ≥20; con Node 18 el build no corre y solo muestra un warning — usar `nvm use 20`).

## Esto Ya No Se Puede Resolver Con Código — Requiere Acción Del Usuario

- [ ] **Stripe real**: crear producto/precio en el dashboard de Stripe y cargar `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRO_PRICE_ID` en Railway.
- [ ] **Resend real**: cuenta + API key + dominio de envío verificado (SPF/DKIM), cargar `RESEND_API_KEY`/`SENDER_EMAIL` en Railway.
- [ ] **`APP_URL`**: apuntarla al dominio real del frontend para que los redirects de Stripe funcionen.
- [ ] **`ADMIN_API_KEY`**: generar un valor fuerte y cargarlo en Railway para poder usar el endpoint de beta signups.
- [ ] **`SENTRY_DSN`** (opcional pero recomendado): crear proyecto en Sentry y cargar el DSN.
- [ ] **`NEXT_PUBLIC_PLAUSIBLE_DOMAIN`** (opcional pero recomendado): crear el sitio en Plausible con el dominio real y cargarlo como variable de build del frontend en Railway.
- [ ] **Dominio propio**: hoy corre en `*.up.railway.app`; para cobrar con tarjeta y enviar emails de login sin oler a spam conviene un dominio propio.
- [ ] **Revisión legal de `/privacy` y `/terms`**: las páginas ya existen pero dicen explícitamente "responsable pendiente de completar" — hay que rellenar entidad legal, NIF/CIF y domicilio antes de vender públicamente. Esto no lo puedo inventar por ti.
- [ ] **Backups de Postgres en Railway**: confirmar plan/retención actual.
- [ ] **Canal de soporte**: un email o chat visible para usuarios de pago.

## Puntuación Ponderada

| Área | Puntos | Cambio vs. anterior |
| --- | ---: | --- |
| Loop principal de producto | 20/25 | = |
| Backend/API/datos | 18/20 | = |
| Frontend/dashboard UX | 14/15 | = |
| Testing y build | 14/15 | +1 (50 tests, cubre el endpoint admin nuevo) |
| Seguridad y privacidad | 10/10 | +1 (beta signups ya no quedan expuestos sin protección) |
| Deploy/operación | 6/10 | = (sigue sin smoke Docker ni rate limit distribuido; observabilidad lista pero no activada) |
| Comercialización/monetización | 5/5 | = |
| **Total** | **87/100** | +2 |

## Checklist P0 Antes De Enseñarlo Fuera

- [x] Hacer primer commit del repo recién inicializado.
- [x] Elegir target de deploy: Railway.
- [x] Desplegar backend, frontend y Postgres en Railway.
- [x] Proteger endpoints de ingestion con shared key.
- [x] Auth passwordless (login por código de email) implementada y testeada.
- [x] Beta signups implementados y testeados, con endpoint admin para leerlos.
- [x] Billing con Stripe (checkout/portal/webhook) implementado y testeado.
- [x] Landing con pricing, privacy y terms.
- [x] Error tracking y analytics listos para activarse (Sentry, Plausible).
- [ ] Ejecutar smoke Docker completo con `docker compose up --build`.
- [ ] Configurar en Railway: `STRIPE_*`, `RESEND_API_KEY`, `APP_URL`, `ADMIN_API_KEY`, `SENTRY_DSN`, `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`.
- [ ] Rellenar entidad legal real en `/privacy` y `/terms`.
- [ ] Dominio propio.

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

1. **Cargar todas las variables pendientes en Railway** (`STRIPE_*`, `RESEND_API_KEY`, `SENDER_EMAIL`, `APP_URL`, `ADMIN_API_KEY`, `SENTRY_DSN`, `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`) — es el único paso que desbloquea billing, email, observabilidad y el panel de beta signups a la vez.
2. **Probar el flujo completo en producción:** signup beta -> `curl` a `/api/v1/beta/signups` con `X-Admin-Key` para confirmarlo -> login por código de email -> checkout Stripe (test mode) -> webhook actualiza suscripción -> dashboard refleja el estado.
3. **Dominio propio + DNS**, y actualizar `APP_URL`/CORS/Resend con el dominio final.
4. **Rellenar `/privacy` y `/terms`** con la entidad legal real.
5. **Smoke Docker:** correr `docker compose up --build` localmente para validar que el stack completo levanta igual que en Railway.
6. **Rate limiting distribuido:** mover el rate limiter in-memory a Redis antes de escalar a más de una instancia.

## Verificaciones Ejecutadas Hoy

```bash
cd backend && python -m pytest -q
# 50 passed

cd backend && python -c "
import os; os.environ['SENTRY_DSN'] = 'https://public@sentry.example.com/1'
from app.main import app
"
# Sentry error tracking enabled -- app loads fine with DSN set

nvm use 20 && cd frontend && npm run lint
# tsc --noEmit -p tsconfig.lint.json -> OK

nvm use 20 && cd frontend && npm run build
# Next.js build OK: /, /login, /pricing, /privacy, /terms estáticas; /dashboard dinámica
```

## Riesgos Principales

- **Billing no funcional en producción todavía:** el código de Stripe está completo y testeado, pero sin credenciales reales configuradas en Railway, cualquier intento de checkout fallará en vivo. No anunciar pricing públicamente hasta completarlo.
- **Login por email no funcional en producción todavía:** mismo problema con Resend — sin `RESEND_API_KEY`, los códigos de login no llegan. No abrir el login a usuarios reales hasta completarlo.
- **Beta signups sin panel visible todavía:** el endpoint admin existe pero sin `ADMIN_API_KEY` configurada en Railway sigue sin poder consultarse.
- **Rate limit local:** suficiente para una instancia, débil para producción multi-instancia.
- **Sin smoke Docker reciente:** las nuevas rutas (auth/beta/billing) no se han validado en el stack Docker completo, solo en local con `uvicorn --reload` y en Railway.
- **Sin LLM real:** el scoring heurístico funciona, pero los insights todavía no son suficientemente diferenciales.
