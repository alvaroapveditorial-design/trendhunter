# Documento de Traspaso Técnico y de Negocio — AI Trend Hunter

**Fecha de este documento:** 26 de julio de 2026
**Destinatario:** un modelo de IA (ChatGPT) que actuará como CTO, CPO, estratega de producto, experto en SaaS, marketing, crecimiento y monetización.
**Autor:** Claude (Anthropic), como asistente técnico del fundador (Álvaro), a partir de una auditoría directa del código fuente, la configuración de infraestructura, el histórico de commits y la documentación interna del proyecto.

Este documento asume que quien lo lee **no ha visto nunca el código**. Todo lo que se afirma aquí ha sido verificado leyendo el repositorio real, no inferido de memoria. Donde algo está planeado pero no implementado, se dice explícitamente. Donde algo está roto o es un riesgo, también.

---

# 1. Resumen ejecutivo

## Qué hace el SaaS

**AI Trend Hunter** (dominio: `aitrendhunter.app`) es una plataforma que **detecta tendencias emergentes de producto/SaaS a partir de señales públicas de desarrollo** — repositorios de GitHub, historias de Hacker News y feeds RSS de medios de startups/tech — y las convierte en una lista puntuada y accionable de oportunidades de negocio.

El usuario abre un dashboard, ve una lista de "tendencias" (por ejemplo: *"Self-hosted LLM gateways"*, *"AI agents for QA testing"*), cada una con:

- Un **trend score** (0-100).
- Un **opportunity score** (0-100).
- Un **saturation score** (0-100, cuanto más alto peor: más saturado el espacio).
- Un **momentum** (velocidad de crecimiento reciente).
- Las **fuentes concretas** (qué repos, qué historias de HN, qué artículos) que sustentan esa tendencia, con enlaces.
- Un **insight en texto** generado heurísticamente.
- Una lista de **ideas de producto SaaS** derivadas de esa tendencia.

## Qué problema resuelve

Los fundadores, indie hackers y equipos de producto que buscan la próxima idea de SaaS pierden horas cada semana rastreando manualmente GitHub trending, Hacker News y newsletters de startups, sin ninguna forma sistemática de distinguir una tendencia real de un pico de ruido de fin de semana. Cuando una tendencia llega a un informe o newsletter, la ventana de oportunidad ya suele haberse cerrado, porque la señal real aparece primero en código (commits, estrellas, releases) y discusión técnica (hilos de HN), no en cobertura mediática.

## Para quién está diseñado

- **Indie hackers y fundadores solo/en equipos pequeños** que buscan su próxima idea de producto o quieren validar una que ya tienen.
- **Product managers** que quieren vigilar espacios adyacentes a su producto.
- **Scouts de venture capital / inversores ángel** que quieren señal temprana de qué está construyendo la comunidad técnica antes de que sea noticia.

No está (todavía) diseñado para equipos grandes, uso multi-usuario/colaborativo, ni para analistas que necesiten exportación masiva de datos: es una herramienta de un solo usuario por cuenta, sin roles ni equipos.

## Propuesta de valor

"Detecta oportunidades de SaaS antes de que sean obvias." La promesa concreta, tal como está en la landing y el pricing, es: **señal pública dentro (GitHub, Hacker News, RSS) → tendencias puntuadas fuera → briefs accionables** que se pueden verificar (cada score enlaza a su evidencia original, nada es una caja negra).

## Diferenciación frente a la competencia

- **Basado en señal de código, no en cobertura mediática**: la mayoría de herramientas de "trend spotting" (newsletters, paneles de Google Trends, Exploding Topics) trabajan sobre búsquedas o menciones sociales, que llegan tarde. AI Trend Hunter mira directamente los repos y los hilos técnicos donde la señal aparece primero.
- **Puntuación explicable y trazable**: cada trend score se puede desglosar hasta la señal original (qué repo, cuántas estrellas, qué hilo de HN, cuántos puntos). No hay "magia de IA" opaca — ver sección 7 para el detalle exacto del algoritmo, que es heurístico y determinista, no un LLM.
- **Precio de entrada bajo y sin fricción de instalación**: 39 €/mes, sin integraciones que configurar, funciona desde el primer login.

**Advertencia honesta para el lector de este documento**: hoy, la diferenciación real está más en el *concepto y el posicionamiento* que en la sofisticación técnica del motor de detección, que es deliberadamente simple (heurístico, sin IA/LLM real todavía — ver secciones 2 y 7). Esto es una decisión consciente de MVP, no un secreto oculto, pero es importante que quien diseñe la estrategia de crecimiento lo sepa antes de prometer en marketing algo que el producto aún no hace.

---

# 2. Estado actual

**Nota de fecha:** existe un documento interno (`docs/MVP_CHECKLIST.md`) fechado el 24 de julio de 2026 que puntúa el proyecto en **90/100**. Desde esa fecha (hace dos días) se han hecho más cambios reales en producción que ese documento no refleja todavía. Esta sección 2 es la versión actualizada y verificada directamente contra el código y el histórico de commits a fecha de hoy.

## Terminado y funcionando en producción real

- **Dominio propio con SSL**: `aitrendhunter.app`, verificado en Railway.
- **Stripe en modo live**: producto "AI Trend Hunter Pro" a 39 €/mes, checkout, portal de cliente y webhook configurados con claves live reales. Un flujo de registro→pago→login se ha probado de punta a punta con una tarjeta real del propio fundador.
- **Resend en modo live**: los códigos de login se envían por email de verdad (confirmado en logs con `200 OK`).
- **Autenticación passwordless propia**: login por código de un solo uso de 6 dígitos enviado por email, sesión vía cookie JWT firmada. No usa Supabase (que está configurado en variables de entorno pero no conectado a ningún endpoint real — ver sección 9).
- **Billing completo con Stripe**: checkout de suscripción con periodo de prueba de 7 días, portal de cliente para autogestión, webhook que sincroniza el estado real de la suscripción.
- **Meta Pixel + Conversions API**: tracking de conversión verificado en producción, tanto cliente (`PageView`) como servidor (`StartTrial` al completar checkout, `Purchase` al pasar de trialing a active), con email hasheado en SHA-256 y deduplicación por `event_id`.
- **Motor de detección heurístico**: pipeline real de ingestión → scoring → guardado, sin coste de LLM (ver sección 7).
- **Tres fuentes de datos públicas reales**: GitHub Search API, Hacker News API pública, RSS/Atom (TechCrunch Startups, Product Hunt, HN frontpage vía hnrss).
- **Cron de ingestión automática diaria en Railway** (`trendhunter-ingestion-cron`, `0 8 * * *` UTC) que ejecuta el pipeline completo sin intervención manual — añadido hoy mismo para que los datos no se queden obsoletos sin que nadie tenga que pulsar un botón.
- **Corrección del bug de mezcla de tendencias**: el emparejamiento de señales a tendencias existentes ahora se basa en identidad estable de fuente (`source_type` + `source_id`), no en adivinar el título — antes, dos repos de GitHub sin relación podían fusionarse en una sola tendencia si el heurístico de título coincidía. Se purgó la base de datos de producción y se re-ingirió limpia.
- **Rate limiting** en endpoints de ingestión (100 req/hora) y, desde ayer, también en el endpoint de solicitud de código de login (5 req/15 min) — antes cualquiera podía pedir códigos sin límite.
- **Bloqueo de abuso de trial**: un mismo email solo puede recibir el periodo de prueba de 7 días una vez; un segundo checkout con el mismo email se cobra inmediatamente sin trial. Además, ya no se puede abrir una segunda suscripción activa duplicada para el mismo email (409 si ya existe una activa/en trial).
- **Dashboard limpio de elementos de desarrollo**: se quitó la etiqueta "MVP Dashboard" y el panel de administración de ingestión (botones "Pull Hacker News", etc.) que antes eran visibles y clicables por cualquier cliente de pago — ahora la ingestión solo ocurre por el cron, nunca por acción de un cliente.
- **Legal real**: `/privacy` y `/terms` tienen la identidad legal real del fundador (autónomo en España, NIF, domicilio), no un placeholder.
- **Tests automatizados backend**: ~1.200 líneas de tests (`pytest`) cubriendo auth, beta, billing, ingestión de las tres fuentes, rate limiting y trends.
- **CI en GitHub Actions**: en cada push a `main`, corre tests de backend, lint y build de frontend, y un smoke test Playwright contra las URLs reales de producción de Railway.

## Parcialmente terminado

- **Producto/UX**: el dashboard es usable pero no ha pasado por una revisión de "primer uso" completa con ojos de usuario nuevo — el propio fundador ha señalado que, al entrar, no queda claro qué hacer primero. Esta revisión está pendiente (ver sección 17 y la sección de próximos pasos de esta conversación).
- **Seguridad**: hay auth para el dashboard, pero **no hay autorización real en varios endpoints críticos** — ver el hallazgo detallado en la sección 12, es importante.
- **Observabilidad**: Sentry está integrado en el código pero condicionado a que `SENTRY_DSN` esté configurado (sí lo está, y se ha usado activamente esta sesión para depurar un error real de Resend). Plausible está integrado condicionalmente vía `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`.
- **CI/CD**: el workflow de GitHub Actions existe y corre en cada push, pero el smoke test de Playwright **referencia botones que ya no existen en el dashboard** (se quitaron al eliminar el panel de administración) — es muy probable que este workflow esté en rojo ahora mismo. Ver sección 17.

## Pendiente / no implementado en absoluto

- **Ninguna llamada real a un LLM**: `OPENAI_API_KEY` y `ANTHROPIC_API_KEY` existen como variables de configuración pero no se usan en ningún servicio. El campo `ai_insights` de cada tendencia se genera con una plantilla de texto simple (ver sección 7), no con IA generativa.
- **Autenticación de equipos, roles o multi-usuario**: no existe.
- **Alertas, reportes PDF, favoritos/guardado de tendencias**: el modelo de datos ya tiene tablas para esto (`alerts`, `saved_trends`, `reports`) pero **cero endpoints las usan** — es esquema muerto a la espera de funcionalidad.
- **Búsqueda vectorial / embeddings de similitud**: existe la tabla `trend_embeddings` y variables `QDRANT_*`, pero no hay ninguna integración real con Qdrant ni generación de embeddings.
- **Rate limiting distribuido**: el limitador actual es en memoria, por proceso — funciona con una sola instancia del backend, se rompe (dejaría de limitar correctamente) si algún día se escala a más de un contenedor.
- **Panel de administración accesible**: el endpoint para listar beta signups existe y está protegido correctamente (falla cerrado sin `ADMIN_API_KEY`), pero esa variable no está configurada todavía en producción, así que hoy nadie puede consultar la lista de beta signups.
- **Cobro real de prueba fuera del propio fundador**: el modo live de Stripe se ha probado con la tarjeta del propio fundador, pero no con un cliente externo real todavía.

## Porcentaje aproximado de finalización

**Como MVP técnico desplegado y cobrando: ~92/100.**

Se parte del 90/100 documentado ayer y se suman los arreglos de seguridad, abuso de trial y limpieza de dashboard hechos hoy, pero se resta por el hallazgo nuevo de autorización en el endpoint de billing portal (sección 12) y el CI probablemente roto — ambos son reales y no estaban puntuados. Como **producto de mercado listo para escalar a cientos de clientes de pago sin supervisión manual constante**, la cifra realista es más baja, alrededor de **65-70/100**: falta autorización granular, observabilidad completa, y sobre todo, validación de que el producto retiene usuarios reales más allá del propio fundador.

