# MVP Status

## Evaluación

Puntuación actual verificada: **85/100** (ver desglose ponderado en `docs/MVP_CHECKLIST.md`) como MVP técnico desplegado.

Se mantiene por encima de 90 porque existe el loop real desplegado con autodeploy, y ahora además hay auth, beta signups y billing implementados de punta a punta. Falta activar credenciales reales de Stripe/Resend en producción y rate limiting distribuido:

`Hacker News/RSS/GitHub/manual signal -> detector -> trend score -> dashboard -> run history`

## Terminado

- Backend FastAPI local.
- Frontend Next.js dashboard.
- SQLite local por defecto.
- API de tendencias.
- Pipeline heurística.
- Ingestion manual/demo.
- Hacker News collector.
- RSS/Atom collector.
- GitHub collector.
- Historial básico de ejecuciones.
- Estados de loading/error en acciones principales del dashboard.
- Página de error del dashboard cuando el backend no está disponible.
- Manejo 502 controlado si Hacker News falla.
- Dockerfiles para backend y frontend.
- `docker-compose.yml` mínimo para levantar el MVP completo.
- Railway elegido como target de deploy.
- Config-as-code Railway añadida para backend y frontend.
- Alembic configurado con migración inicial.
- Dependencias backend limpiadas para instalar solo el MVP real y evitar conflictos de paquetes futuros.
- Rate limiting in-memory para endpoints mutables de ingestion.
- Tests backend.
- Build frontend.
- Smoke Playwright.
- Auth passwordless por código de un solo uso enviado por email (`app/api/v1/auth.py`, `app/services/email_service.py`, JWT propio vía `JWT_SECRET`, migración `0004_login_codes.py`).
- Beta signups (`app/api/v1/beta.py`, migración `0002_beta_signups.py`).
- Billing con Stripe: checkout session, billing portal y webhook (`app/api/v1/billing.py`, migración `0003_subscriptions.py`).
- Páginas frontend: `/login`, `/dashboard`, `/pricing`, `/privacy`, `/terms`, componentes `LoginForm`, `PricingCheckout`, `BillingPortalButton`, `LandingInteractions`.
- Tests backend para auth, beta y billing (11 tests, todos en verde).

## Parcialmente Terminado

- Producto UX: usable como dashboard, pero sin landing comercial completa.
- Agentes: hay registro y detector simple, pero no LangGraph real.
- IA: placeholders/config, sin llamadas LLM.
- Seguridad: auth propia (JWT + código por email) y rate limiting local ya implementados; falta rate limiting distribuido para multi-instancia.
- Billing: flujo Stripe completo en código, pero sin credenciales reales (`STRIPE_SECRET_KEY`, `STRIPE_PRO_PRICE_ID`, `STRIPE_WEBHOOK_SECRET`) configuradas en producción, así que checkout/portal no funcionan todavía end-to-end.
- Email: flujo de código de login completo en código, pero sin `RESEND_API_KEY` configurada en producción no se envían emails reales.
- Producción: base Docker/Alembic creada, pendiente de endurecer para un proveedor concreto.

## Pendiente

- Rate limiting distribuido si se escala a varias instancias.
- Reportes/alertas.

## Bloqueado Por Credenciales o Servicios

- OpenAI/Anthropic: insights LLM.
- Stripe: activar claves reales (`STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRO_PRICE_ID`) para billing en producción.
- Resend: activar `RESEND_API_KEY` para envío real de códigos de login.
- Reddit/Product Hunt con rate limits altos: tokens opcionales.

## Cómo Probar

Backend:

```bash
cd backend
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run lint
npm run build
npm run smoke
npm run dev
```

Docker:

```bash
docker compose up --build
```

Migraciones:

```bash
cd backend
alembic upgrade head
```

Flujo manual:

1. Abrir `http://localhost:3000`.
2. Pulsar `Run demo ingestion`.
3. Pulsar `Pull Hacker News`.
4. Pulsar `Pull RSS`.
5. Pulsar `Pull GitHub`.
6. Ver nuevas tendencias o actualizaciones.
7. Revisar `Recent pipeline runs` en el panel derecho.

## Cambios Recientes

- Las acciones principales del dashboard ahora muestran estado de ejecución y errores.
- El dashboard tiene una pantalla de error con botón de retry si no puede cargar datos.
- El endpoint de Hacker News devuelve `502` con mensaje estable si falla la red externa.

## Variables Relevantes

- `DATABASE_URL`: por defecto `sqlite:///./trendhunter.db`.
- `NEXT_PUBLIC_API_URL`: URL del backend para el frontend, por defecto `http://localhost:8000`.
- `HACKERNEWS_API_URL`: API pública de Hacker News.
- `HACKERNEWS_DEFAULT_LIMIT`: límite por defecto de historias a recoger.
- `RSS_DEFAULT_FEED`: feed RSS configurado por defecto.
- `RSS_FEED_URLS`: feeds RSS en formato `clave=url,clave=url`.
- `GITHUB_API_URL`: API pública de GitHub.
- `GITHUB_DEFAULT_LIMIT`: límite por defecto de repositorios a recoger.
- `GITHUB_SEARCH_QUERY`: query por defecto para GitHub search.
- `AUTO_CREATE_TABLES`: `true` para comodidad local; en Docker se usa `false` porque corre Alembic.
- `RATE_LIMIT_ENABLED`: activa/desactiva rate limiting.
- `RATE_LIMIT_REQUESTS`: número de requests permitidas por ventana.
- `RATE_LIMIT_PERIOD`: ventana de rate limit en segundos.
- `JWT_SECRET`: firma de los tokens de sesión emitidos tras el login por código; debe cambiarse en producción.
- `RESEND_API_KEY` / `SENDER_EMAIL`: envío de los códigos de login por email.
- `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` / `STRIPE_WEBHOOK_SECRET` / `STRIPE_PRO_PRICE_ID`: billing con Stripe (checkout, portal, webhook).
- `BILLING_TRIAL_DAYS`: días de trial antes de cobrar.
- `APP_URL`: URL pública usada en los redirects de Stripe checkout/portal.

## Rate Limiting

El MVP protege `POST /api/v1/ingestion/*` con un rate limiter in-memory por IP y ruta.
Esto es suficiente para una demo o una sola instancia. Para producción multi-instancia,
hay que cambiarlo por Redis o un rate limiter del proveedor de hosting.

## Deploy/Docker

Target elegido: Railway. Guía operativa en `docs/RAILWAY_DEPLOYMENT.md`.

El compose actual levanta:

- Backend en `http://localhost:8000`.
- Frontend en `http://localhost:3000`.
- SQLite persistida en volumen Docker `backend_data`.

El backend ejecuta `alembic upgrade head` antes de iniciar Uvicorn.
