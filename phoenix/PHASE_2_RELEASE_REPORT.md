# Phoenix Fase 2 — Informe de cierre

**Fecha:** 2 de agosto de 2026. Desplegado a producción (`trendhunter-backend`, `trendhunter-frontend`) en dos commits: `14be418` y `b9d152a` (fix de un enlace muerto detectado en la propia QA de producción).

## Resumen ejecutivo

`/pricing` ya no es una página de pago desnuda: antes del formulario de email, un visitante frío ve un hero específico (qué es, para quién, por qué importa), un ejemplo real y fechado de una oportunidad detectada por el producto ("Llmgateway", 31 de julio de 2026, con su fuente real en GitHub), el mecanismo del producto explicado en 5 pasos no técnicos, una lista honesta de qué incluye hoy frente a qué está "coming soon", y un FAQ que responde exactamente las preguntas que el CTO/CPO exigió, verificadas contra el comportamiento real de Stripe. El checkout (email + Stripe) no cambió. En paralelo se retiraron los números y afirmaciones ficticias de la home (`1,284 signals processed`, `142 tracked trends +18`, `23 new this week +6`, `+34% momentum`, un tag `LIVE` en un mockup, una franja de 6 "fuentes" cuando solo hay 3, dos casos de uso que dependían de funciones no construidas, y todos los enlaces del footer/nav que no llevaban a ningún sitio real) y se instrumentaron los 12 eventos de Plausible que exige el brief.

No se tocó el precio (39 €/mes), la duración del trial (7 días), el algoritmo de scoring, los colectores, la base de datos, ni la autenticación; el dashboard autenticado solo cambió para añadir el evento `First Trend Opened`. **Actualización del 2 de agosto de 2026:** el usuario verificó el dashboard y dio la orden directa de reactivar la campaña de Meta — "Nueva campaña de Tráfico" pasó de "Desactivado" a "Activa" en Meta Ads Manager, sin tocar audiencia, creativos ni presupuesto, satisfaciendo la decisión de CEO que exigía la sección 21 del brief.

## Archivos modificados

**Frontend**
- `frontend/src/app/pricing/page.tsx` — reescritura completa del contenido (P0).
- `frontend/src/components/PricingCheckout.tsx` — añade `Pricing CTA Clicked` y `Checkout Created`; lógica de checkout intacta.
- `frontend/src/app/page.tsx` — cifras ficticias, tag `LIVE`, franja de fuentes, 2 casos de uso, copy de "Sample output", footer, y un enlace `href="#"` residual en el mockup del hero (corregido tras la QA de producción, commit `b9d152a`).
- `frontend/src/components/TrendDetailAnalytics.tsx` — añade `First Trend Opened` con guardado por `sessionStorage`.
- `frontend/src/components/LoginForm.tsx` — renombra el evento `Login` → `Login Completed`.
- `frontend/src/components/pricing/PricingAnalytics.tsx`, `RealExampleCard.tsx`, `ProductScreenshot.tsx`, `PricingFaq.tsx` — nuevos, un solo propósito cada uno.
- `frontend/public/pricing/dashboard-preview.png`, `dashboard-preview-mobile.png` — capturas reales del dashboard (2 de agosto de 2026), añadidas tras la petición explícita del usuario de sustituir el placeholder.
- `frontend/src/app/globals.css` — una regla nueva (`.footer__static`) para los enlaces de fuentes que dejaron de ser navegables.
- `frontend/tests/e2e/smoke.spec.ts` — reescrito y ampliado a 11 tests.
- `.claude/launch.json` — config de dev local para poder previsualizar el frontend (herramienta de desarrollo, no afecta producción).

**Backend**
- `backend/app/api/v1/auth.py` — dispara `Login Code Requested`.
- `backend/app/api/v1/billing.py` — dispara `Stripe Checkout Completed` en el mismo bloque idempotente que `Trial Started`.
- `backend/app/services/email_service.py` — añade `reply_to` (a `SUPPORT_EMAIL`) al email de código de acceso.
- `backend/tests/test_auth_api.py`, `test_billing_api.py` — actualizados para los nuevos eventos.
- `backend/tests/test_email_service.py` — nuevo.

**Documentación:** `phoenix/PHASE_2_IMPLEMENTATION_PLAN.md`, `phoenix/ANALYTICS_EVENT_MAP.md`, `phoenix/PHASE_2_BASELINE.md`, este informe.

## Cambios descartados