---

# 3. Arquitectura

## Frontend

- **Next.js 16** (App Router, Server Components), **React 18.3.1**, **TypeScript 5.7.2**.
- Sin framework de CSS: CSS global propio (`globals.css`), sin Tailwind ni CSS-in-JS.
- La landing (`/`) es HTML estático inyectado vía `dangerouslySetInnerHTML` con interactividad añadida mediante un componente cliente (`LandingInteractions.tsx`) que maneja scroll, filtros, y el formulario de beta signup.
- Las páginas de producto (`/dashboard`, `/pricing`, `/login`, `/privacy`, `/terms`) son componentes React normales.
- El frontend **nunca llama directamente al backend desde el navegador** para nada mutante: todo pasa por un route handler propio de Next.js (`/api/backend/[...path]/route.ts`) que actúa de proxy inverso hacia el backend real, reenviando cookies y — solo para escrituras de ingestión — inyectando la cabecera `X-Ingestion-Key` con un secreto que vive únicamente en el servidor. Esto evita exponer la URL interna del backend o secretos al cliente y evita problemas de CORS.
- Deploy como contenedor Docker (`Dockerfile.frontend`), build multi-stage con salida `standalone` de Next.js.

## Backend

- **FastAPI** sobre **Python 3.11**.
- **SQLAlchemy 2.0** como ORM (estilo declarativo clásico, no el nuevo `Mapped[]`).
- **Pydantic v2** + `pydantic-settings` para validación de payloads y configuración.
- **Alembic** para migraciones (4 migraciones aplicadas: schema inicial, beta signups, subscriptions, login codes).
- Arquitectura en capas simples: `api/v1/*.py` (endpoints FastAPI) → `services/*.py` (lógica de negocio) → `models/base.py` (modelos SQLAlchemy). No hay repositorio/DAO intermedio real pese a lo que dice el README sobre "Repository pattern" — es aspiracional, en la práctica los servicios consultan la sesión de SQLAlchemy directamente.
- Middleware HTTP propio para rate limiting (no usa una librería como `slowapi`).
- Deploy como contenedor Docker (`Dockerfile.backend`): al arrancar corre `alembic upgrade head` y luego levanta Uvicorn.

## Base de datos

- **Producción**: PostgreSQL gestionado por Railway (`DATABASE_URL` apunta a `${{Postgres.DATABASE_URL}}`).
- **Desarrollo local**: SQLite por defecto (`sqlite:///./trendhunter.db`), con creación automática de tablas (`AUTO_CREATE_TABLES=true`) en vez de migraciones, por comodidad.
- **Riesgo latente**: no hay ninguna validación que impida arrancar en `ENVIRONMENT=production` con `DATABASE_URL` apuntando a SQLite — si alguna vez se despliega mal configurado, fallaría silenciosamente hacia un fichero SQLite local en el contenedor (efímero, se perdería en cada redeploy).

## APIs

Una única API REST versionada bajo `/api/v1/`, servida por el mismo proceso FastAPI, dividida en 5 routers: `trends`, `ingestion`, `beta`, `billing`, `auth`. Detalle completo en la sección 10.

## Servicios externos

| Servicio | Uso | Modo |
|---|---|---|
| Stripe | Checkout, portal de cliente, webhooks de suscripción | Live (real, cobra de verdad) |
| Resend | Envío de emails transaccionales (código de login) | Live |
| Meta Graph API (Conversions API) | Tracking de conversión server-side para Meta Ads | Live, verificado |
| GitHub REST API (búsqueda pública) | Fuente de señales de tendencias | Pública, sin token (opcional `GITHUB_TOKEN` para más rate limit) |
| Hacker News Firebase API | Fuente de señales de tendencias | Pública, sin autenticación |
| RSS/Atom (TechCrunch, Product Hunt, hnrss) | Fuente de señales de tendencias | Pública |
| Sentry | Error tracking del backend | Activo (`SENTRY_DSN` configurado) |
| Plausible | Analítica de producto privacy-first | Condicional a `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` |

## Hosting

**Railway**, como monorepo desplegado en (al menos) tres servicios independientes dentro del mismo proyecto:

- `trendhunter-backend` (root: `backend/`, Dockerfile: `Dockerfile.backend`)
- `trendhunter-frontend` (root: `frontend/`, Dockerfile: `Dockerfile.frontend`)
- `Postgres` (base de datos gestionada por Railway)
- `trendhunter-ingestion-cron` (mismo Dockerfile que el backend, pero con `cronSchedule: "0 8 * * *"` en vez de servir HTTP — ejecuta el script de ingestión y termina)

## Autenticación

Sistema propio, sin proveedor externo (pese a que existen variables `SUPABASE_*` sin usar). Passwordless por código de un solo uso:

1. El usuario introduce su email en `/login`.
2. El backend genera un código numérico de 6 dígitos, lo guarda **hasheado** (HMAC-SHA256 con `SECRET_KEY`) en la tabla `login_codes` con expiración de 10 minutos, y lo envía por email vía Resend.
3. El usuario introduce el código; el backend lo compara contra el hash (comparación de tiempo constante), y si es válido emite una cookie de sesión firmada con JWT (`trendhunter_session`, HttpOnly, `Secure` en producción, `SameSite=Lax`, expira en 60 minutos por defecto).
4. `GET /auth/me` decodifica esa cookie y devuelve el email y el estado de suscripción actual.

No hay contraseñas en ningún punto del sistema para clientes finales.

## Pagos

Stripe Checkout (modo `subscription`) + Stripe Customer Portal, ambos creados llamando a la API REST de Stripe directamente por HTTP con `httpx` (no se usa el SDK oficial `stripe-python`). El estado real de la suscripción vive en la tabla `subscriptions`, sincronizada exclusivamente a través de un webhook firmado (`checkout.session.completed`, `customer.subscription.created/updated/deleted`), verificando la firma HMAC de Stripe manualmente contra `STRIPE_WEBHOOK_SECRET`.

## Analytics

Plausible (analítica de producto, privacy-first, sin cookies) + Meta Pixel/CAPI (analítica de conversión publicitaria). No hay analítica de producto propia (no se registra qué hace cada usuario dentro del dashboard).

## Emails

Resend, solo para el código de login. No hay emails de bienvenida, de recordatorio de fin de trial, de recibo, ni de reactivación — todo eso lo gestiona Stripe de forma nativa (Stripe envía sus propios recibos y avisos de cobro) pero no hay ningún email propio del producto más allá del código de acceso.

## Infraestructura

Todo dockerizado. `docker-compose.yml` permite levantar backend + frontend + volumen persistente para SQLite en local, pero **no se usa en producción** (Railway no ejecuta `docker-compose.yml`, cada servicio se despliega por separado desde su propio Dockerfile).

## CI/CD

GitHub Actions (`.github/workflows/smoke.yml`), disparado en cada push a `main`: corre tests de backend con pytest, lint y build de frontend, y finalmente un smoke test end-to-end con Playwright **contra las URLs reales de producción** (`trendhunter-backend-production.up.railway.app` y el equivalente de frontend). No hay despliegue automático desde este workflow — el deploy real a Railway se dispara por separado (integración nativa de Railway con el repo de GitHub, o manualmente vía Railway CLI).

## Diagrama de arquitectura (texto)

```
                              ┌─────────────────────────────┐
                              │        Usuario final         │
                              │   (navegador, aitrendhunter  │
                              │          .app)               │
                              └───────────────┬──────────────┘
                                              │ HTTPS
                                              ▼
                        ┌───────────────────────────────────────┐
                        │     Railway: trendhunter-frontend       │
                        │  Next.js 16 (Docker, standalone)        │
                        │  - Landing, /pricing, /login,           │
                        │    /dashboard, /privacy, /terms         │
                        │  - Meta Pixel (cliente) + Plausible     │
                        │  - Proxy interno: /api/backend/[...]    │
                        │    (inyecta cookies + X-Ingestion-Key)  │
                        └───────────────┬──────────────────────┘
                                        │ HTTP interno (red privada Railway)
                                        ▼
                        ┌───────────────────────────────────────┐
                        │     Railway: trendhunter-backend        │
                        │  FastAPI (Docker)                       │
                        │  /api/v1/trends    (público, lectura)   │
                        │  /api/v1/ingestion (protegido por key)  │
                        │  /api/v1/beta      (público + admin)    │
                        │  /api/v1/billing   (Stripe checkout/    │
                        │                     portal/webhook)     │
                        │  /api/v1/auth      (login passwordless) │
                        │  - Rate limiting in-memory               │
                        │  - Meta CAPI (servidor) al recibir       │
                        │    webhooks de Stripe                    │
                        └───┬───────────┬───────────┬────────────┘
                           │           │           │
                           ▼           ▼           ▼
                    ┌──────────┐ ┌──────────┐ ┌─────────────┐
                    │ Postgres │ │  Stripe  │ │   Resend    │
                    │ (Railway)│ │  (Live)  │ │  (emails)   │
                    └──────────┘ └──────────┘ └─────────────┘
                           ▲
                           │ escribe trends / trend_sources /
                           │ agent_executions
                           │
                ┌──────────┴───────────────────────────┐
                │  Railway: trendhunter-ingestion-cron   │
                │  Mismo backend, sin servir HTTP         │
                │  Cron "0 8 * * *" UTC (diario)          │
                │  run_scheduled_ingestion.py:            │
                │   - GitHubCollector.collect()           │
                │   - HackerNewsCollector.collect()       │
                │   - RSSCollector.collect()               │
                │   - DetectorService.ingest_batch()      │
                └───────────┬──────────────┬─────────────┘
                            ▼              ▼
                     ┌────────────┐ ┌──────────────┐    ┌──────────────┐
                     │ GitHub API │ │ Hacker News  │    │  RSS feeds    │
                     │  (público) │ │ API (público)│    │ (TechCrunch,  │
                     └────────────┘ └──────────────┘    │ ProductHunt,  │
                                                          │ hnrss)        │
                                                          └──────────────┘

        Fuera del flujo de request, en cada evento de Stripe:
        Stripe webhook → backend → Meta Graph API (Conversions API)
        con email SHA-256 hasheado, para atribuir StartTrial/Purchase
        a la campaña de Meta Ads.

        Sentry recibe excepciones no controladas del backend.
```

## Patrones de diseño reales (no aspiracionales)

- Separación API / servicio / modelo, razonablemente limpia.
- Sin inyección de dependencias más allá de lo que da FastAPI (`Depends`).
- Sin colas, sin *background workers* reales (Celery está en las dependencias futuras planeadas pero no instalado ni usado).
- El "sistema de agentes" que menciona el README (Source Collector Agent, Noise Filter Agent, Trend Analyzer Agent, Opportunity Finder Agent, Competitor Watcher Agent, Report Generator Agent) es **una descripción de visión futura, no código real**. Hoy existe un único proceso llamado `DetectorService`, sin orquestación multiagente, sin LangGraph. Esto es importante para que quien lea este documento no asuma una sofisticación de "agentes de IA" que no existe todavía.

---

# 4. Stack tecnológico

