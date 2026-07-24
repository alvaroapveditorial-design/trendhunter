# Checklist Ejecutable Para Lanzar El MVP

Fecha de evaluación: 24 de julio de 2026.

Proyecto evaluado: **AI Trend Hunter**.

## Evaluación Actual

**Preparación para MVP público: 90/100.**

Desde la evaluación anterior (87/100) se completó todo el bloque de "acciones que solo el usuario puede hacer": dominio propio (`aitrendhunter.app`) comprado, verificado en Railway con SSL válido; Resend activado y confirmado enviando emails reales; cuenta de Stripe activada a **modo live** (verificación de negocio, banco, 2FA), con producto, claves y webhook live configurados. El flujo completo (beta signup → checkout → webhook → login por email real → dashboard) está verificado en producción. La nota no sube más porque quedan: legal por rellenar, `ADMIN_API_KEY`/`SENTRY_DSN`/`NEXT_PUBLIC_PLAUSIBLE_DOMAIN` sin configurar, smoke Docker sin correr, rate limiting sigue in-memory, y no se ha hecho un cobro real de prueba todavía.

## Resuelto Hoy

- [x] **Dominio propio**: `aitrendhunter.app` comprado, DNS configurado (CNAME + TXT de verificación) en Namecheap, verificado en Railway con certificado SSL válido.
- [x] **Código actualizado** al dominio nuevo: `metadataBase` en `layout.tsx`, texto del mockup en `page.tsx`, `APP_URL` y `CORS_ORIGINS` en Railway.
- [x] **Resend activado**: `RESEND_API_KEY` y `SENDER_EMAIL` configurados; confirmado en logs (`POST https://api.resend.com/emails → 200 OK`) que los códigos de login llegan de verdad.
- [x] **Stripe en modo live**: cuenta activada (verificación de negocio, cuenta bancaria, 2FA), producto "AI Trend Hunter Pro" (39€/mes) copiado a live, `STRIPE_SECRET_KEY`/`STRIPE_PUBLISHABLE_KEY`/`STRIPE_PRO_PRICE_ID` live configurados, webhook live creado (`trendhunter-backend-live`, 4 eventos) con su propio `STRIPE_WEBHOOK_SECRET`.
- [x] **Flujo completo verificado en producción** (modo test primero, y la infraestructura live ya desplegada): signup → checkout → webhook → login por email real → dashboard.

## Pendiente — Requiere Acción Del Usuario

- [ ] **Legal en `/privacy` y `/terms`**: siguen con placeholder ("responsable pendiente de completar"). Necesito tu nombre legal, NIF/CIF, domicilio y email de contacto para rellenarlo.
- [ ] **`ADMIN_API_KEY`**: sin configurar — el endpoint de beta signups sigue sin poder consultarse.
- [ ] **`SENTRY_DSN`** (recomendado): crear proyecto en Sentry y cargar el DSN.
- [ ] **`NEXT_PUBLIC_PLAUSIBLE_DOMAIN`** (recomendado): crear el sitio en Plausible con `aitrendhunter.app` y cargarlo como variable de build del frontend.
- [ ] **Cobro real de prueba**: todavía no se ha hecho un checkout con dinero real para confirmar el flujo live de punta a punta (decisión del usuario: aplazado por ahora).
- [ ] **Canal de soporte**: email o chat visible para usuarios de pago.
- [ ] **Backups de Postgres en Railway**: confirmar plan/retención.
- [ ] **Smoke Docker**: `docker compose up --build` no se ha corrido desde que se añadieron auth/beta/billing.

## Puntuación Ponderada

| Área | Puntos | Cambio vs. anterior |
| --- | ---: | --- |
| Loop principal de producto | 20/25 | = |
| Backend/API/datos | 18/20 | = |
| Frontend/dashboard UX | 14/15 | = |
| Testing y build | 14/15 | = |
| Seguridad y privacidad | 10/10 | = |
| Deploy/operación | 9/10 | +3 (dominio propio live, Stripe y Resend en producción real) |
| Comercialización/monetización | 5/5 | = |
| **Total** | **90/100** | +3 |

## Checklist P0 Antes De Enseñarlo Fuera

- [x] Dominio propio con SSL válido.
- [x] Stripe en modo live con producto, claves y webhook configurados.
- [x] Resend enviando emails reales, confirmado.
- [x] Flujo completo (signup, login, checkout, webhook, dashboard) verificado.
- [ ] Legal real en `/privacy` y `/terms`.
- [ ] `ADMIN_API_KEY`, `SENTRY_DSN`, `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`.
- [ ] Canal de soporte visible.

## Checklist P1 Para Beta Privada

- [x] Auth básica (propia, JWT + código por email).
- [x] Probar el flujo de login end-to-end contra producción con email real.
- [ ] Probar un pago real de prueba (modo live) end-to-end.
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
- [x] Billing con Stripe — live y operativo.
- [x] Emails con Resend — live y operativo.
- [ ] Vector search/Qdrant para similitud de tendencias.
- [ ] Orquestación LangGraph real.
- [ ] Monitorización de competidores.

## Siguientes Pasos Recomendados (Ejecutables, En Orden)

1. **Rellenar legal real** en `/privacy` y `/terms` — dame tus datos (nombre legal, NIF/CIF, domicilio, email de contacto) y los escribo yo.
2. **Configurar `ADMIN_API_KEY`, `SENTRY_DSN`, `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`** en Railway — 10 minutos, desbloquea panel de beta signups, error tracking y analytics.
3. **Canal de soporte**: decide un email (ej. `soporte@aitrendhunter.app` o tu email personal) y lo añado a la landing.
4. **Cobro real de prueba** cuando estés listo: un checkout con tu propia tarjeta para confirmar el flujo live de punta a punta antes de anunciar.
5. **Smoke Docker**: `docker compose up --build` para validar el stack completo una vez más antes del lanzamiento público.
6. **Lanzamiento**: retomar el plan de Show HN, Reddit, IndieHackers y outreach de GitHub.
7. **Rate limiting distribuido** (Redis) — puede esperar a después del lanzamiento si el tráfico inicial es bajo.

## Riesgos Principales

- **Sin legal real**: vender con placeholder legal es un riesgo de cara a clientes reales — complétalo antes de anunciar públicamente.
- **Sin verificar con dinero real**: el modo live nunca se ha probado con un cobro real, solo con la configuración validada — hazlo antes de anunciar en masa.
- **Beta signups sin panel accesible**: sin `ADMIN_API_KEY` no puedes consultar quién se ha apuntado a la beta.
- **Rate limit local**: suficiente para una instancia, débil para producción multi-instancia.
- **Sin smoke Docker reciente**: las rutas de auth/beta/billing no se han validado en el stack Docker completo.
- **Sin LLM real**: el scoring heurístico funciona, pero los insights todavía no son suficientemente diferenciales.