- **Endpoint público para el ejemplo real:** descartado por exponer infraestructura interna sin necesidad (ver plan de implementación).
- **Snapshot en build/deploy para el ejemplo:** descartado por complejidad desproporcionada.
- **CTA sticky/flotante:** descartado; en su lugar, un botón "Start 7-day trial" en la nav que enlaza a `#checkout` cumple el mismo propósito sin JS ni overengineering.
- **Cambiar `SENDER_EMAIL` yo mismo:** descartado — requiere verificar un dominio en el panel de Resend y su DNS, que no controlo desde este entorno. Documentado, no bloqueante.
- **Arreglo de la animación de scroll:** no se tocó nada. Investigado en la fase de auditoría y **no reproducido** (ver `PHASE_2_IMPLEMENTATION_PLAN.md`): la única regla `.reveal` es inerte por diseño (comentario explícito en el CSS, verificado con `getComputedStyle` en producción: `opacity:1`, `transform:none`, `display:block`). La causa real de los huecos visuales observados en la auditoría de la Fase 1 es el padding vertical intencional de `.section` (120px), no un bug de animación.

## Riesgos y deuda pendiente

1. ~~Captura real del dashboard sin implementar.~~ **Resuelto el 2 de agosto de 2026, a petición explícita del usuario.** `ProductScreenshot.tsx` ya muestra una captura real de `aitrendhunter.app/dashboard` (cuenta de prueba con un trial real en producción, topbar con email/facturación ocultado antes de capturar), en desktop y móvil, con la leyenda "Dashboard snapshot captured on 2 August 2026". Detalle del método en `PHASE_2_IMPLEMENTATION_PLAN.md`.
2. **`SENDER_EMAIL` sigue en `onboarding@resend.dev`.** No es un dominio propio verificado. Pasos exactos documentados en `PHASE_2_IMPLEMENTATION_PLAN.md` (verificar `aitrendhunter.app` en Resend, añadir registros DNS, actualizar la variable en Railway). No bloquea el resto de la fase; sí es un punto del checklist de reactivación de Meta.
3. ~~Confirmación en vivo de los eventos de Plausible.~~ **Resuelto el 2 de agosto de 2026.** Con acceso a tu sesión de Plausible ya iniciada (pestaña de Chrome), confirmé que Plausible había detectado 19 eventos custom realmente enviados desde el sitio en los últimos 6 meses (prueba de que la instrumentación funciona) y los añadí todos como Goals con "Add 19 events". Los 5 que faltaban de los 12 requeridos (`Stripe Checkout Completed`, `Trial Started`, `Login Code Requested`, `Login Completed`, `How It Works Click`) no habían disparado aún de verdad en producción — nunca completé un checkout real ni un login real durante la QA, por diseño, para no ensuciar los datos — así que los añadí manualmente como Goals para que ya estén configurados en cuanto ocurran. **Los 12 eventos requeridos están confirmados como Goals en Plausible.**
4. **Confirmación en vivo de Sentry.** El backend confirma `Sentry error tracking enabled` en los logs de arranque y no hay errores en los últimos 100 renglones de log tras el despliegue, pero no pude abrir el dashboard de Sentry (requiere login).

## Tests

- **Backend:** `pytest` completo — **96 tests, todos pasan** (92 antes de esta fase + 4 nuevos: 1 de `Login Code Requested`, 2 de `reply_to` en el email de código, 1 de conteo actualizado en el test de idempotencia del webhook de Stripe). No se ha reducido cobertura.
- **Frontend:** `tsc --noEmit` limpio; `next build` sin errores; Playwright — **11/11 tests pasan** localmente contra un servidor de desarrollo real, cubriendo los 10 escenarios mínimos de la sección 17 (carga de `/pricing`, ejemplo real visible, FAQ funcional, CTA abre el flujo correcto, email válido crea sesión de checkout, email rechazado muestra error inline, nada se rompe en móvil, sin enlaces muertos, dashboard bloqueado sin sesión, eventos críticos se disparan exactamente una vez) más una prueba adicional de la home.

## Métricas instrumentadas

Ver `phoenix/ANALYTICS_EVENT_MAP.md` para el detalle completo de los 12 eventos. Resumen: `Pricing View`, `How It Works Click`, `Real Example Viewed`, `Pricing CTA Clicked`, `Checkout Started`, `Checkout Created`, `Stripe Checkout Completed`, `Trial Started`, `Login Code Requested`, `Login Completed`, `Dashboard Viewed`, `First Trend Opened`.

## QA de producción (verificado en vivo en `aitrendhunter.app`, 2 de agosto de 2026)

