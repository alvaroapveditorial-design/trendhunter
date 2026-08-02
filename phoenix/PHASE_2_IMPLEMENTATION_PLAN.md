# Phoenix Fase 2 — Plan de implementación

**Antes de tocar código.** Ver `PHASE_2_BASELINE.md` para la línea base y `ANALYTICS_EVENT_MAP.md` para el detalle de instrumentación.

## Hallazgos de la auditoría previa

- **Eventos de conversión existentes:** `Landing Viewed`, `CTA Clicked`, `Beta Signup Completed` (home); `Pricing Viewed`, `Sign Up Started`, `Checkout Started`, `Checkout Failed` (pricing/checkout); `Login` (login); `Dashboard Viewed`, `Trend Viewed`, `Opportunity Viewed`, `Search Used`, `Filter Used` (dashboard); `Trial Started`, `Trial Converted`, `Trial Expired` (backend, webhook de Stripe). Faltan exactamente los que lista el brief como nuevos: `How It Works Click`, `Real Example Viewed`, `Pricing CTA Clicked`, `Checkout Created`, `Stripe Checkout Completed`, `Login Code Requested`, `First Trend Opened`. Detalle de mapeo en `ANALYTICS_EVENT_MAP.md`.
- **Datos/cifras ficticias confirmadas en código:** mockup del hero (`1,284 signals processed`, `142 Tracked trends +18`, `23 New this week +6`, `Avg. momentum +34%`, tabla de 4 filas con nombres y sparklines inventados) y las 3 tarjetas de "Sample output" (scores, momentum y briefs inventados) en `frontend/src/app/page.tsx`.
- **Enlaces falsos confirmados:** footer → "About" apunta a `#top`; "GitHub", "Hacker News", "RSS feeds" (columna Sources) apuntan a `#top`. Todos en `frontend/src/app/page.tsx`.
- **"Coming soon" en posición principal de venta:** 2 de 4 casos de uso ("Monitor emerging niches" → alertas, "Prep weekly opportunity reports" → PDF export).
- **Fuentes infladas:** franja de logos lista 6 elementos (GitHub, Hacker News, RSS feeds, Product changelogs, Release notes, Dev forums) cuando el producto integra 3 (GitHub, HN, RSS — el resto son subconjuntos de RSS).
- **Copy poco natural confirmado:** `"No open free plan: a short trial to validate real value."` en `frontend/src/app/pricing/page.tsx`.
- **Mecanismo actual para datos reales del dashboard:** el router completo de `/api/v1/trends` (incluido `/spotlight`) exige `require_internal_key` (server-to-server, no expuesto al navegador). **No crearé un endpoint público nuevo** — ver decisión de "ejemplo real" más abajo.
- **Bug de scroll (ítem 12 del brief) — investigado, NO reproducido:** `globals.css` línea 1259 tiene una única regla, `.landing-page .reveal { opacity: 1; transform: none; }`, con el comentario explícito *"content is always visible; motion is intentionally avoided so nothing can freeze hidden in throttled/offscreen rendering contexts"*. No existe ningún IntersectionObserver ni lógica JS que oculte `.reveal` (verificado por grep en todo `frontend/src`). Verificado en vivo con `getComputedStyle` sobre 6 elementos `.reveal` reales en producción: `opacity: 1`, `transform: none`, `display: block` en todos. La causa real de los "vacíos" observados en la auditoría de ayer es el padding vertical genuino de `.section` (`120px` arriba y abajo, confirmado por `getComputedStyle`), no un fallo de animación. **No se toca ninguna animación.** Se documenta como investigado y descartado, tal como exige el brief.
- **Resend / dominio de email:** confirmado en Railway (`trendhunter-backend`, vía `railway variable list`) que `SENDER_EMAIL=onboarding@resend.dev` en producción — el dominio de pruebas de Resend, no uno propio. `RESEND_API_KEY` y `SUPPORT_EMAIL` (`alvaroapveditorial@hotmail.com`) ya están configurados. El código ya lee `SENDER_EMAIL` exclusivamente por variable de entorno (`backend/app/core/config.py`), así que no hace falta ningún cambio de código para apuntar a un dominio propio una vez esté verificado — solo cambiar el valor de la variable. Cambio de código aplicado en esta fase: `send_login_code_email` (en `backend/app/services/email_service.py`) ahora añade `reply_to: [SUPPORT_EMAIL]` cuando está configurado, igual que ya hacía `send_support_contact_email` — antes el email de código de acceso no tenía Reply-To. Cubierto por `backend/tests/test_email_service.py` (nuevo).

  **Qué falta y cómo resolverlo (acción externa, no soy yo quien puede completarla):**
  1. En el dashboard de Resend, verificar el dominio `aitrendhunter.app` (o el subdominio que se prefiera, p.ej. `mail.aitrendhunter.app`) en la sección **Domains**.
  2. Añadir los registros DNS que Resend indique (típicamente SPF y DKIM, tipo TXT/CNAME) en el proveedor DNS del dominio. Esperar a que Resend marque el dominio como **Verified** (puede tardar minutos u horas según el TTL).
  3. Elegir una dirección remitente sobre ese dominio, p.ej. `noreply@aitrendhunter.app`.
  4. En Railway, servicio **trendhunter-backend**, actualizar la variable `SENDER_EMAIL` a esa dirección (`railway variable set SENDER_EMAIL=noreply@aitrendhunter.app --service trendhunter-backend`). Redeploy automático al guardar.
  5. **Verificación:** solicitar un código de acceso real desde `/login` con un email propio y confirmar que (a) el correo llega, (b) el remitente mostrado es `noreply@aitrendhunter.app` y no `onboarding@resend.dev`, (c) responder al correo llega a `alvaroapveditorial@hotmail.com` (Reply-To).

  No invento ningún valor de dominio ni cambio la variable yo mismo: verificar un dominio en Resend requiere acceso a su panel y al DNS del dominio, que no controlo desde este entorno. Esto no bloquea el resto de la fase — el checklist de reactivación de Meta (sección 21) lo recoge como riesgo documentado explícito si sigue sin resolverse antes de reactivar.

