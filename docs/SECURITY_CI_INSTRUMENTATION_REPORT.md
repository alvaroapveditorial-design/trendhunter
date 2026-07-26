# Informe: Auditoría e Implementación de Seguridad, CI e Instrumentación — AI Trend Hunter

**Fecha:** 26 de julio de 2026
**Destinatario:** ChatGPT, como continuación del documento de traspaso técnico (`docs/HANDOFF_CTO.md`, ver ahí el contexto completo del producto: qué es, arquitectura, motor de detección, modelo de negocio).
**Alcance de este informe:** una intervención directa sobre el código — no solo auditoría — para preparar el proyecto para empezar a adquirir clientes reales. Prioridades, en este orden: seguridad, CI/CD, instrumentación. Sin funcionalidades nuevas, sin cambios de UX salvo imprescindibles, sin refactors innecesarios.

Todo lo descrito aquí está **implementado, testeado localmente, commiteado y desplegado en producción real** (`aitrendhunter.app` y el backend en Railway), y verificado en vivo con `curl` y con un navegador real tras el despliegue — no es un plan, es lo que ya está corriendo.

---

## 1. Seguridad

### 1.1 Problemas encontrados

**P1 — Crítico — IDOR en el portal de facturación de Stripe.**
`POST /api/v1/billing/portal` recibía `{email}` en el body, buscaba la suscripción de ese email y devolvía una URL real y funcional del Stripe Customer Portal para esa suscripción — sin comprobar en ningún momento que quien hacía la petición fuera el dueño de ese email. Cualquiera que conociera o adivinara el email de un cliente de pago podía obtener un enlace para ver sus facturas, cambiar su tarjeta o cancelar su suscripción, sin acceso a su bandeja de entrada. El botón de la UI (`BillingPortalButton.tsx`) siempre mandaba el email correcto de la sesión activa, así que el problema no era visible usando la app normalmente — pero el endpoint del backend en sí no imponía ese vínculo y era alcanzable directamente vía HTTP.

**P2 — Crítico — `POST /api/v1/trends` sin ninguna protección.**
A diferencia de todos los endpoints de escritura bajo `/ingestion/*` (protegidos por una clave compartida `X-Ingestion-Key`), la creación manual de tendencias no tenía ninguna verificación. Cualquiera podía insertar tendencias falsas directamente en la base de datos de producción.

**P3 — Crítico — `GET /api/v1/trends*` completamente público.**
El paywall del producto vive únicamente en el Server Component del dashboard de Next.js (que redirige a `/pricing` si no hay sesión con suscripción activa). La API REST subyacente que sirve esos datos no tenía ninguna protección: cualquiera con la URL del backend (visible en la consola del navegador al usar el dashboard, o simplemente adivinable por convención de Railway) podía leer el catálogo completo de tendencias con una petición HTTP directa, sin pagar y sin autenticarse.

**P4 — Importante — Sin headers de seguridad.**
Ni el backend (FastAPI) ni el frontend (Next.js) enviaban ningún header de hardening: sin CSP, sin HSTS, sin `X-Frame-Options`, sin `X-Content-Type-Options: nosniff`, sin `Referrer-Policy`, sin `Permissions-Policy`.

**P5 — Importante — Checkout y portal de facturación sin rate limiting.**
De todos los endpoints mutables, solo `/ingestion/*` (100 req/hora) y `/auth/request-code` (5 req/15 min, arreglado en una sesión anterior) tenían límite de tasa. `/billing/checkout` y `/billing/portal` no tenían ninguno, dejando la puerta abierta a enumeración de emails (probar muchos emails contra `/checkout` para ver cuáles devuelven 409 "ya tienes suscripción activa") o abuso general.

**P6 — Importante — Dependencias con CVEs activos y en uso real en producción.**
Auditoría con `pip-audit` sobre `backend/requirements.txt`: 54 vulnerabilidades conocidas en 12 paquetes. Las relevantes para producción (no herramientas de desarrollo): `python-jose` (firma y verifica la cookie de sesión JWT — superficie de ataque real), `cryptography` (dependencia de jose), `python-multipart` (parsea todo input multipart), `requests`, `sentry-sdk`, `fastapi` (parche disponible). Además, `PyJWT==2.8.0` estaba instalada con CVEs activos **sin usarse en ningún sitio del código** (confirmado por grep: solo `python-jose` se importa realmente en `app/core/security.py`) — dependencia muerta con vulnerabilidades pagando su coste de superficie de ataque sin ningún beneficio.