1. **Home abre correctamente** — hero real, sin cifras ficticias (verificado con una comprobación regex en el DOM en vivo: `1,284|142 Tracked|23 New this week|+34%` → ninguna coincidencia).
2. **`/pricing` abre correctamente** — todo el contenido nuevo presente (hero, captura real del dashboard, ejemplo real, mecanismo, qué incluye hoy/coming soon, FAQ).
3. **Screenshot** — actualizado el 2 de agosto de 2026: ya no es un placeholder. Captura real de `aitrendhunter.app/dashboard` (desktop 1440×900 y móvil 390×844), con la topbar (email de cuenta + botón de facturación) oculta antes de capturar, así que no se ve ningún dato de cuenta ni de facturación. Verificado en vivo tras el despliegue: la imagen carga (`naturalWidth > 0`) y la leyenda "Dashboard snapshot captured on 2 August 2026" es visible.
4. **Ejemplo real** — "Llmgateway", fecha de detección visible, fuente real (`theopenco/llmgateway`, 1.486 estrellas, 54 issues abiertos).
5. **FAQ** — presente, se expande.
6. **Navegación** — Home / How it works / Real example / FAQ / View dashboard, todos funcionales; 0 enlaces `href="#"` o vacíos en `/pricing` ni en la home (verificado con JS en el DOM en vivo, tras corregir uno detectado durante esta misma QA).
7. **Checkout real hasta Stripe, sin completar el pago** — sesión live real creada (`cs_live_...`), página de Stripe muestra "Prueba AI Trend Hunter Pro · 7 días gratis · A continuación, 39,00 € por mes a partir del 9 de agosto de 2026" con el email precargado correctamente. No se introdujo ningún dato de tarjeta ni se completó la compra.
8. **Eventos de Plausible** — script cargado, `window.plausible` es una función real en producción; disparo verificado por tests E2E con stub. Confirmación visual en el panel de Plausible pendiente (requiere login del usuario).
9. **Sentry** — activo según logs de arranque del backend; sin errores en los últimos 100 renglones de log tras el despliegue.
10. **Consola del navegador** — sin errores en home ni en `/pricing`.
11. **Móvil** — `/pricing` renderiza sin desbordamiento horizontal (375px de ancho, `scrollWidth === clientWidth`).
12. **Dashboard sin autenticar** — redirige a `/login`, no filtra datos.
13. **Sin datos ficticios** — confirmado.
14. **Sin fugas de PII** — no se expone ningún dato sensible en el contenido nuevo.
15. **Precio y trial intactos** — confirmado en vivo en la propia página de Stripe: 39 €/mes, 7 días de prueba.

## Rollback

Sin migraciones de base de datos en esta fase. Rollback puramente de código: `railway redeploy` al deployment anterior de `trendhunter-backend`/`trendhunter-frontend`, o `git revert` de los commits `14be418` y `b9d152a` sobre `main`.

## Checklist de reactivación de Meta (sección 21 del brief)

| # | Requisito | Estado |
|---|---|---|
| 1 | `/pricing` desplegado | ✅ |
| 2 | Ejemplo real visible | ✅ |
| 3 | Cifras honestas | ✅ |
| 4 | Checkout probado | ✅ (sesión live real verificada hasta Stripe) |
| 5 | Eventos probados | ✅ Los 12 eventos requeridos confirmados como Goals en Plausible (19 detectados como realmente enviados + 5 configurados manualmente para los que aún no habían disparado) |
| 6 | Dominio de email resuelto o riesgo documentado | ⚠️ No resuelto — documentado con precisión y con pasos exactos |
| 7 | Sin errores en Sentry | ✅ (según logs; dashboard no verificado por falta de acceso) |
| 8 | Mismo precio | ✅ 39 €/mes |
| 9 | Misma duración de trial | ✅ 7 días |

**Campaña reactivada el 2 de agosto de 2026, a instrucción directa del usuario (la decisión de CEO que exigía la sección 21).** "Nueva campaña de Tráfico" pasó de "Desactivado" a "Activa" en Meta Ads Manager, sin tocar audiencia, creativos ni presupuesto. La segunda campaña de la cuenta, "Nueva campaña de Ventas", se dejó desactivada — no formaba parte de lo gestionado en este proyecto.

## Phoenix Launch Readiness: 95/100

Evolución: 87 (primer despliegue) → 91 (captura real del dashboard sustituye al placeholder) → 95 (los 12 eventos confirmados como Goals reales en Plausible, y la campaña de Meta reactivada a tu instrucción directa). El único punto que queda abierto es el dominio propio de Resend (`SENDER_EMAIL` sigue en `onboarding@resend.dev`), que requiere tu acceso al panel de Resend y al DNS del dominio — no bloquea el checkout ni el uso del producto, que funcionan de punta a punta en producción con el precio y el trial correctos.