## Archivos que modificaré

**Frontend**
- `frontend/src/app/pricing/page.tsx` — reescritura de contenido (hero, mecanismo, ejemplo real, qué recibes, FAQ, nav, CTA).
- `frontend/src/components/PricingCheckout.tsx` — nuevos eventos (`Pricing CTA Clicked`, `Checkout Created`), sin tocar la lógica del checkout.
- `frontend/src/app/page.tsx` — cifras del mockup, ejemplos de "Sample output", franja de fuentes, casos de uso, footer (enlaces muertos).
- `frontend/src/components/LandingInteractions.tsx` — sin cambios de lógica; revisar si el copy de errores necesita ajuste (no se prevé).
- `frontend/src/components/TrendDetailAnalytics.tsx` — añadir `First Trend Opened` (guardado por `sessionStorage`, una vez por sesión de navegador).
- `frontend/src/components/LoginForm.tsx` — renombrar evento `Login` → `Login Completed`.
- **Nuevos:** `frontend/src/components/pricing/RealExampleCard.tsx`, `frontend/src/components/pricing/ProductScreenshot.tsx`, `frontend/src/components/pricing/PricingFaq.tsx`, `frontend/src/components/pricing/PricingNav.tsx` — componentes pequeños, de un solo propósito, sin librerías nuevas.
- `frontend/src/app/globals.css` — nuevas reglas de estilo para las secciones anteriores, reutilizando variables y patrones ya existentes (`.scard`, `.pricing-card`, `.section-head`). Sin animaciones nuevas.
- `frontend/tests/e2e/smoke.spec.ts` — nuevos casos E2E (ver sección de tests).

**Backend**
- `backend/app/api/v1/auth.py` — disparo de `Login Code Requested` (server-side).
- `backend/app/api/v1/billing.py` — disparo de `Stripe Checkout Completed` junto a `Trial Started` (mismo bloque idempotente ya existente).
- `backend/tests/test_auth_api.py` / `backend/tests/test_billing_api.py` — tests de los nuevos disparos (monkeypatch, mismo patrón que los existentes).

**Documentación**
- `phoenix/PHASE_2_IMPLEMENTATION_PLAN.md` (este archivo), `phoenix/PHASE_2_BASELINE.md`, `phoenix/ANALYTICS_EVENT_MAP.md`, `phoenix/PHASE_2_RELEASE_REPORT.md`.

## Archivos que NO tocaré

`backend/app/services/detector_service.py`, cualquier `*_collector.py`, `backend/app/models/`, `backend/app/api/deps.py` (auth), `backend/app/api/v1/billing.py` más allá del disparo de evento señalado (ni precio, ni `trial_period_days`, ni lógica de checkout/portal), `frontend/src/app/dashboard/**`, `frontend/src/app/login/**` (salvo el rename de evento ya indicado), infraestructura, cron, migraciones.

## Decisión: ejemplo real de oportunidad (sección 5.3 del brief)

