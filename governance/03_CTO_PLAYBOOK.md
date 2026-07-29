# 03 — CTO Playbook

**AI Trend Hunter · Manual del CTO**
Versión 1.0 · Julio 2026 · Propietario: CTO (ChatGPT) · Ejecutor principal: Lead Engineer (Claude Code) · Auditor: Codex

Este manual define la filosofía técnica de la empresa y las checklists operativas que la hacen real. Se apoya en [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) (el "cómo" del código) y [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) (el "cómo" de los releases).

---

## 1. Filosofía técnica

1. **La tecnología existe para el negocio, no al revés.** El stack actual (FastAPI + Postgres + Next.js en Railway, Stripe, Resend, Plausible, Sentry) es deliberadamente aburrido. El presupuesto de innovación se gasta en el producto (detección de señales), no en la infraestructura.
2. **Coste marginal ~cero es una decisión de arquitectura.** El motor de detección es heurístico, sin LLM en el camino crítico. Cada cliente nuevo cuesta céntimos. Romper esta propiedad exige aprobación del Consejo — es la base del margen del negocio (los costes fijos totales, ~50-100 €/mes, se cubren con 2-3 suscripciones).
3. **Producción es la única verdad.** "Funciona en tests" es una hipótesis; "lo verifiqué en producción con datos reales" es un hecho. Todo release termina con verificación en vivo, no con el deploy.
4. **Fallar en silencio es el peor fallo.** El incidente formativo de esta empresa: un cron que se disparaba puntualmente cada día y moría en 0,26 segundos por una variable de entorno ausente — días de datos congelados sin una sola alerta. De ahí las reglas: todo proceso batch reporta a Sentry, y toda automatización nueva se verifica en su **primer disparo real**, no solo en su configuración.
5. **Reversibilidad por defecto.** Soft-deletes (`is_active`), migraciones aditivas, scripts de limpieza reversibles, feature flags cuando toque. Lo irreversible se trata como lo que es: excepcional y aprobado.
6. **La deuda técnica se paga cuando duele, no cuando incomoda.** Refactorizar sin dolor medido es procrastinación con buena prensa. Pero la deuda que ya mordió (duplicación que causó un bug, filtro bypasseable) se paga inmediatamente y con test de regresión.

---

## 2. Responsabilidades del CTO

- Proteger las propiedades arquitectónicas del negocio: coste marginal, simplicidad del stack, independencia de proveedores no críticos.
- Mantener el roadmap técnico alineado con el comercial (hoy: nada que no acerque a 100 clientes).
- Decidir qué deuda se paga y cuándo (con input del Lead Engineer y de Codex).
- Garantizar que la seguridad y la observabilidad no se erosionan release a release.
- Preparar la organización técnica para el siguiente orden de magnitud **antes** de necesitarlo, pero no dos órdenes antes (sección 8).

---

## 3. Criterios de arquitectura

Ante cualquier decisión de arquitectura, evaluar en este orden:

1. **¿Es la opción más simple que resuelve el problema de hoy y sobrevive al de dentro de 6 meses?** No 5 años: 6 meses. A esta escala, optimizar para 5 años es especular.
2. **¿Añade un proveedor, un servicio o una tecnología nueva?** Cada adición es una superficie de fallo, una factura y una curva de aprendizaje. La respuesta por defecto es no.
3. **¿Introduce coste variable por cliente?** Si sí, al Consejo.
4. **¿Es reversible?** Una migración de datos destructiva, un cambio de proveedor de pagos o un rediseño del modelo de datos exigen diseño escrito y revisión de Codex antes de una línea de código.
5. **¿Cómo falla?** Todo componente nuevo debe responder: qué pasa cuando falle (no "si"), quién se entera, y cómo se recupera.

**Decisiones ya tomadas que no se reabren sin datos nuevos:** monolito FastAPI (no microservicios), Postgres para todo (no hay volumen que justifique otra cosa), heurísticas sin LLM en ingesta, Railway como plataforma (hasta que el coste o los límites duelan), rate limiting in-memory (suficiente a un solo proceso; se revisa al escalar horizontalmente — ver riesgo TEC-4 en [12_RISK_REGISTER.md](12_RISK_REGISTER.md)).

---

## 4. Deuda técnica

**Registro:** la deuda conocida vive como sección en el acta del Consejo mensual, con tres campos: qué es, qué dolor causa hoy, qué la convertiría en urgente.

**Deuda conocida actual (julio 2026):**
| Deuda | Dolor hoy | Se vuelve urgente cuando |
|---|---|---|
| Rate limiting in-memory | Ninguno (1 proceso) | Se escale a >1 réplica de backend |
| Proxy frontend no reenvía `Stripe-Signature` | Ninguno (Stripe llama directo al backend) | Algo sensible a cabeceras pase por el proxy |
| `AUTO_CREATE_TABLES` como mecanismo junto a Alembic | Confusión potencial | Primera migración compleja en producción |
| Sender de email `onboarding@resend.dev` (dominio de pruebas de Resend) | Deliverability subóptima, imagen | Antes de escalar adquisición — **prioridad alta** |