## Backend (Python 3.11)

| Paquete | Versión | Para qué |
|---|---|---|
| fastapi | 0.109.0 | Framework web / API |
| uvicorn[standard] | 0.27.0 | Servidor ASGI |
| pydantic | 2.5.3 | Validación de datos |
| pydantic-settings | 2.1.0 | Configuración desde variables de entorno |
| sqlalchemy | 2.0.23 | ORM |
| psycopg2-binary | 2.9.9 | Driver de Postgres |
| alembic | 1.13.1 | Migraciones de base de datos |
| httpx | 0.25.1 | Cliente HTTP (Stripe, GitHub, HN, RSS, Meta, Resend) |
| requests | 2.31.0 | Cliente HTTP (uso puntual) |
| passlib[bcrypt] | 1.7.4 | Hashing de contraseñas (código muerto: no hay contraseñas en el flujo actual) |
| PyJWT | 2.8.0 | JWT (redundante con python-jose, ver nota abajo) |
| python-jose[cryptography] | 3.3.0 | Emisión/verificación real de JWT de sesión |
| cryptography | 41.0.7 | Dependencia de jose |
| python-multipart | 0.0.6 | Parsing de formularios |
| sentry-sdk | 1.39.1 | Error tracking |
| structlog | 24.1.0 | Logging estructurado (declarado, uso limitado en la práctica) |
| pytest / pytest-asyncio / pytest-cov / pytest-mock | 7.4.3 / 0.21.1 / 4.1.0 / 3.12.0 | Testing |
| black / isort / flake8 / mypy / pylint | — | Calidad de código (no hay evidencia de que se corran en CI) |

**Nota de limpieza pendiente**: `PyJWT` y `python-jose` están ambas instaladas pero solo `python-jose` se usa realmente (`app/core/security.py`). `passlib[bcrypt]` está instalada y tiene funciones (`hash_password`, `verify_password`) que **no las llama nadie** en el flujo actual, porque no hay contraseñas — es código muerto de un diseño de auth anterior al passwordless.

**No instalado, mencionado como "futuro" explícitamente en `requirements.txt`**: OpenAI/Anthropic SDKs, LangGraph/LangChain, Redis, Celery, Qdrant, Supabase SDK, SDK oficial de Stripe, clientes de Reddit/Product Hunt, Pandas/Numpy.

## Frontend (Node 22)

| Paquete | Versión |
|---|---|
| next | 16.2.7 |
| react / react-dom | 18.3.1 |
| typescript | 5.7.2 |
| @playwright/test | ^1.60.0 (dev, testing e2e) |

Sin librería de UI (no Tailwind, no shadcn, no MUI). Sin gestor de estado (no Redux/Zustand — no hace falta, todo es Server Components + `fetch` con `useState` local en los pocos componentes cliente).

## Servicios SaaS utilizados (no librerías, sino cuentas/servicios externos reales)

- Railway (hosting + Postgres + cron)
- Stripe (pagos, modo live)
- Resend (email transaccional, modo live)
- Meta Business (Ads Manager + Pixel + Conversions API)
- Sentry (error tracking)
- Plausible (analítica)
- Namecheap (registro de dominio, DNS)
- GitHub (repositorio de código + Actions para CI + fuente pública de datos)

---

# 5. Flujo completo del usuario

## 1. Landing (`/`)

Página de marketing estática (HTML embebido) con: hero con mockup del dashboard, sección de problema, sección "cómo funciona" (pipeline de 3 pasos), features, casos de uso, ejemplos de salida (cards de tendencias de muestra), y un formulario de **beta signup** (email + rol + intereses) que llama a `POST /api/v1/beta/signups`. Este formulario de beta es independiente del flujo de pago: captura interés, no da acceso.

Dos CTAs principales en la barra de navegación y el hero: **"Try 7 days free"** → `/pricing`, y **"View dashboard"** → `/dashboard` (que redirige a login si no hay sesión).

## 2. Registro / Pago (`/pricing`)

No existe un "registro" separado del pago: **crear cuenta = empezar a pagar**. El usuario introduce su email de facturación en el formulario de checkout (`PricingCheckout.tsx`), que llama a `POST /api/v1/billing/checkout`. El backend:

- Comprueba si ese email ya tiene una suscripción activa/en trial → si sí, error 409 (no se puede duplicar).
- Comprueba si ese email ha tenido *alguna* suscripción antes (aunque esté cancelada) → si es la primera vez, incluye 7 días de trial; si no, cobra inmediatamente sin trial.
- Crea una Stripe Checkout Session y devuelve la URL; el frontend redirige el navegador a Stripe.

**El usuario tiene que introducir una tarjeta de crédito real para empezar el trial** — no hay "prueba sin tarjeta". Esto fue una decisión de negocio consciente esta misma semana (ver sección 13) tras evaluar reducir fricción quitando la tarjeta, y se decidió mantenerla.

## 3. Login (`/login`)

Solo aplica a alguien que ya tiene una suscripción (activa, en trial, o cancelada). Es passwordless: email → código de 6 dígitos por email → verificación → cookie de sesión. Detallado en la sección 3 ("Autenticación").

## 4. Prueba gratuita

7 días, empieza en el momento del checkout (`subscription_data[trial_period_days]` en Stripe). Durante el trial, el usuario tiene acceso completo al dashboard (`has_active_subscription` es `true` para estados `active` y `trialing` por igual — no hay ninguna funcionalidad reservada solo para pago confirmado). Al terminar el trial, Stripe cobra automáticamente 39 € salvo cancelación previa desde el portal de cliente.

## 5. Dashboard (`/dashboard`)

Ver sección 6 para el detalle completo. En resumen: lista de tendencias filtrable + panel de detalle con el brief de la tendencia seleccionada + historial de ejecuciones del pipeline de ingestión (ahora automático, ya no accionable manualmente por el cliente).

## 6. Uso del producto

El usuario navega, filtra y lee tendencias. No hay ninguna acción de "uso" más allá de lectura y filtrado: no se puede guardar, exportar, comentar, ni configurar alertas (esas funcionalidades están en el modelo de datos pero no implementadas — ver sección 8).

## 7. Upgrade

No existe upgrade: hay un único plan (Pro, 39 €/mes). No hay tiers.

## 8. Pago

Gestionado 100% por Stripe Checkout. El backend nunca ve ni toca datos de tarjeta.

## 9. Renovación

Automática por Stripe cada mes mientras la suscripción esté `active` y no tenga `cancel_at_period_end=true`. El backend se entera de renovaciones vía el webhook `customer.subscription.updated`, que actualiza `current_period_end` en la tabla `subscriptions`.

## 10. Cancelación

El usuario pulsa "Manage billing" en el dashboard (`BillingPortalButton.tsx`) → `POST /api/v1/billing/portal` → se le redirige al Stripe Customer Portal, donde puede cancelar, cambiar tarjeta o ver facturas. Stripe notifica el cambio vía webhook (`customer.subscription.deleted` o `updated` con `cancel_at_period_end=true`), y el backend actualiza el estado. **Importante de seguridad**: ver sección 12 — este endpoint tiene un fallo de autorización real.

---

# 6. Dashboard

Hay una única pantalla de producto: `/dashboard` (Server Component de Next.js, `force-dynamic`, se re-renderiza en cada request).

## Estructura de la pantalla

**Cabecera (`topbar`)**: título "AI Trend Hunter", email del usuario logueado, botón "Manage billing" (abre el portal de Stripe).

**Resumen (`summary-grid`)**, 4 métricas calculadas en el momento a partir de las tendencias visibles con los filtros actuales:
- **Active trends**: número de tendencias que cumplen el filtro actual.
- **Top score**: el trend_score más alto entre las visibles.
- **Categories**: número de categorías distintas.
- **Total engagement**: suma de `engagement_count` de todas las tendencias visibles.

**Filtros (`filters`)**, formulario GET que recarga la página con query params:
- Búsqueda de texto libre (`q`, busca en título/descripción/resumen).
- Categoría (`category`, dropdown poblado dinámicamente desde `GET /trends/meta/categories`).
- Fuente (`source_type`, dropdown poblado desde `GET /trends/meta/sources`).
- Score mínimo (`min_score`, número 0-100).
- Botón "Clear filters" si hay algún filtro activo.

**Lista de tendencias (`trend-list`)**, columna izquierda: cada fila es un enlace (no un botón, así que preserva los filtros en la URL) mostrando el score con un color según umbral (`strong` ≥80, `good` ≥65, `watch` <65), título, badge "Verified" si `is_verified`, descripción, y chips con fuente principal, categoría, número de menciones y de engagement.

**Panel de detalle (`detail-panel`)**, columna derecha, muestra la tendencia seleccionada (por defecto la primera de la lista, o la que indique `?trend=slug`):
- Título y descripción completa.
- Tres scores en grid: Trend, Opportunity, Saturation.
- **AI insight**: un párrafo de texto (heurístico, no LLM — ver sección 7).
- **SaaS opportunities**: lista de 3 ideas de producto derivadas de la tendencia.
- **Source signals**: lista de cada fuente concreta (repo/historia/artículo) con su tipo, upvotes, comentarios y fecha.
- **Recent pipeline runs**: historial de las últimas ejecuciones del motor de ingestión (agente, señales procesadas/creadas/actualizadas, fecha, estado) — esto **hasta ayer era accionable por el cliente** (botones para disparar ingestión manualmente); hoy es solo lectura, porque se quitó el panel de administración del dashboard de cliente (ver sección 2).

## Lo que el usuario puede hacer hoy

- Buscar, filtrar y ordenar (por score) tendencias.
- Ver el detalle completo de una tendencia con toda su evidencia.
- Ver el historial de cuándo se actualizaron los datos.
- Gestionar su facturación (cancelar, cambiar tarjeta, ver facturas) vía el portal de Stripe.
- Cerrar sesión (endpoint existe: `POST /auth/logout`, aunque no hay botón visible de "logout" confirmado en el código de la UI actual — solo el link a billing portal en la topbar; **esto probablemente merece revisión de UX**).

## Lo que el usuario NO puede hacer (aunque parte del esquema de datos ya lo prevé)

- Guardar/marcar tendencias como favoritas.
- Configurar alertas por keyword o categoría.
- Descargar/exportar un reporte (PDF o cualquier formato).
- Invitar a un compañero de equipo.
- Cambiar su email o borrar su cuenta desde la UI (tendría que escribir al email de contacto).

---

# 7. Motor de detección de tendencias

Esta es la pieza más importante para entender qué es realmente el producto hoy, y es fundamental leerla con atención porque el nombre "AI Trend Hunter" puede sugerir un motor con IA generativa, y **no lo es**: es un sistema heurístico, determinista y basado en reglas, sin llamadas a ningún LLM.

## Qué datos analiza

Tres fuentes públicas, cada una traducida a un formato común (`SignalIngest`: título, contenido, tipo de fuente, URL, id de fuente, autor, upvotes, comentarios, shares, categoría, keywords, fecha de publicación):