**P7 — Importante — 3 vulnerabilidades de severidad alta en la cadena de dependencias de Next.js.**
`npm audit` reportó 3 altas en `postcss` (XSS en la salida de CSS, path traversal vía `sourceMappingURL`) y `sharp` (CVEs heredados de `libvips`), ambas dependencias transitivas de `next@16.2.7`.

**P8 — Bajo — sin forma de cerrar sesión desde la UI.**
El endpoint `POST /auth/logout` existía y funcionaba, pero el dashboard nunca renderizaba ningún botón que lo llamara. Se decidió que esto era lo bastante básico (control de sesión) como para arreglarlo pese a la instrucción de "no cambiar UX salvo imprescindible" — no había ninguna otra forma de que un usuario cerrara sesión explícitamente.

### 1.2 Solución aplicada

**Fix de P1 (IDOR del billing portal).** Nueva dependencia compartida `require_session_email()` en `backend/app/api/deps.py`, que decodifica la cookie de sesión firmada (`trendhunter_session`) y devuelve el email que contiene. `POST /billing/portal` ahora usa exclusivamente ese email — ya no acepta ni lee ningún email del body de la petición. Se añadió `test_billing_portal_requires_authentication` (confirma 401 sin cookie) y `test_billing_portal_ignores_body_email_uses_session_only` (crea una suscripción para un email "víctima", autentica con la sesión de un email "atacante" distinto, envía el email de la víctima en el body, y confirma que la respuesta es 404 — la petición se resuelve contra la sesión del atacante, nunca contra el body). El schema `BillingPortalCreate`, que ya no se usa, se eliminó.

**Fix de P2 (creación de tendencias sin protección).** `POST /trends` ahora exige la misma dependencia `require_ingestion_key` que ya protegía `/ingestion/*` — reutilizando el patrón y el secreto ya existentes (`INGESTION_API_KEY`) en vez de inventar uno nuevo. Test añadido: `test_create_trend_requires_ingestion_key_when_configured`.

**Fix de P3 (API de tendencias pública).** Nueva variable de entorno `BACKEND_INTERNAL_KEY` y dependencia `require_internal_key()`, aplicada a nivel de router a todos los endpoints de `/api/v1/trends*` (lecturas incluidas). Sigue el mismo patrón de "fail-open si la clave no está configurada" que ya usaba `require_ingestion_key` — es decir, el código se puede desplegar sin riesgo de romper nada mientras la variable esté vacía, y solo empieza a exigirse cuando se configura explícitamente en ambos servicios. El frontend (`frontend/src/lib/api.ts`, que hace las llamadas server-side a la API de tendencias desde el Server Component del dashboard) ahora manda `X-Internal-Key` en cada petición si `BACKEND_INTERNAL_KEY` está definida en su propio entorno. Test añadido: `test_trend_reads_require_internal_key_when_configured`. **Esta clave ya está generada, configurada en ambos servicios de Railway (`trendhunter-backend` y `trendhunter-frontend`) y verificada activa en producción** — ver sección de verificación más abajo.

**Fix de P4 (headers de seguridad).** Middleware nuevo en `backend/app/main.py` (`security_headers_middleware`) que añade a toda respuesta: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, y `Strict-Transport-Security` (solo si `ENVIRONMENT=production`). En el frontend, `next.config.ts` añade los mismos headers vía `async headers()`, más una **Content-Security-Policy real** construida específicamente para lo que esta app necesita:

```
default-src 'self';
script-src 'self' 'unsafe-inline' https://plausible.io https://connect.facebook.net;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com;
img-src 'self' data: https://www.facebook.com;
connect-src 'self' https://plausible.io https://graph.facebook.com https://connect.facebook.net https://www.facebook.com;
frame-ancestors 'none';
base-uri 'self';
form-action 'self';
```

**Fix de P5 (rate limiting en billing).** `/billing/checkout` y `/billing/portal` se añadieron explícitamente (por path exacto, no por prefijo) al limitador general existente (100 req/hora por IP). Deliberadamente **no** se aplicó por prefijo `/billing/*`, porque eso habría incluido `/billing/webhook` — el endpoint que recibe los eventos reales de Stripe. Someter el webhook a un límite de 100/hora habría arriesgado descartar entregas legítimas de Stripe si alguna vez reintenta un lote grande de eventos (por ejemplo tras una caída), lo cual habría sido un riesgo real de romper el sincronismo de estado de facturación en producción. El webhook queda explícitamente excluido.