Evaluadas las tres opciones en el orden que pide el brief:
1. **Endpoint público** — descartado. El router de `/api/v1/trends` está protegido con `require_internal_key` (server-to-server). Exponer un endpoint público nuevo, aunque fuera de solo lectura, añade superficie de ataque nueva (rate limiting, allowlist de campos, etc.) fuera del alcance autorizado ("no sobreingenierices", "no expongas endpoints internos").
2. **Snapshot en build/deploy** — descartado por ahora. Añadiría un paso de build nuevo para una sola tarjeta de ejemplo; complejidad desproporcionada al problema.
3. **Ejemplo real estático, fechado y documentado — elegido.** Tendencia real extraída directamente de la base de datos de producción hoy (2 de agosto de 2026): **"Llmgateway"**, detectada el 31 de julio de 2026 vía GitHub (`theopenco/llmgateway`, 1.486 estrellas, 54 issues abiertos), trend score 83, opportunity 88, saturation 29, momentum 33,2. Se muestra con su fecha real de detección y una nota explícita de que es un ejemplo real capturado en una fecha concreta, no un dato en vivo. **Mantenimiento documentado:** para refrescar el ejemplo, consultar `SELECT ... FROM trends WHERE is_active=true ORDER BY trend_score DESC LIMIT 5` vía `railway connect Postgres`, elegir una tendencia con score alto y descripción comprensible para un lector no técnico, y actualizar la constante en `RealExampleCard.tsx` junto con su fecha.

## Decisión: captura del dashboard (sección 5.2)

**Actualización (2 de agosto de 2026, tras petición explícita del usuario):** el placeholder inicial se sustituyó por una captura real. Generada con Playwright contra `https://aitrendhunter.app/dashboard` autenticado con una cuenta de prueba (`test-checkout@example.com`, con un `trialing` real en `subscriptions`, sin datos personales asociados a una persona real), usando un token de sesión firmado con la `SECRET_KEY` real de producción (generado vía `backend/scripts/print_session_token.py`, ejecutado con `railway run --service trendhunter-backend` para heredar las variables de entorno reales). Antes de capturar se ocultó `.topbar` (que muestra el email de la cuenta y el botón "Manage billing") mediante una regla CSS inyectada, para no exponer ningún dato de cuenta/facturación. Dos capturas guardadas en `frontend/public/pricing/`: `dashboard-preview.png` (1440×900, 174 KB) y `dashboard-preview-mobile.png` (390×844, 51 KB), ambas por debajo del presupuesto de ~300 KB documentado originalmente. `ProductScreenshot.tsx` ahora renderiza estas imágenes con `<picture>`/`srcSet` para servir la versión móvil por debajo de 640px, y una leyenda "Dashboard snapshot captured on 2 August 2026". El proceso de refresco queda documentado en el propio componente.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| El ejemplo real ("Llmgateway") deja de ser representativo con el tiempo | Documentado el proceso de refresco; es una tendencia real con fecha visible, no se presenta como "hoy" |
| Nuevos eventos de Plausible duplican con los existentes | Renombrado explícito (`Login` → `Login Completed`, `Pricing Viewed` → `Pricing View`) en vez de añadir uno paralelo |
| `First Trend Opened` sin backend, solo `sessionStorage` | Aceptable: es una métrica de comportamiento de sesión de navegador, no de identidad de usuario; documentado en `ANALYTICS_EVENT_MAP.md` |
| Cambiar `/pricing` rompe el checkout | El formulario y su lógica (`PricingCheckout.tsx`) no se tocan más que para añadir dos `track()`; cubierto por test de regresión de checkout ya existente + nuevo E2E |
| Placeholder de captura se queda así mucho tiempo | Se marca explícitamente como deuda pendiente en el informe final, con instrucciones exactas de qué añadir |
| Resend sigue en dominio de pruebas | Documentado como riesgo aceptado y explícito en el checklist de reactivación de Meta — no bloquea el resto de la fase |

## Plan de pruebas

1. Backend: `pytest` completo (suite existente + nuevos tests de los dos eventos server-side).
2. Frontend: `npx tsc --noEmit`, `npm run build`, Playwright smoke ampliado (ver criterios de aceptación).
3. QA manual en producción tras el despliegue (checklist de la sección 18 del brief), incluyendo un checkout real hasta Stripe sin completar el cobro.

## Plan de rollback

Todo el cambio vive en un commit (o serie corta de commits) sobre `main`, desplegado vía Railway. Rollback: `railway redeploy` al deployment anterior de `trendhunter-frontend`/`trendhunter-backend`, o `git revert` del commit si hace falta revertir en el propio repositorio. No hay migraciones de base de datos en esta fase — el rollback es puramente de código, sin riesgo de estado inconsistente.

## Criterios de aceptación

Los del brief, sección 19, sin recortes. Se verifican uno a uno en `PHASE_2_RELEASE_REPORT.md`.