**Regla de pago:** deuda que causó un incidente → se paga ya. Deuda que bloquea una iniciativa priorizada → se paga como parte de esa iniciativa. Resto → cola normal con puntuación de [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md).

---

## 5. Seguridad

Estado y doctrina (auditorías previas: `docs/SECURITY_CI_INSTRUMENTATION_REPORT.md`, `docs/PRE_LAUNCH_QA_REPORT.md`):

1. **Fail closed.** Los endpoints admin sin clave configurada deniegan (patrón ya implantado en `require_admin_key`). Toda protección nueva sigue este patrón.
2. **Validación en el punto de paso obligatorio, no solo en el borde.** Lección real: el filtro de relevancia vivía en los collectors y un endpoint raw lo bypasseaba; hoy el gate está centralizado en `DetectorService`. Toda validación crítica debe vivir donde ningún camino pueda esquivarla.
3. **Producción no expone superficies de desarrollo:** `/docs`, `/redoc`, `/openapi.json` deshabilitados; mensajes de error orientados a cliente, jamás trazas ni hosts internos.
4. **Secretos:** solo en variables de entorno de Railway; jamás en el repo, jamás en logs, jamás en documentos. Los secretos usados transitoriamente en diagnóstico no se persisten. Validadores de arranque rechazan valores por defecto en producción (`JWT_SECRET`, `SECRET_KEY`) — y **todo servicio nuevo que comparta el código debe recibir esas variables** (lección del incidente del cron).
5. **Webhooks:** firma verificada siempre; manejadores idempotentes (Stripe entrega at-least-once — ya mordió una vez con analytics duplicados; el patrón de guardia por identificador único es obligatorio).
6. **Sesiones:** cookie firmada, sin IDOR (la identidad sale de la sesión, nunca del body — regresión cubierta por test).
7. Revisión de seguridad de Codex obligatoria en: auth, billing, endpoints nuevos públicos, y cualquier cosa que toque datos personales.

---

## 6. Observabilidad

**Doctrina: cada capa responde una pregunta distinta.**
- **Sentry** (backend + cron): ¿algo está roto? Todo proceso, incluidos los batch standalone, inicializa Sentry. Excepciones "esperadas" que indican fallo operativo real (Stripe rechaza, Resend falla) se capturan explícitamente — Sentry no ve los `HTTPException` controlados por sí solo.
- **Plausible**: ¿qué hacen los usuarios? Eventos de producto (`Dashboard Viewed`, `Trend Viewed`, `Trial Started`...) tanto cliente como servidor (Events API para los que ocurren en webhooks, sin navegador).
- **Meta Pixel/CAPI**: ¿qué convierte en publicidad? Con deduplicación por `event_id`.
- **`agent_executions` (Postgres)**: ¿corrió el pipeline y qué hizo? Es la fuente de verdad de la ingesta — los logs de Railway pueden no mostrar los disparos de cron; la base de datos no miente.

**Reglas:**
- Ningún fallo silencioso: si un proceso puede fallar sin que Sentry lo sepa, ese proceso está mal instrumentado.
- La verificación de una automatización incluye siempre su primer disparo real (no solo la configuración).
- Pendiente conocido: alertas proactivas (email/push cuando el cron no corra o Sentry acumule errores). Hoy la detección es reactiva; aceptable a esta escala, inaceptable a partir de ~100 clientes (sección 8.1).

---

## 7. Calidad, releases y definición de excelencia técnica

- Estándares de código, tests y CI en [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md). Proceso completo de release en [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md).
- **Excelencia técnica aquí significa:** (1) el cliente ve datos correctos y frescos, (2) los cobros son exactos, (3) nada falla en silencio, (4) cualquier miembro del equipo puede entender cualquier módulo en una tarde, (5) desplegar es aburrido. No significa: la última tecnología, cobertura del 100%, ni microservicios.
- La suite de tests del backend (81 tests hoy) corre en verde siempre. Un test rojo bloquea todo deploy sin excepciones ni "es flaky" — un test flaky se arregla o se borra con decisión escrita.

---

## 8. Preparación por escala

### 8.1 Preparados para 100 clientes (horizonte actual)
Lo que falta y debe hacerse **antes** de llegar:
- [ ] Dominio de email propio verificado en Resend (adiós `onboarding@resend.dev`) — afecta deliverability de los códigos de login, que son la puerta del producto.
- [ ] Alerta proactiva de cron caído (el check programado manual de hoy → chequeo automático diario que avise si no hay `agent_executions` frescas).
- [ ] Alerta de errores Sentry por email al CEO configurada y probada.
- [ ] Backup de Postgres verificado: no solo que Railway lo haga, sino **restaurar uno de verdad** en un entorno temporal y documentar el procedimiento (RPO/RTO objetivo: perder <24h de datos, recuperar en <4h).
- [ ] Runbook de incidentes de 1 página: qué mirar (Sentry → `agent_executions` → logs Railway → Stripe), en qué orden, y qué puede tocar cada rol sin aprobación ([01_COMPANY_CHART.md](01_COMPANY_CHART.md), regla de urgencia).