**Fix de P6 (dependencias backend).** En `backend/requirements.txt`: `fastapi` 0.109.0→0.109.1, `python-dotenv` 1.0.0→1.2.2, `requests` 2.31.0→2.33.0, `python-jose[cryptography]` 3.3.0→3.4.0, `cryptography` 41.0.7→43.0.1, `python-multipart` 0.0.6→0.0.18, `sentry-sdk` 1.39.1→1.45.1. Se **eliminaron** `PyJWT` y `passlib[bcrypt]` (y sus funciones muertas `hash_password`/`verify_password` en `app/core/security.py`, confirmadas sin ningún caller). Instalación limpia en un venv nuevo (Python 3.11) y suite completa de tests corrida contra las versiones nuevas: 58/58 en verde.

**Fix de P7 (dependencias frontend).** `next` 16.2.7→16.2.12 (parche). Como ese bump por sí solo no arrastraba versiones parcheadas de `postcss`/`sharp` (Next.js fija internamente versiones transitivas independientes de su propio parche), se añadió un bloque `overrides` en `package.json` forzando `postcss@^8.5.18` y `sharp@^0.35.0`. Se confirmó que `next/image` no se usa en ningún componente del proyecto (grep sin resultados), así que forzar `sharp` — que Next.js solo usa para optimización de imágenes vía `next/image` — no tiene ningún riesgo funcional. Resultado: `npm audit` pasó de 3 vulnerabilidades altas a **0**.

**Fix de P8 (logout).** Nuevo componente `LogoutButton.tsx`, añadido junto al botón de "Manage billing" en la cabecera del dashboard. Llama a `POST /auth/logout` (que ya borraba la cookie correctamente) y redirige a `/login`.

### 1.3 Riesgo residual (lo que queda pendiente y por qué)

- **CSP con `'unsafe-inline'`** en `script-src` y `style-src`. El Pixel de Meta se inyecta como un `<script>` inline (`layout.tsx`) y la landing usa atributos `style="--val:88%"` inline de forma extensiva en decenas de elementos. Una CSP estricta sin `'unsafe-inline'` requeriría o bien un sistema de nonces por request (necesita middleware nuevo en Next.js, cambia cómo se declaran los `<Script>`) o convertir todos los estilos inline de la landing a clases CSS — ambas son refactors reales, explícitamente fuera de alcance ("no hagas refactors innecesarios"). Se documenta como riesgo aceptado, no oculto: el resto de directivas (`object-src` implícito en `default-src 'self'`, `base-uri 'self'`, `frame-ancestors 'none'`, `connect-src` restringido a orígenes concretos) sigue aportando protección real incluso con `unsafe-inline` en esas dos directivas.
- **`fastapi`/`starlette` no subieron de versión menor.** El fix real de las CVEs de `starlette` (una dependencia interna de FastAPI que procesa cada request) requiere `starlette>=0.37`, lo cual solo es compatible con `fastapi>=0.110`. Eso es un salto de minor version con más superficie de regresión de la que un cambio de este alcance debía asumir sin una ventana de testing dedicada — se hizo el bump de patch seguro (`0.109.0→0.109.1`) y se deja documentado el resto.
- **`x-forwarded-for` en el rate limiter sigue sin validarse contra una lista de proxies de confianza.** Un atacante podría en teoría falsificar esa cabecera para evadir el límite. Impacto bajo dado que Railway es el único borde de red delante del backend, pero no es una validación defensiva real.
- **Sin revocación de sesión.** La cookie de sesión JWT dura 60 minutos y no hay forma de invalidarla antes de su expiración natural (no hay lista de revocación, no hay estado de sesión en base de datos). Mitigado por el TTL corto, no resuelto — implementarlo bien requeriría Redis o una tabla de sesiones activas, que es un cambio de infraestructura más grande de lo que este trabajo cubría.
- **No se pudo verificar el flujo autenticado completo del dashboard con un login real** (requiere acceso a la bandeja de entrada del fundador para leer el código de un solo uso). Se verificó indirectamente: el build/typecheck pasan, el header `X-Internal-Key` se confirma enviado en cada llamada server-side por revisión de código, y `GET /trends` con la clave correcta responde 200 mientras que sin ella responde 401 (confirmado con `curl` en producción). Falta la confirmación visual de que el dashboard real, con una sesión real, sigue cargando datos correctamente.