1. **GitHub** (`GitHubCollector`): busca repositorios vía la API de búsqueda de GitHub (`GET /search/repositories`), con query por defecto `topic:ai stars:>50`, ordenados por estrellas. Traduce: nombre completo del repo → título, descripción → contenido, `stargazers_count` → upvotes, `open_issues_count` → comentarios, `forks_count` → shares, topics + lenguaje → keywords.
2. **Hacker News** (`HackerNewsCollector`): usa la API pública de Firebase de HN. Soporta feeds `top`, `new`, `best`, `ask`, `show`, `job`. Traduce: `score` → upvotes, `descendants` → comentarios, limpia HTML del texto del post.
3. **RSS/Atom** (`RSSCollector`): parsea feeds configurados (`techcrunch_startups`, `producthunt`, `hn_frontpage`). Como RSS no tiene votos reales, **estima** un número de upvotes según la antigüedad del artículo (48 si <24h, 36 si <72h, 24 si más antiguo) — es un proxy artificial, no una métrica real de popularidad.

## Cómo calcula tendencias (el algoritmo exacto)

Cada señal entrante pasa por `DetectorService._upsert_signal()`:

1. **Extracción de keywords**: combina keywords explícitas de la fuente con palabras inferidas del título+contenido (después de quitar ~90 *stop words* en inglés), quedándose con las 10 más frecuentes.
2. **Inferencia de categoría** (si la fuente no la da ya): compara las keywords contra diccionarios fijos de categoría (`ai_saas`, `developer_tools`, `privacy`, `product`, `marketing`, `startups`, `business`); si no hay coincidencia, cae en `"emerging"`.
3. **Generación del título de la tendencia**: distinto según la fuente. Para GitHub, usa el nombre del repo limpio de guiones. Para el resto, usa las primeras 5 palabras "significativas" del título original (quitando *stop words* y palabras genéricas como "ai", "saas", "startup"). Esto es relevante: **el título de la tendencia se genera automáticamente por heurística de texto, no lo escribe ni lo revisa nadie**, así que puede salir un título torpe o poco natural en casos límite.
4. **Emparejamiento con tendencia existente** (`_find_existing_trend`) — **esta es la lógica que se arregló hoy mismo**: primero busca si ya existe una `TrendSource` con el mismo `(source_type, source_id)` exacto — es decir, "¿ya vimos este repo/historia/artículo concreto antes?" — y si sí, la señal se adjunta a esa misma tendencia sin importar qué título adivinaría el heurístico esta vez. Solo si no hay coincidencia de fuente exacta, y **solo para fuentes que no sean GitHub**, cae a buscar por slug del título adivinado. Las señales de GitHub nunca hacen fallback por título: un repo es una entidad propia y nunca debe agruparse con otro repo solo porque el heurístico adivinó el mismo título. Antes de este arreglo, dos repos sin relación podían fusionarse en una sola tendencia si el heurístico de título coincidía por casualidad — esto pasó en producción y causó datos mezclados y confusos.
5. **Cálculo de scores** (`_recalculate_trend`), con constantes explícitas:

```
engagement = upvotes + comentarios×2 + shares×3
  (con suelo mínimo de 72 para señales RSS, que no tienen votos reales)

velocity   = min(35, engagement / 8)
breadth    = min(20, num_fuentes_distintas × 5)
recurrence = min(20, num_menciones × 4)
source_bonus = +12 si la señal es de GitHub, +8 si es RSS, +0 si es HN

trend_score = min(100, 25 [base] + velocity + breadth + recurrence + source_bonus)

saturation  = min(100, 15 [base] + num_fuentes×8 + num_menciones×3)

opportunity = clamp(0-100, trend_score + 12 [bonus] − saturation × 0.25)

momentum    = velocity  (redondeado)
```

6. **Generación del insight**: una única frase de plantilla fija:
   *"{título} is showing early signal across {N} source(s), with {M} mention(s) and a momentum score of {X}."*
   No hay generación de lenguaje natural real, es un `f-string`.

7. **Generación de oportunidades SaaS**: tres frases de plantilla fija con el nombre de la tendencia insertado:
   - *"Build a focused monitoring dashboard for {tendencia}"*
   - *"Create a lightweight workflow tool around {tendencia}"*
   - *"Package weekly opportunity reports for teams tracking {tendencia}"*
   Es decir: **las "ideas de negocio" que ve el cliente son genéricas y se repiten literalmente en estructura para cada tendencia**, solo cambia el nombre insertado. Esto es honesto de decir: hoy no hay generación de ideas realmente diferenciadas por tendencia.

## Qué IA utiliza

**Ninguna, ahora mismo.** Cero llamadas a OpenAI, Anthropic, o cualquier LLM. Todo el pipeline (extracción de keywords, categorización, scoring, generación de "insight" y "oportunidades") es reglas y plantillas de texto en Python puro. El nombre del producto y el marketing hablan de "AI-powered", lo cual es sostenible en tanto la propuesta de valor real es la curación y puntuación de señal pública — pero es importante que quien diseñe estrategia de producto/marketing sepa que hoy **no hay coste variable de IA por cliente ni por tendencia**, y que cualquier promesa de "insights generados por IA" en marketing es, estrictamente, generosa respecto a lo que hay hoy.

## Cómo se evita el ruido

- Lista de ~90 *stop words* en inglés para no dejar que palabras vacías dominen el título o las keywords.
- Lista de "palabras genéricas de título" (`ai`, `agent`, `code`, `saas`, `startup`...) que se evita usar como título completo de una tendencia si hay alternativa mejor.
- Limpieza de HTML/boilerplate en el contenido de RSS y HN (incluye un regex específico para quitar el patrón *"Discussion | Link"* típico de agregadores).
- Deduplicación de fuente por `(trend_id, source_type, source_id)` con constraint único en base de datos — la misma historia de HN no puede añadirse dos veces a la misma tendencia.

## Cómo se detectan tendencias "emergentes"

No hay una noción explícita de "emergente" vs. "establecida" más allá del propio `trend_score` y el campo `momentum` (que en la práctica es un alias redondeado de `velocity`, el mismo número que ya contribuye al score — no es una medida independiente de cambio en el tiempo). No hay series temporales, no hay comparación entre snapshots: cada vez que llega una nueva señal para una tendencia existente, se recalculan mentions/engagement/score **acumulativamente** sobre los valores ya guardados, así que el "momentum" de hoy no compara realmente "esta semana vs. la semana pasada" — es un proxy de la intensidad de la última señal recibida, no una derivada temporal real.

## Cómo se calculan las oportunidades

Ver fórmula arriba: `opportunity = trend_score + 12 − saturation × 0.25`. Conceptualmente: cuanto más saturado (más fuentes, más menciones acumuladas) más se penaliza la oportunidad, aunque el bonus fijo de +12 amortigua bastante ese castigo.

## Limitaciones conocidas del motor (para ser explícito con el lector de este documento)

1. **Sin ventana temporal real**: los scores son acumulativos desde que se creó la tendencia (hasta 90 días, `expires_at`), no una foto de "esta semana". Una tendencia vieja con muchas menciones acumuladas puede tener un score alto aunque ya no tenga actividad reciente.
2. **Sin IA real**: keywords, categoría, insight y oportunidades son heurística/plantilla, no comprensión semántica.
3. **RSS con métricas inventadas**: los "upvotes" de RSS son un número estimado por antigüedad, no una métrica real de popularidad del artículo.
4. **Categorización básica**: 7 categorías fijas por diccionario de palabras clave; cualquier tema fuera de esas listas cae en `"emerging"`, una categoría cajón de sastre.
5. **Sin verificación humana**: el campo `is_verified` existe en el modelo `Trend` pero no hay ningún flujo (manual ni automático) que lo active — siempre es `False`.
6. **Sin control de calidad de fuente**: si una fuente RSS empieza a publicar contenido de baja calidad o spam, no hay ningún filtro que lo detecte; entraría igual al pipeline.
7. **Escala limitada por diseño**: el detector corre en el mismo proceso que sirve HTTP (o, para el cron, en un script standalone) contra la misma base de datos transaccional — no hay cola, no hay procesamiento paralelo, no hay backpressure. Para 45 señales/día (15 por fuente) esto es más que suficiente; para un volumen de señales órdenes de magnitud mayor, este diseño no escalaría sin rediseño.

---

# 8. Funcionalidades

## Terminadas

- Ingesta de señales desde GitHub, Hacker News y RSS.
- Motor de scoring heurístico (trend/opportunity/saturation/momentum).
- Deduplicación y emparejamiento estable de señales a tendencias por identidad de fuente.
- Dashboard de lectura con filtros (texto, categoría, fuente, score mínimo).
- Detalle de tendencia con evidencia trazable.
- Historial de ejecuciones del pipeline.
- Autenticación passwordless por email.
- Suscripción de pago con trial único por email, checkout y portal de cliente Stripe.
- Bloqueo de suscripciones duplicadas activas.
- Landing pública + captura de interés de beta (independiente del pago).
- Tracking de conversión (Meta Pixel + CAPI) con StartTrial y Purchase.
- Rate limiting básico en ingestión y en solicitud de código de login.
- Cron de ingestión diaria automática sin intervención humana.
- Legal (privacidad/términos) con identidad real.

## En desarrollo / a medias

- Observabilidad completa (Sentry activo, pero sin alertas configuradas más allá de lo por defecto; Plausible activo pero sin dashboards de producto propios).
- Revisión de experiencia de primer uso del dashboard (identificada como pendiente por el propio fundador).

## Ideas futuras (mencionadas en README/docs, no empezadas)

- Insights generados con LLM real (OpenAI/Claude) — esto sería el salto de "heurística" a "IA de verdad".
- Alertas personalizadas por keyword/categoría/umbral de score.
- Reportes en PDF exportables.
- Búsqueda de similitud por embeddings vectoriales (Qdrant).
- Monitorización de competidores.
- Fuentes adicionales: Reddit, Product Hunt (vía API, no solo su feed RSS), YouTube, NewsAPI — hay variables de configuración reservadas (`REDDIT_CLIENT_ID`, `PRODUCTHUNT_TOKEN`, `YOUTUBE_API_KEY`, `NEWSAPI_KEY`) para todas estas, sin collector implementado.
- Colaboración por equipos / roles.
- Orquestación multiagente real (LangGraph) sustituyendo al `DetectorService` heurístico actual.
- Marketplace de datos / white-label (visión de fase 4, muy lejana).

---

# 9. Base de datos

PostgreSQL en producción (SQLite en local). 11 tablas definidas en el ORM, pero **solo 6 están realmente en uso** por el código actual. Esto es importante: hay bastante esquema "muerto", diseñado para funcionalidad futura que aún no existe.

## Tablas activas (usadas por endpoints reales hoy)

### `beta_signups`
Captura del formulario de interés en la landing. `id`, `email` (único), `role`, `interests` (JSON, lista de strings), `status` (default `"new"`, sin flujo que lo cambie todavía), `created_at`, `updated_at`.

### `subscriptions`
La fuente de verdad del estado de pago de cada cliente. `id`, `email`, `plan` (siempre `"pro"`, no hay otros planes), `status` (`trialing`/`active`/`canceled`/etc., viene literal de Stripe), `stripe_customer_id`, `stripe_subscription_id` (único), `stripe_checkout_session_id` (único), `current_period_end`, `trial_end`, `cancel_at_period_end`, timestamps. **No tiene foreign key a ninguna tabla de usuario** — el email es el único vínculo entre una suscripción y una identidad.

