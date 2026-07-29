# 05 — Engineering Standards

**AI Trend Hunter · Estándar oficial de ingeniería**
Versión 1.0 · Julio 2026 · Propietario: Lead Engineer (Claude Code) · Auditor: Codex · Árbitro: CTO

Este documento es normativo: define cómo se escribe, revisa, prueba y entrega el código. Aplica a todo el repositorio (`backend/`, `frontend/`, `scripts/`, `governance/`, `docs/`). El proceso de release completo está en [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md); este documento define los estándares que ese proceso exige.

---

## 1. Definition of Ready (DoR)

Una tarea está lista para empezar cuando:
- [ ] Tiene hipótesis o motivo escrito (plantilla de iniciativa de [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §2.2, o referencia a bug/incidente concreto).
- [ ] Tiene criterio de éxito verificable ("el usuario puede X", "el endpoint devuelve Y", "la métrica Z se instrumenta").
- [ ] Se sabe si toca área sensible (auth, billing, datos, endpoint público) → si sí, revisión de Codex pre-asignada.
- [ ] Se sabe si es reversible → si no, aprobación previa del CEO ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §2.3).
- [ ] Cabe en ≤1 semana; si no, se trocea antes de empezar.

## 2. Definition of Done (DoD)

Una tarea está terminada cuando — y solo cuando — todo esto es cierto:
- [ ] Código escrito conforme a este estándar.
- [ ] Tests: los nuevos cubren el cambio; **la suite completa** está en verde (no solo los nuevos).
- [ ] Si el cambio nació de un bug: existe test de regresión que falla sin el fix.
- [ ] Revisado (sección 4) si toca área sensible.
- [ ] Desplegado a producción con estado `SUCCESS`.
- [ ] **Verificado en producción real**: la funcionalidad se ejercitó de verdad (petición real, navegación real, consulta real a la BD). El deploy no cierra la tarea; la verificación sí.
- [ ] Sentry limpio tras la verificación.
- [ ] Si hubo aprendizaje no obvio: documentado (informe en `/docs` o comentario de código donde aplique).

---

## 3. Git: branching, commits, PRs

### 3.1 Branching strategy
- **Trunk-based development sobre `main`.** `main` es siempre desplegable; Railway despliega automáticamente cada push a `main`.
- A escala actual (un solo ingeniero ejecutor), los commits directos a `main` son aceptables **si** el cambio pasó tests y, cuando toca área sensible, revisión previa. Con el primer ingeniero humano contratado, se pasa a PRs obligatorias con la misma base: ramas cortas (`fix/...`, `feat/...`, vida <3 días), merge a `main`, borrado de rama.
- Prohibido: ramas de larga vida, "develop" intermedio, release branches. La complejidad de Git Flow clásico no compra nada a esta escala.

### 3.2 Commits
- Mensaje: primera línea imperativa y específica (≤72 chars), cuerpo explicando **por qué** (el "qué" ya lo dice el diff). El historial real del repo es el ejemplo a seguir: cada fix relevante narra síntoma → causa raíz → solución.
- Un commit = un cambio lógico. No mezclar refactor + fix + feature en un commit.
- Nunca commitear: secretos, `.env`, credenciales, dumps de datos, artefactos de build.

### 3.3 Pull Requests (cuando aplican)
- Pequeñas (<400 líneas de diff efectivo como guía; si es más grande, trocear).
- Descripción: qué, por qué, cómo se probó, y qué NO cubre.
- CI en verde es condición necesaria para merge, nunca negociable.

---

## 4. Code Review