Lo que explícitamente NO se hace aún: réplicas, colas, caché distribuida, Kubernetes, multi-región. El monolito en Railway aguanta 100 clientes con margen enorme (el dashboard es lectura de una tabla pequeña).

### 8.2 Preparados para 1.000 clientes
Disparadores y acciones (no antes de las señales):
- [ ] Rate limiting a Redis u otro almacén compartido **cuando** haya >1 réplica.
- [ ] Réplicas del backend + healthchecks agresivos cuando p95 de latencia > 500ms sostenido.
- [ ] Índices y revisión de queries cuando alguna consulta supere 100ms p95 (hoy trivial: decenas de trends).
- [ ] Soporte: el email con reply-to deja de escalar; herramienta de tickets ligera + primera contratación de soporte ([01_COMPANY_CHART.md](01_COMPANY_CHART.md), Fase 1-2).
- [ ] Staging environment real (hoy: se prueba en local + verificación en producción; a 1.000 clientes el blast radius ya no lo permite).
- [ ] Revisión de límites de Railway (conexiones Postgres, throughput) y plan B de plataforma documentado (no ejecutado: documentado).
- [ ] Primer ingeniero humano con ownership de guardias (checklist 9.5 antes de contratar).

### 8.3 Preparados para 10.000 clientes
Se planifica en serio solo al superar ~2.000 (planificar dos órdenes de magnitud por adelantado es ficción). Direcciones ya previsibles:
- Separación del pipeline de ingesta como servicio independiente con cola (el cron único deja de bastar si la frecuencia sube o las fuentes se multiplican).
- Postgres gestionado con réplicas de lectura; el dashboard es read-heavy y cacheable por construcción (los datos cambian 1 vez al día).
- CDN/edge para el frontend; el dashboard puede pre-renderizarse por franjas.
- Equipo: VP Engineering humano, guardias formales, SLOs escritos con presupuesto de error.
- Cumplimiento: a esa escala habrá clientes empresa → DPA, subprocesadores documentados, probablemente SOC2 en el horizonte. Coordinar con riesgos LEG-* de [12_RISK_REGISTER.md](12_RISK_REGISTER.md).

---

## 9. Checklists operativas

### 9.1 Diaria (automatizable; hoy la ejecuta el Lead Engineer cuando hay sesión activa)
- [ ] ¿Sentry sin errores nuevos? (si hay: triaje inmediato, ¿afecta a clientes?)
- [ ] ¿`agent_executions` tiene filas de hoy ~08:00 UTC con `status=success`?
- [ ] ¿El dashboard muestra datos de hoy? (spot-check de 1 minuto)
- [ ] ¿Stripe sin webhooks fallidos pendientes de reintento?

### 9.2 Semanal (antes del Consejo)
- [ ] Suite completa de tests en verde local y CI.
- [ ] Revisión de las métricas técnicas del playbook ([11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md), sección ingeniería).
- [ ] ¿Algún error de Sentry recurrente sin causa raíz asignada?
- [ ] ¿Calidad de datos: contenido off-topic o no-inglés visible en el dashboard? (los dos bugs reales de esta clase ya tienen tests, pero el spot-check visual sigue — los filtros heurísticos fallan por vocabulario, no por lógica)
- [ ] ¿Dependencias con CVEs conocidas? (revisión rápida)

### 9.3 Mensual
- [ ] Revisión del registro de deuda técnica (sección 4) — ¿algo cruzó su umbral de urgencia?
- [ ] Restaurar backup en entorno temporal (una vez implantado el procedimiento de 8.1).
- [ ] Revisión de costes de infraestructura vs. presupuesto.
- [ ] Rotación de credenciales si algún secreto tiene >6 meses o hubo sospecha de exposición.
- [ ] Revisión de riesgos técnicos en [12_RISK_REGISTER.md](12_RISK_REGISTER.md).

### 9.4 Antes de cada deploy a producción
La checklist completa vive en [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md), fases 8-10. Resumen mínimo inviolable:
- [ ] Tests en verde (suite completa, no solo los nuevos).
- [ ] Revisión de Codex si toca auth/billing/datos/endpoint público.
- [ ] Migraciones: aditivas, o con plan de rollback escrito.
- [ ] Verificación en producción real tras el deploy (el deploy no cierra la tarea; la verificación sí).
- [ ] Sentry limpio en los 15 minutos posteriores.

### 9.5 Antes de contratar ingenieros humanos
- [ ] ¿El dolor está medido? (incidentes sin cubrir, iniciativas bloqueadas por capacidad, >X horas/semana de trabajo técnico que los agentes no pueden hacer con autonomía segura)
- [ ] README de onboarding: levantar el entorno en <1 hora sin ayuda.
- [ ] `/governance` y `/docs` al día — el nuevo ingeniero hereda la memoria institucional escrita, no oral.
- [ ] Definidos: qué ownership recibe (guardias, incidentes, un dominio concreto), a quién reporta ([01_COMPANY_CHART.md](01_COMPANY_CHART.md)), y cómo colabora con los agentes (los agentes multiplican, el humano posee).
- [ ] Presupuesto: coste total anual < lo que la retención/velocidad ganada justifica. Si no se puede estimar, no es el momento.