### `login_codes`
Códigos de acceso de un solo uso. `id`, `email`, `code_hash` (HMAC-SHA256, nunca se guarda el código en claro), `expires_at`, `consumed_at` (null hasta que se usa), `created_at`.

### `trends`
La tabla central del producto. `id`, `title`, `slug` (único), `description`, cuatro scores (`trend_score`, `opportunity_score`, `saturation_score`, `momentum`), `category`, `tags` (JSON), `keywords` (JSON), `content_summary`, `ai_insights` (texto de plantilla, ver sección 7), `saas_opportunities` (JSON, lista de 3 strings), `mentions_count`, `engagement_count`, `source_count`, `detected_at`, `last_updated_at`, `peak_at` (nunca se rellena en el código actual), `expires_at` (90 días desde detección), `is_active`, `is_verified` (siempre `False`, sin flujo que lo cambie).

### `trend_sources`
La evidencia detrás de cada tendencia. `id`, `trend_id` (FK), `source_type`, `source_url`, `source_id`, `title`, `content`, `author`, `upvotes`, `downvotes` (nunca se rellena, siempre 0), `comments`, `shares`, `published_at`, `fetched_at`. Constraint único en `(trend_id, source_type, source_id)` — evita duplicar la misma fuente en la misma tendencia.

### `agent_executions`
Log de cada corrida del pipeline de ingestión (manual histórico o del cron). `id`, `agent_name` (siempre `"mvp_heuristic_detector"` hoy), `agent_type`, `status` (`running`/`success`/`failed`), `input_params`/`output` (JSON), `error_message`, `started_at`, `completed_at`, `duration_seconds`, `records_processed/created/updated`, `created_trend_ids` (JSON).

## Tablas definidas en el ORM pero SIN NINGÚN endpoint que las use (esquema muerto/preparado)

- **`users`**: modelo completo de usuario con email, username, password hasheada, plan de suscripción, `is_admin`, etc. — **no lo usa ni un solo endpoint**. La identidad real de un cliente hoy es simplemente "un email con una fila en `subscriptions`", no una fila en `users`. Este modelo parece ser de un diseño de auth anterior (con contraseña) que se sustituyó por el passwordless sin limpiar el modelo viejo.
- **`alerts`**: alertas personalizadas por keyword/categoría/score mínimo. Sin endpoints.
- **`saved_trends`**: tendencias guardadas por usuario. Sin endpoints. Además depende de `users.id`, que tampoco se rellena nunca.
- **`trend_embeddings`**: para búsqueda de similitud vectorial. Sin generación de embeddings en ningún sitio.
- **`reports`**: reportes generados (PDF/JSON/HTML). Sin endpoints.

**Implicación práctica para quien planifique roadmap**: construir alertas, favoritos o reportes no arranca de cero en base de datos — el esquema ya existe — pero **sí requiere decidir primero cómo identificar a un usuario de verdad** (hoy no hay fila de usuario, solo email suelto), porque `alerts` y `saved_trends` dependen de `user_id` y esa tabla está vacía y desconectada del sistema de auth real.

## Relaciones

```
trends 1───N trend_sources
trends 1───N trend_embeddings   (sin uso real)
users  1───N alerts              (sin uso real, y "users" está vacía)
users  1───N saved_trends        (sin uso real)
```

`subscriptions` y `login_codes` **no tienen relación FK con nada** — se vinculan a todo lo demás únicamente por el string de email, sin integridad referencial.

---

# 10. APIs

Todas bajo prefijo `/api/v1`. Sin versión v2. Sin GraphQL. REST + JSON puro.

## `trends` (router `trends.py`) — sin autenticación, todo público

- `GET /trends` — lista tendencias activas. Query params: `q`, `category`, `source_type`, `min_score`, `limit` (máx 100), `skip` (paginación). Devuelve `list[TrendResponse]`.
- `GET /trends/meta/categories` — lista de categorías distintas presentes en la base de datos.
- `GET /trends/meta/sources` — lista de tipos de fuente distintos presentes.
- `GET /trends/{id_or_slug}` — detalle completo de una tendencia (incluye fuentes). 404 si no existe o no está activa.
- `POST /trends` — crea una tendencia manualmente con datos fijos (score 50, opportunity 50, saturation 20). **Sin ninguna protección** — cualquiera con la URL puede crear tendencias falsas en producción hoy. Ver sección 12.

## `ingestion` (router `ingestion.py`) — mutaciones protegidas por `X-Ingestion-Key`

- `GET /ingestion/runs` — últimas ejecuciones del pipeline (público, solo lectura).
- `GET /ingestion/rss/feeds` — feeds RSS configurados (público).
- `POST /ingestion/signals` — analiza un lote de señales arbitrarias (hasta 50) y crea/actualiza tendencias. Requiere `X-Ingestion-Key`.
- `POST /ingestion/demo` — corre un lote de señales de ejemplo fijo. Requiere key.
- `POST /ingestion/hackernews?feed=&limit=` — recoge de HN y procesa. Requiere key. 502 si HN falla.
- `POST /ingestion/rss?feed=&limit=` — recoge de un feed RSS y procesa. Requiere key. 502 si el feed falla, 400 si el feed no existe.
- `POST /ingestion/github?q=&limit=` — recoge de GitHub y procesa. Requiere key. 502 si GitHub falla.

## `beta` (router `beta.py`)

- `POST /beta/signups` — crea (o devuelve, si el email ya existe, marcando `already_registered=true`) un registro de interés en la beta. Público, sin protección — es intencional, es un formulario de landing.
- `GET /beta/signups` — lista todos los signups. Protegido por header `X-Admin-Key` contra `ADMIN_API_KEY`, y **falla cerrado**: si `ADMIN_API_KEY` no está configurada, deniega todo (nadie puede consultar, ni siquiera con la key vacía). Hoy esta variable no está configurada en producción, así que este endpoint está efectivamente inaccesible para todos, incluido el propio fundador.

## `billing` (router `billing.py`)

- `POST /billing/checkout` — recibe `{email}`, crea una Stripe Checkout Session (con o sin trial según histórico de ese email), devuelve `{checkout_url, session_id}`. Sin autenticación (es el punto de entrada de un cliente nuevo, tiene sentido que sea público).
- `POST /billing/portal` — recibe `{email}`, busca la suscripción de ese email y devuelve una URL de Stripe Customer Portal para gestionarla. **Sin verificar que quien hace la petición sea dueño de ese email** — ver hallazgo de seguridad crítico en la sección 12.
- `POST /billing/webhook` — recibe eventos de Stripe, verifica la firma HMAC manualmente contra `STRIPE_WEBHOOK_SECRET` (con margen de 5 minutos contra repetición), y actualiza `subscriptions` según el tipo de evento. También dispara los eventos de Meta CAPI (`StartTrial`, `Purchase`).

## `auth` (router `auth.py`)

- `POST /auth/request-code` — recibe `{email}`, genera y envía un código de 6 dígitos. Rate limited (5 cada 15 min por IP+ruta). En producción nunca devuelve el código en la respuesta (solo se envía por email); fuera de producción sí lo devuelve, para desarrollo local rápido.
- `POST /auth/verify-code` — recibe `{email, code}`, verifica contra los últimos 5 códigos no consumidos y no expirados de ese email, y si coincide, emite la cookie de sesión.
- `POST /auth/logout` — borra la cookie de sesión.
- `GET /auth/me` — devuelve `{email, subscription_status, has_active_subscription}` a partir de la cookie de sesión. 401 si no hay cookie válida.

## Endpoints de infraestructura (fuera de `/api/v1`)

- `GET /health` — healthcheck usado por Railway.
- `GET /` — metadata básica de la API.
- `GET /docs`, `GET /redoc` — Swagger/ReDoc, **deshabilitados automáticamente en producción** (`docs_url=None` si `is_production`).

---

# 11. Variables de entorno

Sin revelar ningún valor real — solo qué hace cada una y si está activa o pendiente en producción según la documentación interna del proyecto.

## Core

- `ENVIRONMENT`: `development` o `production`; controla validaciones de seguridad estrictas y si Swagger está expuesto.
- `DEBUG`: modo debug de FastAPI.
- `API_PORT` / `API_HOST`: bind del servidor (Railway inyecta `PORT` automáticamente, usado en el `CMD` del Dockerfile).

## Base de datos

- `DATABASE_URL`: cadena de conexión. En Railway apunta a la referencia nativa `${{Postgres.DATABASE_URL}}`. En local, SQLite por defecto.
- `DATABASE_ECHO`: si se loguean las queries SQL (debug).
- `DATABASE_POOL_SIZE` / `DATABASE_MAX_OVERFLOW`: tamaño del pool de conexiones (solo aplica a Postgres, SQLite lo ignora).
- `AUTO_CREATE_TABLES`: `true` crea tablas automáticamente al arrancar (solo local); `false` en Docker/producción, donde Alembic gestiona el esquema.

## Autenticación y seguridad

