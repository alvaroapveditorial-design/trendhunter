# 08 — Release Process

**AI Trend Hunter · Proceso oficial de releases**
Versión 1.0 · Julio 2026 · Propietario: Lead Engineer (Claude Code) · Auditor: Codex · Estándares aplicables: [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md)

Este proceso aplica a **todo** cambio que llegue a producción, incluido el "cambio de una línea" — la historia de esta empresa incluye una variable de entorno ausente que tumbó el pipeline de datos durante días y una etiqueta incorrecta que minaba la credibilidad de todos los números. El tamaño del diff no predice el tamaño del daño.

El pipeline completo:

```
Idea → Descubrimiento → Diseño → Arquitectura → Desarrollo → Testing → QA → Revisión → Deploy → Monitorización → Retrospectiva
```

Las fases 2-4 son proporcionales al riesgo: un fix de copy las atraviesa en un minuto; un cambio de billing las recorre enteras. Lo que nunca es proporcional al riesgo, porque es fijo: tests en verde, verificación en producción y monitorización posterior.

---

## Fase 1 — Idea

**Entrada:** cualquier fuente (bug, entrevista, métrica, Consejo, riesgo).
**Checklist:**
- [ ] Formulada como iniciativa ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §2.2) o como bug con reproducción.
- [ ] Pasó el filtro de las 12 preguntas de [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) §2 (los bugs de producción con clientes afectados lo saltan: son prelación 1).
**Criterio de salida:** tiene dueño, hipótesis/motivo y hueco en la cola semanal (máx. 3).
**Bloqueo:** sin dueño o sin hueco → espera. No hay "lo cuelo rápido".

## Fase 2 — Descubrimiento

**Objetivo:** entender el problema antes de tocar la solución.
**Checklist:**
- [ ] ¿Cuál es la causa raíz / la necesidad real? (para bugs: reproducido y explicado, no solo parcheado el síntoma — el estándar es el diagnóstico del cron: no "no corre", sino "corre y muere en 0,26s por validación de Settings")
- [ ] ¿A quién afecta y cuánto? (datos de Plausible/BD, no intuición)
- [ ] ¿Existe ya algo en el sistema que lo resuelva a medias? (evitar duplicar mecanismos)
**Criterio de salida:** el dueño puede explicar el problema en 3 frases sin mencionar la solución.

## Fase 3 — Diseño