- **Quién revisa:** Codex revisa a Claude Code; Claude Code revisa a Codex; a los humanos futuros los revisa cualquiera de los dos + un humano si el cambio es sensible. **Nadie aprueba su propio trabajo.**
- **Revisión obligatoria** (bloqueo hasta aprobar) si el cambio toca: autenticación/sesiones, billing/Stripe, manejo de datos personales, endpoints públicos nuevos, migraciones de datos, o configuración de seguridad (CORS, CSP, rate limiting).
- **Revisión opcional pero recomendada:** refactors grandes, cambios de scoring/heurísticas (afectan al producto directamente).
- **Qué busca la revisión, en orden:** (1) corrección — ¿hay un caso de entrada/estado que rompa esto?, (2) seguridad — ¿fail closed? ¿validación en el punto de paso obligatorio?, (3) simplicidad — ¿hay una versión más simple?, (4) consistencia con el código circundante. El estilo lo vigilan las herramientas, no los revisores.
- **Independencia real:** la revisión se hace sin compartir el contexto de la conversación donde se escribió el código ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §2.4).

---

## 5. Testing y QA

### 5.1 Pirámide real de este proyecto
1. **Tests de API/contrato (pytest + TestClient)** — la capa principal (81 tests hoy). Cada endpoint: caso feliz, validación (422), auth (401/404), y casos de negocio.
2. **Tests de regresión** — cada bug de producción deja uno, nombrado descriptivamente y con docstring que cuenta la historia real (`test_stripe_webhook_marks_trial_cancellation_scheduled_via_cancel_at` es el patrón).
3. **E2E smoke (Playwright)** — lo mínimo que debe estar vivo tras cada deploy: páginas públicas renderizan, el paywall se aplica, el formulario clave existe.
4. **QA manual en producción** — para flujos con dinero real o proveedores externos (checkout completo, cancelación, entrega de email): se ejercitan de verdad, con evidencia, según [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) fase 10.

### 5.2 Reglas
- Un test rojo bloquea el deploy. Un test flaky se arregla o se elimina con decisión escrita — no se reintenta hasta que pase.
- Los tests monkeypatchean los servicios externos (Stripe, Resend, CAPI, Plausible); jamás llaman a servicios reales.
- Los tests de webhooks firman payloads de verdad (HMAC real contra secreto de test) — probar la verificación de firma, no saltársela.
- Datos de test únicos por ejecución (`uuid4` en emails/IDs) para no acoplar tests entre sí.
- Cobertura: no hay objetivo numérico de cobertura. El objetivo es: **todo camino con dinero, auth o datos de cliente tiene test**. La cobertura por porcentaje invita a tests decorativos.

---

## 6. CI / CD

- **CI (GitHub Actions):** en cada push — suite de backend + build de frontend + smoke. CI rojo = no se despliega nada más hasta arreglarlo (la rama está rota para todos).
- **CD (Railway):** push a `main` → build → deploy automático de los servicios afectados. El pipeline de deploy no es el final: la fase de verificación en producción ([08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) fase 10) es parte del delivery.
- **Rollback:** la vía rápida es `railway redeploy` del deployment anterior o revert del commit. Todo cambio arriesgado debe conocer su rollback **antes** de desplegarse.
- **Migraciones:** aditivas por defecto (añadir columnas nullable, nuevas tablas). Las destructivas (drop, rename, cambio de tipo) exigen: plan escrito, backup verificado, y ventana acordada con el CEO.

---

## 7. Seguridad (estándar de código)