---

## 2. CI/CD

### 2.1 Problemas encontrados

El único workflow de CI (`.github/workflows/smoke.yml`, disparado en cada push a `main`) corre tests de backend, lint y build de frontend, y finalmente un smoke test end-to-end con Playwright contra las URLs reales de producción de Railway. Ese smoke test (`frontend/tests/e2e/smoke.spec.ts`) hacía `page.goto("/")` y esperaba encontrar botones llamados "Run demo ingestion", "Pull Hacker News", "Pull RSS" y "Pull GitHub", y clicaba en cada uno esperando una respuesta 2xx del backend. Esos botones formaban parte de un panel de administración de ingestión que **ya no existe en el dashboard** — se eliminó en un commit anterior (`9d951ef`, misma línea de trabajo de esta sesión) precisamente porque estaba expuesto a cualquier cliente de pago logueado, no solo al operador del producto. El test, además, navegaba a `/` esperando encontrar el dashboard ahí — pero `/` es la landing pública desde que se añadió el flujo de auth/billing (el dashboard vive en `/dashboard` y exige sesión + suscripción activa). En resumen: el test llevaba tiempo verificando una versión del producto que ya no existía, con altísima probabilidad de que el pipeline de GitHub Actions estuviera en rojo en cada push reciente.

### 2.2 Solución aplicada

Reescrito por completo (`frontend/tests/e2e/smoke.spec.ts`) para reflejar la arquitectura real actual. Como el dashboard exige un login por código de email de un solo uso que **en producción nunca se devuelve al cliente** (solo se envía por email real vía Resend), no es posible automatizar un login real sin una bandeja de entrada de pruebas — así que el nuevo smoke test cubre lo que sí es verificable sin credenciales, y que además es justo lo más relevante tras el trabajo de seguridad de este informe:

1. La landing (`/`) renderiza con el formulario de beta signup visible.
2. `/pricing` renderiza con el formulario de checkout (email + botón "Start trial").
3. `/login` renderiza con el formulario de código de email.
4. `/dashboard`, visitado sin sesión, **redirige** a `/login` o `/pricing` en vez de mostrar cualquier dato — esta última prueba es la más valiosa: confirma en cada deploy, con un navegador real, que el paywall/gate de autenticación sigue activo, que es exactamente lo que se reforzó en la sección de seguridad de este informe.

Verificación: 58 tests de backend (`pytest`) + `tsc --noEmit` (lint) + `next build` + las 4 pruebas de Playwright, todo en verde localmente contra Node 20 (el proyecto usa Node 22 en Docker; localmente solo había Node 18 disponible vía default, así que se usó `nvm` para probar contra Node 20, la versión mínima real que exige `next@16.2.12`) y, tras el despliegue, las 4 pruebas de Playwright se re-ejecutaron **contra la producción real ya desplegada** y pasaron igual.

---

## 3. Instrumentación

### 3.1 Sistema existente antes de esta intervención

Solo pageview automático de Plausible (sin eventos custom) y Meta Pixel/Conversions API limitado a dos eventos de conversión publicitaria (`StartTrial`, `Purchase`) ya integrados en una sesión de trabajo anterior. No existía ningún sistema genérico de eventos de producto, ni captura de errores de frontend, ni captura real de fallos operativos de backend hacia Sentry (los `HTTPException` de 4xx que ya se lanzaban en fallos de Stripe/GitHub/HN/RSS no llegaban nunca a Sentry, porque Sentry no captura automáticamente excepciones HTTP "esperadas" — solo excepciones no controladas).

### 3.2 Arquitectura elegida

Dos piezas nuevas, ambas construidas sobre la infraestructura ya existente (Plausible, ya integrado y pagado/activo; Sentry, ya integrado) en vez de añadir un SDK de analítica nuevo:

- **`frontend/src/lib/analytics.ts`**: una función `track(event, props)` que envuelve `window.plausible(...)`, no-op si el script no ha cargado (ad blocker, dominio sin configurar, etc.), nunca lanza. Usada desde componentes cliente ya existentes y unos pocos nuevos, muy pequeños, de un solo propósito.
- **`backend/app/services/plausible_events.py`**: un `send_plausible_event()` que llama a la Events API HTTP de Plausible (`https://plausible.io/api/event`), con el mismo patrón defensivo que ya usaba `meta_capi.py` (nunca lanza, loguea en fallo, no-op si no está configurado). Se usa para los eventos que ocurren dentro del webhook de Stripe, donde no hay navegador — exactamente al lado de las llamadas ya existentes a la Conversions API de Meta.