**Objetivo:** decidir la experiencia/el comportamiento antes que la implementación.
**Checklist:**
- [ ] ¿Cómo se comporta para el usuario? (incluye estados de error y vacío — reglas de [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §11)
- [ ] ¿Respeta los principios de producto? (repasar [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md); citar número si alguno está en tensión)
- [ ] ¿Qué eventos lo instrumentan? (principio §13: instrumentado o no existe)
- [ ] Copy revisado: describe el producto real, sin nombres internos, en el idioma del producto.
**Criterio de salida:** comportamiento definido, incluidos los caminos tristes.

## Fase 4 — Arquitectura

**Objetivo:** decidir el cómo técnico al nivel adecuado de ceremonia.
**Checklist:**
- [ ] ¿Toca área sensible (auth, billing, datos, endpoint público, migración)? → diseño escrito breve + revisión de Codex **antes** de codificar.
- [ ] ¿Es reversible? Si no → aprobación CEO previa + plan de rollback escrito.
- [ ] ¿Dónde vive la validación? (en el punto de paso obligatorio, no solo en el borde — [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) §7)
- [ ] ¿Cómo falla y quién se entera? (Sentry, `agent_executions`, alertas)
- [ ] ¿Añade proveedor/tecnología/coste variable? → criterios de [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §3.
**Criterio de salida:** el enfoque cabe en un párrafo y nadie con contexto lo objetó.

## Fase 5 — Desarrollo

**Checklist:**
- [ ] Conforme a [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) (naming, seguridad, observabilidad, comentarios).
- [ ] Commits atómicos con mensajes que explican el porqué.
- [ ] Sin scope creep: lo que surja por el camino se anota como idea nueva (anti-patrón "ya que estamos", [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) §6.2).
- [ ] Sin secretos, sin datos reales de clientes en fixtures.
**Criterio de salida:** el cambio compila, corre localmente y hace lo diseñado.

## Fase 6 — Testing

**Checklist:**
- [ ] Tests nuevos: caso feliz + validación + auth (si aplica) + el caso raro que motivó el cambio.
- [ ] Si es un fix: test de regresión que **falla sin el fix** (verificado), con docstring que cuenta la historia.
- [ ] Suite completa en verde (backend); typecheck + build en verde (frontend).
- [ ] Mocks para servicios externos; firmas de webhook reales contra secreto de test.
**Criterio de salida:** suite completa verde.
**Bloqueo duro:** un test rojo detiene todo. Sin excepciones, sin "es flaky" ([05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) §5.2).

## Fase 7 — QA

**Objetivo:** ejercitar el cambio como lo hará el usuario, no como lo pensó el autor.
**Checklist:**
- [ ] Recorrido manual del flujo afectado en entorno local (o preview) con ojos de cliente.
- [ ] Estados de error y vacío vistos de verdad, no imaginados.
- [ ] Si toca datos visibles: spot-check de calidad (¿algo raro, off-topic, mal etiquetado?).
- [ ] Si toca email: envío real de prueba y revisión en inbox (incluido spam).
**Criterio de salida:** el dueño lo usó como usuario y no encontró vergüenzas.

## Fase 8 — Revisión

**Checklist:**
- [ ] Revisión de Codex si toca área sensible (obligatoria, bloqueante) — reglas de [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) §4.
- [ ] Hallazgos de la revisión: resueltos o aceptados por escrito con motivo.
- [ ] Nadie aprueba su propio trabajo.
**Criterio de salida:** aprobación del revisor o constancia escrita de que el cambio no requería revisión obligatoria.
**Bloqueo:** un hallazgo de seguridad crítico de Codex solo lo levanta el CEO por escrito ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §2.4).

## Fase 9 — Deploy

**Checklist:**
- [ ] CI en verde en `main`.
- [ ] Migraciones: aditivas, o plan de rollback escrito y backup verificado.
- [ ] Variables de entorno nuevas: creadas en **todos** los servicios que las necesitan (backend, cron, frontend — lección del `JWT_SECRET`), antes del deploy.
- [ ] Se conoce el rollback (redeploy anterior / revert) antes de pulsar.
- [ ] Deploy con estado `SUCCESS` confirmado en todos los servicios afectados (se espera y se comprueba; no se asume).
**Criterio de salida:** servicios en `SUCCESS`.
**Bloqueo:** deploy fallido → se arregla o se revierte antes de cualquier otra cosa; `main` roto es prioridad absoluta.

## Fase 10 — Monitorización (el deploy no cierra la tarea; esta fase sí)

**Checklist inmediata (primeros 15 minutos):**
- [ ] **Verificación en producción real:** ejercitar el cambio de verdad — petición HTTP real, navegación real del flujo, consulta real a la BD de producción. Con evidencia (respuesta, captura, fila).
- [ ] Sentry: cero errores nuevos relacionados.
- [ ] Si toca webhook/billing: verificar el efecto en datos reales (p. ej., replay del evento y comprobación de la fila — patrón usado en el fix de `cancel_at`).
**Checklist diferida:**
- [ ] Si toca automatización programada: **verificar el primer disparo real** (programar la comprobación, no confiar en la configuración — regla nacida del incidente del cron).
- [ ] Si toca funnel: revisar los eventos en Plausible en las 24-48h siguientes.
**Criterio de salida:** funcionando en producción con evidencia. Ahora sí, la tarea está Done ([05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) §2).

## Fase 11 — Retrospectiva

**Para cambios normales:** una línea en el registro semanal (qué salió, qué se aprendió).
**Para incidentes o bugs encontrados en producción (obligatorio):**
- [ ] Postmortem breve sin culpables: síntoma → causa raíz → por qué el proceso no lo atrapó → qué regla/test/checklist nuevo lo previene.
- [ ] Los tres artefactos: fix + test de regresión + lección escrita en `/docs` ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §8).
- [ ] ¿El riesgo estaba en [12_RISK_REGISTER.md](12_RISK_REGISTER.md)? Si no, se añade; si sí, se recalibra su probabilidad.
- [ ] Si la lección cambia una regla: commit al documento de governance correspondiente.

---

## Resumen de bloqueos absolutos (nunca se despliega si...)

1. Un test de la suite está en rojo.
2. Falta revisión obligatoria de área sensible.
3. Hay un bloqueo de seguridad de Codex sin levantar por el CEO.
4. Una migración destructiva no tiene plan de rollback y backup verificado.
5. Una variable de entorno nueva no está en todos los servicios que la necesitan.
6. Es una acción irreversible sin aprobación explícita del CEO.
7. Nadie va a estar disponible para la fase 10 tras el deploy (no se despliega y se abandona: desplegar es comprometerse a verificar).