Complementa la doctrina de [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §5. Reglas de implementación:

- **Fail closed:** ausencia de configuración de una protección = denegar (patrón `require_admin_key`).
- **Identidad solo de la sesión firmada**, jamás del body/query (regresión IDOR cubierta por test).
- **Validación centralizada en el punto de paso obligatorio**, no solo en los bordes (lección del bypass del filtro de relevancia: los gates críticos viven en `DetectorService`, no solo en los collectors).
- **Idempotencia en todo manejador de webhook** (guardia por identificador único antes de efectos secundarios no idempotentes).
- **Rate limiting en todo endpoint público de escritura** (registro en `RATE_LIMITED_PATHS` al crear el endpoint, no después).
- **Pydantic valida todo input** con límites explícitos (longitudes, patrones, rangos). Normalización (trim, lowercase de emails) en validators, no dispersa.
- **Secretos:** solo env vars; los validadores de `Settings` rechazan defaults inseguros en producción; todo servicio nuevo de Railway recibe el set completo de variables requeridas (lección del cron caído por `JWT_SECRET` ausente).
- Producción no expone `/docs`, `/redoc` ni `/openapi.json`.

---

## 8. Observabilidad y logging (estándar de código)

- Todo proceso de arranque independiente (API, cron, scripts) inicializa Sentry si `SENTRY_DSN` existe.
- Fallos operativos de proveedores externos (Stripe 4xx/5xx, Resend ≥400) se capturan **explícitamente** en Sentry — un `HTTPException` controlado no llega solo.
- Logging: nivel INFO para hitos de proceso (qué corrió, cuánto procesó), ERROR con contexto para fallos. Nunca loguear: secretos, tokens, cuerpos completos de peticiones con datos personales.
- Los procesos batch registran su ejecución en `agent_executions` (fuente de verdad consultable; los logs de plataforma pueden perderse, la BD no).
- Helpers de integraciones de analytics/eventos: **nunca lanzan** (never-throw); fallan a log + Sentry sin romper el flujo del usuario.

---

## 9. Performance

- Presupuestos actuales (holgados a esta escala, revisados al escalar — [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §8): TTFB de páginas públicas <1s; endpoints de API p95 <300ms; ninguna query >100ms p95.
- Regla de oro: **no optimizar sin medir**. La optimización especulativa se rechaza en review.
- N+1 y queries en bucle: prohibidos en código nuevo; los existentes se cazan cuando duelan.
- El frontend usa `Promise.all` para fetches independientes (patrón ya establecido en el dashboard).

---

## 10. Naming y convenciones

- **Python:** snake_case; módulos por dominio (`services/`, `api/v1/`, `models/`, `schemas/`); type hints en firmas públicas; docstrings que explican propósito y, cuando existe, la historia ("por qué es así") — el código del repo ya sigue este patrón y es el ejemplo canónico.
- **TypeScript/React:** componentes PascalCase, funciones camelCase; componentes de servidor por defecto, `"use client"` solo cuando hay interactividad.
- **Nombres internos ≠ nombres de UI:** los identificadores internos (p.ej. `mvp_heuristic_detector`) jamás se muestran crudos al cliente; siempre hay una capa de etiqueta de presentación.
- **API:** rutas REST en plural (`/trends`, `/signups`), versionadas (`/api/v1/`), respuestas con schemas Pydantic explícitos (nunca dicts sueltos).
- **Comentarios:** explican restricciones y porqués que el código no puede expresar; nunca narran el qué. Los comentarios que cuentan la historia de un bug real (por qué existe este guard) son bienvenidos y ya son práctica del repo.

## 11. Refactoring

- Se refactoriza: (a) cuando la duplicación ya causó un bug o una divergencia (lección real: `RELEVANCE_TERMS` duplicado en dos collectors → consolidado en `text_filters.py` como single source of truth), (b) como parte de una tarea que toca esa zona (regla del boy-scout, con moderación), (c) cuando una iniciativa priorizada lo exige.
- No se refactoriza: por estética, por "modernizar", ni en áreas sin tests (primero se ponen tests, luego se refactoriza).
- Un refactor no cambia comportamiento; si lo cambia, son dos commits (refactor + cambio), no uno.

## 12. Documentación

- **El repo es la documentación:** `/governance` (cómo funciona la empresa), `/docs` (informes, auditorías, handoffs), docstrings y comentarios (el código), historial de git (la cronología).
- Cada incidente o auditoría relevante genera informe en `/docs` (práctica ya establecida: QA reports, security reports, handoffs).
- Scripts one-off en `backend/scripts/` con docstring que explica qué hacen, por qué existen y si son reversibles. Los scripts de diagnóstico puntual que ya no sirven se borran.
- README: siempre suficiente para levantar el entorno local en <1 hora (se valida antes de cada contratación — [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §9.5).