### 3.3 Eventos añadidos

| Categoría pedida | Evento | Dónde se dispara | Notas |
|---|---|---|---|
| Landing | `Landing Viewed` | `LandingInteractions.tsx`, al montar | |
| Landing | `CTA Clicked` | `LandingInteractions.tsx`, listener delegado en `.btn` | Captura texto del botón y `href` |
| Landing | `Pricing Viewed` | `PageViewTracker` en `pricing/page.tsx` | |
| Registro | `Sign Up Started` | `PricingCheckout.tsx`, al enviar el formulario | En este producto, "registrarse" = empezar el checkout; no hay paso de creación de cuenta separado |
| Registro | `Login` | `LoginForm.tsx`, tras verificar el código con éxito | |
| Registro | `Logout` | `LogoutButton.tsx` (nuevo, ver sección 1.2) | |
| Trial | `Trial Started` | Backend, webhook `checkout.session.completed` con `subscription_status=trialing` | |
| Trial | `Trial Converted` | Backend, webhook `customer.subscription.updated`, transición trialing→active | Junto al `Purchase` de Meta CAPI ya existente |
| Trial | `Trial Expired` | Backend, transición trialing→{past_due, unpaid, canceled, incomplete_expired} | Cubre el caso de que el cobro al final del trial falle |
| Pago | `Checkout Started` | `PricingCheckout.tsx`, al enviar el formulario | |
| Pago | `Checkout Completed` | Backend, webhook `checkout.session.completed` con `subscription_status=active` | Caso de un email que ya usó su trial y paga directo sin periodo de prueba |
| Pago | `Checkout Failed` | `PricingCheckout.tsx`, catch de la llamada a `/billing/checkout` | Cubre fallos del lado cliente; Stripe no notifica por webhook los intentos de checkout abandonados con la configuración actual de eventos suscritos |
| Pago | `Billing Portal Opened` | `BillingPortalButton.tsx`, al pulsar | |
| Dashboard | `Dashboard Viewed` | `PageViewTracker` en `dashboard/page.tsx` | |
| Dashboard | `Trend Viewed` | `TrendDetailAnalytics.tsx`, al montar/cambiar la tendencia seleccionada | |
| Dashboard | `Opportunity Viewed` | Mismo componente, si la tendencia tiene oportunidades listadas | No hay una pantalla de "oportunidad" separada del detalle de tendencia en el producto actual — se dispara junto a `Trend Viewed` cuando aplica |
| Dashboard | `Search Used` | `DashboardFilterAnalytics.tsx`, al enviar el formulario de filtros con `q` no vacío | Se manda solo la longitud del texto buscado, no el texto en sí, por privacidad |
| Dashboard | `Filter Used` | Mismo componente, si hay categoría/fuente/score mínimo activos | |
| Engagement | sesión, duración, páginas, frecuencia, retención | — | Ya cubierto automáticamente por el pageview + tracking de "engaged time" nativo de Plausible en todas las páginas (el script está en el layout raíz, aplica a todo el sitio incluido el dashboard) — no requería código adicional |
| Errores | `Frontend Error` | `ErrorTracking.tsx` (montado en el layout raíz, `window.onerror` + `unhandledrejection`) y `error.tsx` (App Router error boundary) | |
| Errores | Backend / excepciones / fallos de API | Sentry (`sentry_sdk.capture_exception` / `capture_message`) añadido explícitamente en: rechazo de checkout/portal de Stripe (`billing.py`), fallos de fetch de GitHub/HN/RSS (`ingestion.py`), y el script del cron diario (`run_scheduled_ingestion.py`, que **antes de este cambio ni siquiera inicializaba Sentry**, al correr como proceso standalone fuera de `app.main`) | |

### 3.4 Cobertura conseguida y huecos honestos

**No se instrumentaron `Trend Saved` ni `Trend Shared`** de la lista pedida, a propósito: esas funcionalidades no existen en el producto (confirmado contra el modelo de datos y las rutas de la API en `docs/HANDOFF_CTO.md`, sección 8 — la tabla `saved_trends` existe en el esquema pero no tiene ningún endpoint ni UI). Instrumentar un evento para una acción que el usuario no puede realizar habría sido fabricar datos falsos en el dashboard de analítica. Si en algún momento se construyen esas funciones, el patrón para añadir el evento ya está establecido (`track("Trend Saved", {...})` en el punto donde se implemente el botón).