- `JWT_SECRET`: firma tokens (heredado de un diseño anterior; el sistema de sesión real usa `SECRET_KEY`, no esta — posible resto sin limpiar).
- `SECRET_KEY`: firma la cookie de sesión JWT y el hash HMAC de los códigos de login. **Crítica**: si se filtra, se pueden falsificar sesiones y códigos.
- `ALGORITHM`: algoritmo JWT (`HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES` / `REFRESH_TOKEN_EXPIRE_DAYS`: existen pero pertenecen a un flujo de refresh token que no está conectado a ningún endpoint activo.
- `SESSION_TIMEOUT_MINUTES`: duración real de la cookie de sesión del passwordless (60 min por defecto).
- `CORS_ORIGINS`: lista de orígenes permitidos, separados por coma; en producción debe ser el dominio real del frontend.
- `INGESTION_API_KEY`: secreto compartido entre el frontend (route handler proxy) y el backend para autorizar escrituras de ingestión.
- `ADMIN_API_KEY`: protege el listado de beta signups. **No configurada en producción todavía.**
- `AUTH_CODE_RATE_LIMIT_REQUESTS` / `AUTH_CODE_RATE_LIMIT_PERIOD`: límite de solicitudes de código de login (5 cada 900s por defecto).
- `RATE_LIMIT_ENABLED` / `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_PERIOD`: límite general de escrituras de ingestión (100/hora por defecto).

## Fuentes de datos

- `GITHUB_API_URL`, `GITHUB_TOKEN` (opcional, mejora rate limit), `GITHUB_DEFAULT_LIMIT`, `GITHUB_SEARCH_QUERY`.
- `HACKERNEWS_API_URL`, `HACKERNEWS_DEFAULT_LIMIT`.
- `RSS_DEFAULT_FEED`, `RSS_FEED_URLS` (formato `clave=url,clave=url`).
- Reservadas sin collector implementado: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`, `PRODUCTHUNT_TOKEN`, `YOUTUBE_API_KEY`, `NEWSAPI_KEY`.

## Email

- `RESEND_API_KEY`: clave de Resend. Configurada en producción (live).
- `SENDER_EMAIL`: remitente de los emails transaccionales.

## Billing

- `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRO_PRICE_ID`: credenciales live de Stripe, configuradas.
- `STRIPE_API_URL`: base de la API de Stripe (permite apuntar a un mock en tests).
- `BILLING_TRIAL_DAYS`: días de trial (7).
- `APP_URL`: URL pública usada para construir las URLs de éxito/cancelación de Stripe y el `event_source_url` de Meta CAPI.

## Marketing / Analítica

- `META_PIXEL_ID`, `META_CAPI_ACCESS_TOKEN`, `META_GRAPH_API_URL`: tracking de conversión de Meta Ads, configurado y verificado.
- `NEXT_PUBLIC_META_PIXEL_ID`: igual que `META_PIXEL_ID` pero expuesto al cliente (necesario para el script del Pixel).
- `PLAUSIBLE_DOMAIN` / `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` / `ANALYTICS_ENABLED`: analítica de producto.

## LLM (declaradas, sin uso real — ver sección 7)

- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `LLM_MODEL`, `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `MOCK_LLM_RESPONSES`.

## Infraestructura futura (declaradas, sin uso real)

- `REDIS_URL`, `QDRANT_URL`, `QDRANT_COLLECTION_NAME`, `QDRANT_VECTOR_SIZE`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `CELERY_WORKER_CONCURRENCY`.
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SECRET_KEY`: declaradas, el sistema de auth real no las usa.

## Observabilidad

- `SENTRY_DSN`: si está presente, activa Sentry automáticamente; si no, queda desactivado sin romper nada. Configurado en producción.
- `LOG_LEVEL`, `ENABLE_STRUCTURED_LOGGING`.

## Feature flags declarados (sin lógica condicional real detrás en el código actual)

- `ENABLE_AGENT_SCHEDULING`, `ENABLE_VECTOR_SEARCH`, `ENABLE_PDF_REPORTS`, `ENABLE_SLACK_ALERTS`: existen como booleanos de configuración pero no hay código que los lea para activar/desactivar nada — son aspiracionales.

## Frontend específicas

- `NEXT_PUBLIC_API_URL`: URL pública del backend, usada por el navegador y por el proxy del servidor si `API_URL` no está definida.
- `API_URL`: URL del backend usada solo server-side por el proxy (puede ser la URL interna de red privada de Railway, más rápida y sin salir a internet).
- `INGESTION_API_KEY` (en el frontend): la misma clave que en el backend, usada por el proxy para inyectar la cabecera en escrituras de ingestión.

---

# 12. Seguridad

## Autenticación

Sólida para lo que cubre: passwordless por email con código de un solo uso, hash HMAC-SHA256 de los códigos (nunca en claro en base de datos), comparación en tiempo constante (`hmac.compare_digest`), cookie de sesión `HttpOnly` + `Secure` en producción + `SameSite=Lax`, expiración corta (60 min). No hay contraseñas que puedan filtrarse en una brecha de datos.

## Autorización — **aquí hay un hallazgo de seguridad real que se ha detectado escribiendo este documento y que merece atención inmediata**

**`POST /api/v1/billing/portal` no verifica que quien hace la petición sea el dueño del email que envía en el body.** El endpoint recibe `{email}`, busca si ese email tiene una suscripción con `stripe_customer_id`, y si la tiene, **genera y devuelve una URL real y funcional del Stripe Customer Portal para esa suscripción** — sin comprobar la cookie de sesión, sin comprobar que el email del body coincida con el email de la sesión activa. Esto significa: **cualquiera que conozca o adivine el email de un cliente de pago puede obtener un enlace que le permite ver sus facturas, cambiar su método de pago o cancelar su suscripción**, sin necesidad de tener acceso a esa bandeja de entrada. En la UI normal esto no se nota porque el botón "Manage billing" siempre envía el email de la sesión ya autenticada — pero el endpoint del backend en sí no impone ese vínculo, y es alcanzable directamente. Esto se debería arreglar antes de escalar campañas de adquisición: comprobar `email == session.email` (usando la cookie `trendhunter_session` ya disponible) antes de generar el portal.

Más allá de esto:

- `POST /api/v1/trends` (crear tendencia manualmente) **no tiene ninguna protección** — a diferencia de los endpoints de `/ingestion`, no requiere `X-Ingestion-Key`. Cualquiera puede insertar tendencias falsas en producción hoy.
- Todos los `GET /api/v1/trends*` son públicos por diseño (no hace falta estar logueado para verlos vía API directa, aunque el dashboard sí exige sesión) — esto es en la práctica una fuga: **cualquiera con la URL del backend puede leer el catálogo completo de tendencias sin pagar**, saltándose por completo el paywall del dashboard. El paywall solo protege la experiencia del dashboard de Next.js, no la API subyacente.

## Protecciones existentes

- **Rate limiting**: en memoria, por IP+ruta, sobre escrituras de `/ingestion/*` (100/hora) y sobre `/auth/request-code` (5/15min). **Debilidad conocida**: confía en la cabecera `X-Forwarded-For` sin validar que venga de un proxy de confianza — un atacante puede falsificarla para evadir el límite.
- **Verificación de firma de webhooks de Stripe**: implementada a mano (no con el SDK oficial), con comprobación de timestamp (rechaza firmas de más de 5 minutos) para mitigar repetición.
- **Secretos inseguros bloqueados en arranque**: si `ENVIRONMENT=production` y `JWT_SECRET` o `SECRET_KEY` siguen en su valor por defecto, la aplicación **no arranca** (falla explícitamente al iniciar).
- **CORS restringido**: métodos y cabeceras explícitos (no `*`), orígenes desde `CORS_ORIGINS`.
- **Swagger/ReDoc deshabilitados en producción.**
- **Validaciones de entrada**: Pydantic con longitudes y patrones (regex de email) en los payloads públicos (`SignalIngest`, `BetaSignupCreate`, etc.).

## Validaciones ausentes o débiles (documentadas también en `docs/AUDIT.md`, una auditoría interna previa)

- `source_type` en `SignalIngest` acepta cualquier string de 2-40 caracteres — no está restringido a una lista cerrada de fuentes válidas.
- `source_url` acepta cualquier string, no se valida como URL real.
- Sin manejo explícito de errores de conexión a base de datos (un fallo de Postgres devolvería un 500 genérico, no un 503 controlado).
- Sin CSRF: dado que las mutaciones no dependen de la cookie de sesión para autorizar (excepto la lectura de `/auth/me`), el riesgo práctico es bajo hoy, pero merece revisión si se añade más lógica atada a sesión.

---

# 13. Modelo de negocio

## Precio

**39 €/mes**, plan único ("Pro"), sin niveles ni descuentos anuales todavía. Se permiten códigos de promoción de Stripe (`allow_promotion_codes: true` en el checkout) aunque no hay ninguno creado activamente que se sepa.

## Prueba gratuita

7 días, **con tarjeta obligatoria desde el primer momento**. Esta fue una decisión explícita tomada esta semana: se planteó quitar la tarjeta para reducir fricción de entrada, pero se decidió mantenerla para evitar registros de baja calidad y abuso. El trial solo se concede **una vez por email** — un segundo intento con el mismo email se cobra de inmediato, sin trial.

## Suscripciones

Mensual, recurrente, gestionada íntegramente por Stripe (cobro, dunning de pagos fallidos, facturas, impuestos si Stripe Tax estuviera activado — no hay evidencia en el código de que lo esté). Cancelación en cualquier momento desde el portal de cliente, efectiva al final del periodo ya pagado (`cancel_at_period_end`).

## Costes (estimación basada en la infraestructura real observada, no en facturas reales que no son visibles desde el código)

- **Railway**: 3-4 servicios (backend, frontend, Postgres, cron) — coste bajo, probablemente en el rango de $20-50/mes en el plan Hobby/Pro de Railway para este volumen.
- **Stripe**: comisión estándar (~1,5% + 0,25€ en la UE para tarjetas europeas, más para tarjetas fuera de la UE) sobre cada cobro de 39€.
- **Resend**: nivel gratuito probablemente suficiente para el volumen actual (códigos de login son el único email enviado).
- **Sentry / Plausible**: niveles gratuitos o de entrada, bajo volumen.
- **Meta Ads**: presupuesto de campaña, decidido por el fundador (rango bajo, ~300-500€/mes según la conversación de esta sesión).
- **Sin coste de LLM**: cero, porque no hay llamadas a modelos de IA en el pipeline (ver sección 7) — esto es una ventaja de margen importante que quien diseñe estrategia de precios debería tener en cuenta: **el coste marginal por cliente es prácticamente cero** más allá de la comisión de Stripe.

## Margen

Con coste marginal casi nulo por cliente (sin LLM, sin infraestructura que escale linealmente con clientes en el rango actual), el margen bruto por suscripción de 39€ es muy alto una vez cubiertos los costes fijos de infraestructura (~50-100€/mes total). El punto de equilibrio de los costes fijos se alcanza con muy pocos clientes de pago (2-3 suscripciones ya cubrirían Railway+Resend+Sentry+Plausible).

## Hipótesis de negocio no validadas todavía

- Que founders/indie hackers paguen 39€/mes de forma sostenida por señal de tendencias sin verificar retención más allá de un mes.
- Que el valor percibido del motor heurístico actual (sin IA generativa real) sea suficiente para justificar el precio frente a alternativas gratuitas (GitHub Trending, HN directamente).
- Que la adquisición vía Meta Ads sea rentable dado el ticket de 39€/mes (LTV desconocido todavía, cero clientes externos confirmados a fecha de este documento).

## Métricas esperadas / objetivo declarado por el fundador

El objetivo explícito comunicado en esta conversación es **llegar a 100 clientes de pago (facturando de verdad) lo antes posible**, no solo 100 registros de interés en la beta. A 39€/mes, 100 clientes = 3.900€/mes de MRR.

---

# 14. Marketing

## Landing

Una sola página (`/`), en inglés, con estructura clásica de SaaS B2B: hero con mockup de producto, problema, cómo funciona (pipeline de 3 pasos), features, casos de uso, ejemplos de salida reales (cards de tendencias), y formulario de captura de interés de beta. No hay blog, no hay páginas de comparación con competidores, no hay páginas de landing por keyword/SEO.

## SEO

Básico: metadata de Next.js (`title`, `description`, Open Graph) en cada página, `metadataBase` apuntando al dominio real. No hay evidencia de sitemap.xml, robots.txt, structured data (JSON-LD), ni contenido de blog para SEO orgánico de cola larga. Esto es una brecha si el canal de adquisición a largo plazo debe incluir orgánico/SEO.

## Meta Ads

Campaña configurada (no publicada hasta que el fundador decida lanzarla) en Meta Business Manager, cuenta "Duskwell". Solo Facebook + Instagram (no Audience Network), objetivo "Tráfico a la web", presupuesto bajo (~300-500€/mes según lo discutido). Tracking verificado de punta a punta: Pixel cliente (`PageView`) + Conversions API servidor (`StartTrial`, `Purchase`) con deduplicación por `event_id` de Stripe y hash SHA-256 del email para cumplir con los requisitos de datos de Meta.

## Google Ads

No hay ninguna integración ni tracking de Google Ads en el código (no hay Google Tag, no hay Google Ads Conversion API). Si se quisiera este canal, habría que construirlo desde cero, análogo a lo que se hizo con Meta.

## Newsletter

No existe ninguna infraestructura de newsletter (no hay integración con Substack, Beehiiv, ni un sistema de envío de emails periódicos de contenido — Resend solo se usa para el código de login transaccional).

## Contenido

No hay blog ni sistema de contenido en el repositorio. Toda la "prueba de producto" ante un visitante nuevo se limita a los ejemplos estáticos embebidos en la landing (3 tarjetas de tendencias de muestra, con datos ficticios ilustrativos, no datos reales del sistema en vivo).

## Afiliados / Referidos

No implementado. No hay tabla de datos, ni lógica de tracking de referidos, ni programa de afiliados en ningún punto del código.

## Roadmap de adquisición (estado real, no aspiracional)

Según lo discutido en esta misma sesión de trabajo con el fundador:
- **Orgánico (Show HN, Reddit, IndieHackers)**: ya intentado en una sesión anterior, pero el fundador reportó no poder interactuar en varios foros por posible detección de spam — es decir, **el canal orgánico ya tiene fricción real conocida**, no es un canal "listo para usar".
- **Meta Ads**: configurado y con tracking verificado, pendiente de decisión de lanzamiento por parte del fundador.
- **Beta privada por email**: hay una lista de interesados capturada vía `beta_signups`, pero **inaccesible hoy** porque `ADMIN_API_KEY` no está configurada en producción (ver secciones 2 y 11) — el fundador literalmente no puede ver hoy quién se ha apuntado a la beta sin configurar esa variable primero.

---

# 15. Competidores

Este SaaS compite en el espacio de "descubrimiento de oportunidades de producto/mercado", un espacio con jugadores establecidos que conviene conocer antes de posicionar la propuesta de valor. (Análisis basado en conocimiento general de mercado, no en investigación en vivo de este momento — conviene verificar precios y features actuales antes de usarlo en materiales de venta.)

## Quiénes son

- **Exploding Topics**: el competidor más directo en "descubrir tendencias antes de que exploten". Usa señal de búsqueda y menciones, no señal de código/desarrollo.
- **Glimpse**: similar, capa de datos de tendencias de búsqueda con más granularidad temporal que Google Trends.
- **GitHub Trending (gratis, nativo de GitHub)**: la fuente más directa de "qué repos están creciendo" — gratis, sin scoring de oportunidad de negocio, sin agregación con otras fuentes.
- **Hacker News / Algolia HN Search (gratis)**: acceso directo a la misma fuente que usa AI Trend Hunter, sin curación ni scoring.
- **Newsletters curadas manualmente** (Lenny's Newsletter, Trends.vc, Starter Story, etc.): curación humana de alta calidad, pero lenta (semanal) y sin trazabilidad de evidencia por señal.
- **GummySearch / similar herramientas de "escucha social" para founders**: se centran en Reddit, más orientadas a validar dolor de usuario que a detectar señal de desarrollo.

## Fortalezas de los competidores

- Marca y confianza establecidas (especialmente Exploding Topics, con años de contenido público).
- Newsletters curadas manualmente tienen mejor calidad de "insight" que cualquier heurística automática hoy — un editor humano razona mejor que una plantilla de texto.
- Herramientas gratuitas (GitHub Trending, HN) tienen cero fricción de precio, aunque cero curación.

## Debilidades de los competidores

- Ninguno de los mencionados combina explícitamente **GitHub + Hacker News + RSS con trazabilidad de evidencia por tendencia** en un solo producto con scoring numérico transparente.
- Las herramientas basadas en búsqueda/social (Exploding Topics, Glimpse) llegan estructuralmente más tarde que la señal de código — cuando algo ya se busca mucho en Google, probablemente ya hay competencia.
- Las newsletters curadas manualmente no escalan ni se personalizan por categoría de interés del lector.

## Ventajas competitivas reales de AI Trend Hunter (hoy, no aspiracionales)

- Señal de desarrollo temprana (GitHub) combinada con discusión técnica (HN) — nadie identificado combina ambas con evidencia trazable por defecto.
- Precio de entrada relativamente bajo (39€/mes) frente a herramientas de inteligencia de mercado B2B tradicionales, que suelen ser más caras.
- Cada score es auditable hasta su fuente concreta — no es una caja negra.

**Advertencia honesta**: la ventaja competitiva de "IA" que sugiere el nombre del producto no existe todavía de forma diferenciada frente a alternativas gratuitas si el motor heurístico se percibe como poco sofisticado tras el uso — el riesgo real de churn frente a la competencia gratuita (GitHub Trending + HN directamente) depende de cuánto valor perciba el cliente en el scoring y la agregación frente a simplemente mirar las fuentes él mismo.

---

# 16. Roadmap

## Próximos 30 días (lo inmediatamente accionable dado el estado actual)

1. Arreglar el fallo de autorización del endpoint de billing portal (sección 12) — es el ítem más urgente de seguridad antes de escalar adquisición de pago.
2. Arreglar el smoke test de Playwright roto (referencia botones que ya no existen en el dashboard tras quitar el panel de administración) — el CI en GitHub Actions probablemente está en rojo ahora mismo.
3. Configurar `ADMIN_API_KEY` en producción para poder consultar la lista de beta signups.
4. Revisión de experiencia de primer uso del dashboard (ya identificada como pendiente por el fundador: "abres la aplicación y casi no sabes ni por dónde meterle mano").
5. Decidir y ejecutar el lanzamiento de la campaña de Meta Ads (ya configurada y con tracking verificado, solo falta la decisión de publicarla).
6. Confirmar que el cron de ingestión diaria (recién creado) funciona de forma fiable varios días seguidos antes de depender de él sin supervisión.
7. Hacer un cobro real de prueba con un cliente externo (no el propio fundador) para validar el flujo live de punta a punta.

## Próximos 90 días

- Retomar el canal orgánico (Show HN, Reddit, IndieHackers) resolviendo la fricción de moderación/spam ya detectada.
- Validar retención real: ¿los primeros clientes de pago siguen suscritos al segundo/tercer mes?
- Evaluar si el motor heurístico necesita evolucionar hacia insights generados por LLM real para sostener el precio de 39€/mes frente a alternativas gratuitas.
- Cerrar el hueco de autorización en `POST /api/v1/trends` (creación pública sin protección) y considerar si `GET /api/v1/trends*` debería exigir sesión para no filtrar el catálogo completo por API sin pagar.
- Migrar el rate limiting a algo distribuido (Redis) si el tráfico lo justifica.
- Decidir el destino del esquema muerto (`users`, `alerts`, `saved_trends`, `reports`, `trend_embeddings`): o se empieza a construir sobre él (alertas, favoritos) o se limpia para reducir complejidad.

## Próximos 12 meses

- Si la retención valida el modelo: construir alertas personalizadas y reportes exportables (el esquema de datos ya está listo, falta la lógica y la UI).
- Evaluar seriamente la incorporación de un LLM real para insights diferenciados por tendencia, con control de coste (hoy el margen es altísimo precisamente porque no hay coste de IA; cualquier LLM real cambia esa ecuación y debe diseñarse con cuidado).
- Explorar fuentes adicionales ya contempladas en configuración pero sin collector (Reddit, Product Hunt vía API real, YouTube, NewsAPI).
- Si el volumen de clientes lo justifica, introducir tiers de precio (hoy solo hay un plan).
- Reconsiderar identidad de usuario real (tabla `users` conectada de verdad) si se necesita cualquier funcionalidad multi-dispositivo, multi-usuario o de equipo.

---

# 17. Problemas conocidos

## Bugs activos / regresiones probables

1. **CI probablemente roto**: el smoke test de Playwright (`frontend/tests/e2e/smoke.spec.ts`) espera botones ("Run demo ingestion", "Pull Hacker News", "Pull RSS", "Pull GitHub") que se eliminaron del dashboard hoy mismo al quitar el panel de administración. El workflow de GitHub Actions corre este test contra producción en cada push a `main`. Es muy probable que el último push haya dejado el CI en rojo. Esto no afecta a los clientes reales (el dashboard funciona bien sin esos botones), pero rompe la señal de "todo verde" del pipeline de CI y debería arreglarse (actualizar o eliminar ese test) cuanto antes.
2. **Fallo de autorización en `POST /api/v1/billing/portal`**: detallado en la sección 12. Es el hallazgo más serio de esta revisión.
3. **`POST /api/v1/trends` sin protección**: cualquiera puede insertar tendencias falsas directamente contra la API de producción.
4. **API de tendencias completamente pública**: el paywall del dashboard no protege la API subyacente — cualquiera puede leer el catálogo completo de tendencias sin pagar, con una petición HTTP directa al backend.

## Limitaciones de diseño conocidas (no son "bugs" per se, pero son riesgos si se ignoran al escalar)

- Rate limiting en memoria, por proceso — no sobrevive a un reinicio ni funciona correctamente con más de una instancia del backend.
- `x-forwarded-for` no se valida contra una lista de proxies de confianza, así que es falsificable para evadir el rate limit.
- Sin manejo explícito de caída de base de datos (devolvería 500 genérico).
- `source_type` y `source_url` sin validación estricta de formato.

## Deuda técnica

- Esquema de base de datos con 5 tablas sin ningún uso real (`users`, `alerts`, `saved_trends`, `reports`, `trend_embeddings`) — confunde a cualquiera que lea el modelo de datos pensando que esas funcionalidades ya existen.
- Dos librerías de JWT instaladas (`PyJWT` y `python-jose`) cuando solo una se usa.
- `passlib[bcrypt]` instalada con funciones de hash de contraseña que no llama nadie (el sistema es passwordless).
- Existía un `Dockerfile.frontend` duplicado en dos ubicaciones distintas del repo (`frontend/Dockerfile` y `Dockerfile.frontend` en la raíz) con contenido divergente — Railway solo construye desde el de la raíz; el otro es un duplicado obsoleto que puede confundir a quien edite variables de build de Docker sin saberlo (ya ha causado un despliegue fallido real en esta misma sesión de trabajo, al editarse por error el fichero equivocado).
- El README describe una "arquitectura multiagente" (6 agentes especializados) y patrones "Repository pattern"/"Domain-Driven Design" que no reflejan el código real, mucho más simple — riesgo de que alguien nuevo en el proyecto (o un lector de este mismo documento) sobreestime la sofisticación técnica actual si lee el README en vez del código.

## Riesgos de negocio (no técnicos, pero relevantes para quien diseñe estrategia)

- Cero clientes de pago externos confirmados a fecha de este documento — el único checkout real de prueba fue del propio fundador.
- La promesa de marketing "AI-powered" no se sostiene técnicamente hoy con una inspección de código (no hay LLM) — riesgo reputacional si un cliente técnico audita el producto y lo señala públicamente.
- Dependencia total de tres fuentes públicas gratuitas sin SLA (GitHub, HN, RSS externos) — si alguna cambia su API o empieza a bloquear el scraping/consumo, el pipeline se degrada sin aviso más allá de los logs de error.

---

# 18. Auditoría crítica

*(Actuando como inversor de Y Combinator revisando este proyecto antes de una posible ronda pre-seed.)*

## Lo bueno

- **El fundador ha demostrado velocidad de ejecución real**: dominio propio, Stripe live, Resend live, tracking de ads verificado de punta a punta, y una sesión completa dedicada a cazar y arreglar bugs de producción reales (suscripciones duplicadas, abuso de trial, falta de rate limiting) en vez de ignorarlos. Eso es una señal fuerte de disciplina operativa poco común en un MVP en solitario.
- **El insight de producto es real y defendible**: mirar señal de código antes que cobertura mediática es una tesis correcta y con timing razonable, dado el ritmo actual de creación de repos/herramientas IA.
- **El pricing y el trial están bien pensados para evitar abuso** (una sola vez por email, tarjeta obligatoria) — señal de que el fundador piensa en unit economics desde el día uno, no solo en crecimiento vanidoso.
- **El coste marginal por cliente es prácticamente cero** (sin LLM, sin infraestructura pesada) — esto da un margen envidiable si se valida la demanda.

## Lo malo

- **Cero validación externa de willingness-to-pay.** Todo el aprendizaje de "esto funciona" viene de una única transacción hecha por el propio fundador. Antes de gastar en ads, YC preguntaría: ¿ha hablado con 20 indie hackers reales sobre si pagarían 39€/mes por esto, o se ha construido primero y se pregunta después?
- **La propuesta de "IA" no está respaldada por el producto.** Si el canal de adquisición es gente técnica (indie hackers, HN), en el momento en que alguien mire de cerca el producto y note que no hay LLM detrás de "AI Trend Hunter", el golpe de credibilidad puede ser real. Esto no es necesariamente malo — un motor heurístico honesto puede ser un producto perfectamente vendible — pero el naming y el marketing actuales prometen más de lo que hay.
- **Fallo de seguridad real y explotable en producción** (billing portal sin verificación de propiedad de email) — en un review de YC esto sería una bandera roja inmediata sobre el rigor del proceso de shipping, aunque se haya originado por prisa de MVP, no por negligencia.
- **El "brief de oportunidad SaaS" — el entregable central prometido en el marketing — es hoy tres frases de plantilla con el nombre de la tendencia insertado.** Esto es lo más importante que un inversor señalaría: **el producto no cumple todavía la promesa de valor más específica que hace en su propia landing** ("SaaS opportunity briefs... who, why now, and where the gap is"). Hoy ese "quién, por qué ahora, dónde está el hueco" no se genera de verdad, es texto fijo.
- **CI probablemente roto ahora mismo** por un cambio reciente no reflejado en los tests — señal de que falta un hábito de "actualizar tests cuando cambia la UI", normal en solitario pero peligroso si no se corrige pronto.

## Qué mejoraría

1. Escribir de verdad los "briefs" de oportunidad — aunque sea con una llamada a un LLM barato solo para las tendencias top (no para todas, para controlar coste), en vez de plantilla fija. Es el gap más grande entre promesa y producto.
2. Arreglar la autorización del billing portal antes de cualquier otra cosa relacionada con crecimiento — es el único hallazgo de esta lista con impacto directo y potencial en clientes reales de pago.
3. Hablar con 15-20 personas del público objetivo (indie hackers, PMs) antes de gastar el presupuesto de ads, específicamente enseñándoles el dashboard real (no la landing) y preguntando si pagarían — validar deseabilidad antes de acelerar adquisición.
4. Decidir conscientemente si "AI" en el nombre se sostiene con roadmap real a 90 días (LLM real para insights) o si se reposiciona el marketing hacia lo que el producto es hoy (agregación + scoring transparente), que también es un producto vendible, solo que distinto.

## Qué haría antes de gastar dinero en publicidad

- Arreglar el fallo de autorización del billing portal (no es opcional, es un riesgo de clientes reales).
- Confirmar con al menos un puñado de personas ajenas al fundador que el producto, tal como está hoy (no como se describe en la landing), genera un "wow, esto me ahorra tiempo de verdad" — no asumirlo.
- Verificar que el cron de ingestión diaria funciona de forma fiable varios días seguidos sin supervisión (recién creado, sin historial probado todavía) — no se quiere traer tráfico de pago a un dashboard con datos parados.

## Qué haría antes de buscar los primeros 100 clientes

- Cerrar el hueco entre "briefs de oportunidad" prometidos y plantilla fija actual, aunque sea de forma parcial (top 10-20 tendencias con insight real generado, el resto heurístico).
- Tener un canal de soporte real y visible (hoy solo hay un email personal de contacto en el footer legal, no un flujo de soporte dedicado).
- Confirmar retención real de los primeros clientes más allá del primer mes antes de escalar el gasto de adquisición — 100 clientes que cancelan al segundo mes no es el objetivo real, aunque cumpla la métrica literal pedida.

---

# 19. Archivos importantes

## Backend

- `backend/app/main.py` — punto de entrada de FastAPI: registra routers, CORS, middleware de rate limiting, Sentry, healthcheck.
- `backend/app/core/config.py` — toda la configuración de la aplicación (Pydantic Settings), única fuente de verdad de qué variables de entorno existen.
- `backend/app/core/security.py` — hashing de códigos de login, emisión/verificación de JWT de sesión.
- `backend/app/core/rate_limit.py` — limitador de tasa en memoria (sliding window).
- `backend/app/models/base.py` — todos los modelos SQLAlchemy (11 tablas, ver sección 9).
- `backend/app/models/database.py` — engine y sesión de SQLAlchemy.
- `backend/app/schemas/schemas.py` — todos los esquemas Pydantic de request/response.
- `backend/app/services/detector_service.py` — el motor de detección de tendencias completo (ver sección 7). El archivo más importante para entender el producto.
- `backend/app/services/trend_service.py` — lógica de consulta/listado de tendencias para la API.
- `backend/app/services/github_collector.py` / `hackernews_collector.py` / `rss_collector.py` — los tres collectors de fuentes públicas.
- `backend/app/services/email_service.py` — envío del código de login vía Resend.
- `backend/app/services/meta_capi.py` — envío de eventos de conversión server-side a Meta.
- `backend/app/services/seed.py` — datos de ejemplo para desarrollo local.
- `backend/app/api/v1/trends.py` / `ingestion.py` / `beta.py` / `billing.py` / `auth.py` — los 5 routers de la API.
- `backend/scripts/run_scheduled_ingestion.py` — entrypoint standalone que ejecuta el cron diario de Railway.
- `backend/migrations/versions/*.py` — las 4 migraciones Alembic aplicadas.
- `backend/tests/*.py` — suite de tests (~1.200 líneas), incluyendo `conftest.py` con el fixture de aislamiento de base de datos entre tests.

## Frontend

- `frontend/src/app/layout.tsx` — layout raíz, metadata global, scripts de Plausible y Meta Pixel.
- `frontend/src/app/page.tsx` — landing pública completa.
- `frontend/src/app/dashboard/page.tsx` — la única pantalla de producto real (ver sección 6).
- `frontend/src/app/pricing/page.tsx` / `login/page.tsx` — páginas de conversión y autenticación.
- `frontend/src/app/api/backend/[...path]/route.ts` — el proxy inverso que oculta el backend real y gestiona las claves compartidas.
- `frontend/src/lib/api.ts` — funciones tipadas de acceso a la API desde componentes de servidor.
- `frontend/src/components/PricingCheckout.tsx` / `LoginForm.tsx` / `BillingPortalButton.tsx` / `LandingInteractions.tsx` — los únicos componentes cliente del proyecto.
- `frontend/tests/e2e/smoke.spec.ts` — smoke test de Playwright (actualmente desactualizado, ver sección 17).

## Infraestructura y configuración

- `Dockerfile.backend` / `Dockerfile.frontend` (en la raíz del repo) — los Dockerfiles que Railway realmente construye. **Ojo**: existe un `frontend/Dockerfile` adicional que NO se usa en producción, solo el de la raíz — fuente de confusión ya materializada una vez.
- `docker-compose.yml` — solo para desarrollo local, no se usa en producción.
- `backend/railway.toml` / `frontend/railway.toml` — config-as-code de Railway (builder, healthcheck, política de reinicio).
- `.github/workflows/smoke.yml` — pipeline de CI (tests + build + smoke E2E contra producción en cada push a main).
- `.env.example` — plantilla de todas las variables de entorno documentadas (ver sección 11).

## Documentación interna ya existente en el repo

- `docs/MVP_STATUS.md`, `docs/MVP_CHECKLIST.md` — estado y checklist de lanzamiento (parcialmente desactualizados respecto a hoy, ver sección 2).
- `docs/AUDIT.md` — auditoría de seguridad y calidad previa (fechada 6 de junio de 2026), varios hallazgos siguen pendientes.
- `docs/EXECUTION_PLAN.md`, `docs/NEXT_STEPS.md`, `docs/TESTING.md`, `docs/RAILWAY_DEPLOYMENT.md` — planificación y guías operativas.
- `docs/HANDOFF_CTO.md` — **este mismo documento**.

---

# 20. Resumen final

AI Trend Hunter es un MVP de SaaS real, desplegado, cobrando en modo live, con una tesis de producto defendible: **la señal de una oportunidad de producto aparece primero en código y discusión técnica, no en cobertura mediática, y hoy nadie agrega esas tres fuentes concretas (GitHub, Hacker News, RSS) con scoring transparente y evidencia trazable en un solo sitio.**

Técnicamente, el sistema es deliberadamente simple: un backend FastAPI con una capa de servicios razonablemente limpia, un frontend Next.js que actúa de proxy inteligente hacia ese backend, autenticación passwordless propia sin dependencias externas de identidad, y un motor de detección **heurístico, no de IA generativa**, que convierte señales públicas en tendencias puntuadas mediante fórmulas deterministas y explicables. No hay orquestación multiagente, no hay LLM, no hay coste variable de inteligencia artificial — lo cual es tanto una fortaleza de margen como una brecha real entre lo que promete el naming/marketing ("AI-powered", "briefs accionables") y lo que el código entrega hoy (plantillas de texto fijas para el insight y las oportunidades).

El fundador ha demostrado, en el trabajo reciente sobre este repositorio, una disciplina operativa fuera de lo común para un proyecto en solitario: verificación end-to-end de pagos reales con su propia tarjeta, caza y corrección inmediata de bugs de producción con impacto económico real (suscripciones duplicadas, abuso de trial gratuito, falta de rate limiting en login), limpieza de elementos de desarrollo visibles a clientes de pago, y arreglo de un bug de integridad de datos (mezcla de tendencias no relacionadas) con purga y reingesta limpia. Esto es exactamente el tipo de rigor que separa un side-project de un negocio real.

Al mismo tiempo, esta auditoría ha encontrado **un fallo de autorización explotable en producción** (el endpoint de portal de facturación no verifica propiedad del email) que debería arreglarse antes de cualquier escalado de adquisición, y ha confirmado que **el CI del proyecto probablemente está roto ahora mismo** por un cambio de UI reciente sin actualizar su test correspondiente. Ninguno de los dos es difícil de arreglar, pero ambos son reales y activos hoy, no hipotéticos.

Para el nuevo CTO que herede este proyecto: el código es legible, está razonablemente bien organizado para su tamaño, y tiene tests reales (no decorativos). La deuda técnica principal no es de calidad de código, sino de **alcance no resuelto**: cinco tablas de base de datos completamente construidas y sin usar (`users`, `alerts`, `saved_trends`, `reports`, `trend_embeddings`), a la espera de una decisión de producto sobre si construir sobre ellas o retirarlas. El negocio, por su parte, tiene toda la infraestructura de monetización y tracking lista y verificada, pero **todavía no tiene un solo cliente de pago externo confirmado** — el próximo hito real no es técnico, es conseguir que alguien que no sea el propio fundador pague, se quede, y siga pagando el mes siguiente.