`Checkout Failed` solo cubre fallos detectados por el propio frontend (la llamada a `/billing/checkout` devuelve error). Stripe no envía webhook para checkouts iniciados y abandonados con la suscripción de eventos actual (4 eventos configurados: `checkout.session.completed` + 3 de `customer.subscription.*`); añadir `checkout.session.expired` a la configuración del webhook en el dashboard de Stripe permitiría capturar también los abandonos reales, pero es un cambio de configuración externa a Stripe, no de código, y queda fuera de lo que se tocó en esta intervención.

---

## 4. Calidad

**Limpieza realizada:**
- ~80 líneas de CSS muerto en `frontend/src/app/globals.css`: todas las reglas `.ingestion-panel*`, `.ingestion-actions*`, `.pipeline-meta*`, `.action-message*` y `.secondary-button` correspondientes al panel de administración de ingestión eliminado del JSX en un commit anterior (`9d951ef`) pero nunca limpiado del CSS. Confirmado por grep que ninguna clase se referenciaba ya en ningún componente antes de borrarlas.
- `PyJWT` (dependencia) y las funciones `hash_password`/`verify_password` en `app/core/security.py` (dead code de un diseño de auth con contraseña, anterior al sistema passwordless actual) — cero callers confirmados por grep.
- `passlib[bcrypt]` (dependencia, solo usada por las funciones anteriores).
- Schemas Pydantic `UserBase`, `UserCreate`, `UserLogin`, `UserResponse`, `TokenResponse` en `backend/app/schemas/schemas.py` — cero referencias en ningún endpoint (corresponden al mismo diseño de auth anterior; la tabla `users` del modelo de datos, que estos schemas reflejaban, sigue existiendo y sin usar, pero esa es una decisión de producto documentada en `docs/HANDOFF_CTO.md`, no se tocó).
- `BillingPortalCreate` schema, huérfano tras el fix de seguridad de la sección 1.
- Verificación explícita: cero `console.log`, cero `print()` de depuración, cero `TODO`/`FIXME` en todo el código de aplicación (`grep` recursivo sobre `backend/app`, `backend/scripts` y `frontend/src`, resultado vacío tanto al empezar como al terminar).
- `flake8 --select=F401,F841` (imports y variables sin usar) sobre `backend/app`: sin resultados tras todos los cambios.

No se tocó el esquema de base de datos (`users`, `alerts`, `saved_trends`, `reports`, `trend_embeddings` siguen sin usarse) ni el README (que sigue describiendo una arquitectura multiagente aspiracional que no refleja el código real) — ambos son decisiones de producto/documentación fuera del alcance de "seguridad, CI, instrumentación", ya señaladas como deuda técnica en `docs/HANDOFF_CTO.md`.

---

## 5. Archivos modificados

**Backend**
- `backend/app/api/deps.py` — **nuevo**. Dependencias compartidas: `require_session_email`, `require_ingestion_key` (movida aquí desde `ingestion.py`), `require_internal_key`.
- `backend/app/api/v1/billing.py` — fix del IDOR, rate limiting específico, eventos Plausible, captura Sentry en fallos de Stripe.
- `backend/app/api/v1/ingestion.py` — usa la dependencia compartida, captura Sentry en fallos de fetch.
- `backend/app/api/v1/trends.py` — protección de lecturas (`require_internal_key`) y de la creación manual (`require_ingestion_key`).
- `backend/app/core/config.py` — nueva variable `BACKEND_INTERNAL_KEY`.
- `backend/app/core/security.py` — eliminadas `hash_password`/`verify_password` (dead code).
- `backend/app/main.py` — nuevo middleware de headers de seguridad, rate limiting extendido a billing/trends.
- `backend/app/schemas/schemas.py` — eliminados schemas de usuario/token sin uso y `BillingPortalCreate`.
- `backend/app/services/plausible_events.py` — **nuevo**. Eventos server-side de Plausible.
- `backend/requirements.txt` — versiones parcheadas, `PyJWT`/`passlib` eliminados.
- `backend/scripts/run_scheduled_ingestion.py` — inicialización de Sentry + captura de excepciones (antes invisible para Sentry).
- `backend/tests/test_billing_api.py` — test del portal actualizado a auth por cookie + 2 tests nuevos de regresión del IDOR.
- `backend/tests/test_trends_api.py` — 2 tests nuevos (clave de ingestion en creación, clave interna en lecturas).

**Frontend**
- `frontend/next.config.ts` — headers de seguridad + CSP.
- `frontend/package.json` / `package-lock.json` — Next.js 16.2.12, overrides de postcss/sharp.
- `frontend/src/app/layout.tsx` — monta `ErrorTracking`.
- `frontend/src/app/error.tsx` — reporta al error boundary global.
- `frontend/src/app/dashboard/page.tsx` — monta trackers, añade `LogoutButton`, quita el prop `email` de `BillingPortalButton`.
- `frontend/src/app/pricing/page.tsx` — monta `PageViewTracker`.
- `frontend/src/app/globals.css` — limpieza de CSS muerto, estilo del botón de logout.
- `frontend/src/components/BillingPortalButton.tsx` — ya no manda email en el body.
- `frontend/src/components/LandingInteractions.tsx` — eventos Landing Viewed / CTA Clicked / Beta Signup Completed.
- `frontend/src/components/LoginForm.tsx` — evento Login.
- `frontend/src/components/PricingCheckout.tsx` — eventos Sign Up/Checkout Started, Checkout Failed.
- `frontend/src/components/LogoutButton.tsx` — **nuevo**.
- `frontend/src/components/PageViewTracker.tsx` — **nuevo**.
- `frontend/src/components/ErrorTracking.tsx` — **nuevo**.
- `frontend/src/components/DashboardFilterAnalytics.tsx` — **nuevo**.
- `frontend/src/components/TrendDetailAnalytics.tsx` — **nuevo**.
- `frontend/src/lib/analytics.ts` — **nuevo**.
- `frontend/src/lib/api.ts` — envía `X-Internal-Key` en las llamadas server-side a la API de tendencias.
- `frontend/tests/e2e/smoke.spec.ts` — reescrito por completo.

**Raíz**
- `.env.example` — `BACKEND_INTERNAL_KEY` documentada, `SESSION_TIMEOUT_MINUTES` corregido de 1440 (valor obsoleto, contradecía el hardening ya aplicado en una sesión anterior) a 60.
- `docs/HANDOFF_CTO.md` — documento de traspaso completo (entregado previamente).
- `docs/SECURITY_CI_INSTRUMENTATION_REPORT.md` — este informe.

## 6. Despliegue y verificación en producción

Dos commits (`de07f19` seguridad/CI/dependencias, `1008d0b` instrumentación/limpieza) empujados a `main`, desplegados automáticamente por la integración de Railway con GitHub. Tras el despliegue:

- `curl` contra el backend de producción: `/health` → 200; `POST /trends` sin clave → 401; `POST /billing/portal` sin sesión → 401; headers de seguridad presentes en la respuesta.
- Variable `BACKEND_INTERNAL_KEY` generada y configurada en `trendhunter-backend` y `trendhunter-frontend` en Railway (mismo valor en ambos), ambos servicios redesplegados automáticamente al fijar la variable.
- Tras ese segundo despliegue: `GET /trends` sin `X-Internal-Key` → 401; con la clave correcta → 200. La API de tendencias ya no es de lectura pública.
- Navegador real contra `aitrendhunter.app`: cero errores de consola, `window.plausible` y `window.fbq` cargan correctamente bajo la nueva CSP (sin violaciones).
- Suite de Playwright (4 tests) re-ejecutada contra la producción ya desplegada: 4/4 en verde, incluida la comprobación de que `/dashboard` sigue redirigiendo correctamente a un visitante sin sesión.

## 7. Pendientes

Los mismos de la sección "Riesgo residual" (1.3) más:
- Confirmación visual de un login real y completo contra el dashboard en producción (necesita acceso a la bandeja de entrada del fundador para el código de un solo uso — no ejecutable de forma automática).
- Añadir `checkout.session.expired` a la suscripción de eventos del webhook de Stripe (en el dashboard de Stripe, no en código) para capturar `Checkout Failed` también en el servidor, no solo cuando el frontend detecta el fallo.
- Migración de CSP a nonces y subida de minor version de fastapi/starlette, ambas explícitamente diferidas por requerir más superficie de cambio de la que este trabajo debía asumir sin ventana de testing dedicada.
