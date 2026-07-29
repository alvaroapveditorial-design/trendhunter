# 07 — Decision Framework

**AI Trend Hunter · Sistema oficial para tomar decisiones**
Versión 1.0 · Julio 2026 · Propietario: CEO · Usado por: todo el equipo

Este documento define cómo se filtran, puntúan y deciden las iniciativas, y quién decide qué. Es el motor de priorización que alimenta la cola semanal de [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §4 y el orden del día del Consejo ([09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md)).

---

## 1. Clasificación previa: ¿qué tipo de decisión es?

Antes de puntuar nada, clasificar:

**Tipo 1 — Irreversible o cara de revertir.** Dinero real, datos de clientes, precio, marca, compromisos externos, arquitectura fundamental. → Decide el CEO, con input escrito del CTO (y de Codex si es técnica). Mínimo una noche entre propuesta y decisión, salvo incidente activo. Se registra siempre (sección 5).

**Tipo 2 — Reversible.** Casi todo lo demás: código con rollback, copy, experimentos, scripts reversibles. → Decide el nivel más bajo con autoridad ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §2), ejecuta, y comunica después. La velocidad en Tipo 2 es una ventaja competitiva; la prudencia en Tipo 1 es supervivencia.

**Regla de ambigüedad:** si no está claro de qué tipo es, es Tipo 1.

---

## 2. El filtro: doce preguntas antes de puntuar

La mayoría de las ideas deben morir aquí, barato. Toda iniciativa candidata responde por escrito (una línea por pregunta; "no sé" es respuesta válida y reveladora):

1. **¿Aumenta ingresos?** ¿Cómo exactamente — más trials, mejor conversión, menos churn, precio?
2. **¿Aumenta retención?** ¿Qué comportamiento semanal refuerza?
3. **¿Reduce churn?** ¿Ataca una causa de cancelación conocida (de entrevistas/datos) o imaginada?
4. **¿Genera WOW?** ¿Acorta el camino a "esto sabe algo que yo no sé"? ([04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §4.5)
5. **¿Reduce complejidad?** ¿O añade superficie de mantenimiento, bug y confusión?
6. **¿Escala?** ¿Funciona igual con 10× clientes? ¿Introduce coste variable por cliente? (si sí → Consejo, [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md) §7)
7. **¿Puede medirse?** ¿Qué evento/métrica concreta de [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) lo capturará?
8. **¿Tiene hipótesis?** Formulada con la plantilla de [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §6.1, con umbral de éxito escrito **antes**.
9. **¿Tiene KPI y dueño?** Un número y un nombre. Sin ambos, no entra en cola.
10. **¿Qué coste de oportunidad tiene?** ¿Qué NO haremos esta semana por hacer esto? (nombrarlo explícitamente)
11. **¿Qué pasa si esperamos 90 días?** Si la respuesta honesta es "nada grave", pierde toda urgencia artificial y compite en frío.
12. **¿Qué pasa si no se hace nunca?** Si la respuesta es "nada", la decisión ya está tomada: no se hace. Esta pregunta mata más iniciativas que ninguna otra, y ese es su trabajo.

**Criterio de paso:** para avanzar a puntuación, la iniciativa necesita al menos un "sí" fuerte en las preguntas 1-4 (impacto) y ninguna respuesta descalificante en 5-6 (complejidad/escala sin justificar). Las respuestas se archivan con la iniciativa: en la retrospectiva se comparan con lo que realmente pasó, y así se calibra el olfato del equipo.

---

## 3. La puntuación: RICE adaptado

Para lo que sobrevive al filtro. Fórmula:

```
Puntuación = (Reach × Impact × Confidence) / Effort
```

**Reach (alcance, por trimestre):** ¿a cuántos usuarios/prospectos toca?
- A esta escala se usa una escala ordinal honesta, no falsa precisión: 1 = un puñado de usuarios · 3 = una fracción significativa de los activos · 10 = todos los usuarios o todo el tráfico del funnel.

**Impact (impacto por usuario alcanzado):** 0.25 = mínimo · 0.5 = bajo · 1 = medio · 2 = alto · 3 = masivo (cambia la decisión de pagar/quedarse).

**Confidence (confianza):** 100% = hay datos propios o es mecánico · 80% = evidencia parcial (entrevistas, patrones del sector) · 50% = intuición fundada · <50% = es una apuesta; se dice sin vergüenza y puntúa como tal.

**Effort (esfuerzo):** en días-persona totales (incluye diseño, tests, verificación y el coste del proceso de release). Mínimo 0.5.

**Modificadores posteriores a la puntuación (no numéricos, se aplican como veto o empujón):**
- Viola un principio de [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md) → veto salvo decisión CEO.
- Mitiga un riesgo alto del [12_RISK_REGISTER.md](12_RISK_REGISTER.md) → sube posiciones.
- Es prelación 1-2 del sistema operativo (incidente/seguridad) → salta la cola directamente.

**Ejemplo real de calibración** (para futuros miembros): "formulario de soporte antes del lanzamiento" → Reach 10 (todo cliente puede necesitarlo), Impact 1 (medio: no convierte, pero su ausencia mata confianza), Confidence 100%, Effort 0.5 días → puntuación 20, y además mitigaba un gap del checklist de lanzamiento → se hizo esa misma semana. "Email semanal de retención" → Reach 3, Impact 2, Confidence 50% (aún sin datos de que la retención sea el problema), Effort 3 → 1.0 → a la nevera hasta tener datos de retención reales (decisión registrada en `docs/PMF_SPRINT_REPORT.md`).

---

## 4. Reglas de decisión complementarias

- **Empates:** gana la de menor Effort (lo barato enseña más rápido). Si persiste, decide el principio de producto aplicable; si no hay, el CEO.
- **Lo urgente contra lo importante:** solo las prelaciones 1-2 ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §4.3) pueden desplazar la cola. Todo lo demás espera al lunes. La sensación de urgencia no es un argumento; es una emoción.
- **Decisiones en caliente:** prohibidas para Tipo 1. La regla de la noche: ninguna decisión irreversible se toma el mismo día en que se propuso, salvo incidente activo con clientes afectados.
- **Quién puede decir no:** cualquiera puede argumentar contra cualquier iniciativa con datos o principios. Solo el CEO puede decir el "no" final a algo que puntúa alto, y lo registra.

---

## 5. Registro de decisiones (Tipo 1)

Toda decisión Tipo 1 queda registrada en el acta del Consejo con este formato mínimo:

```
DECISIÓN #YYYY-NN
Fecha:
Contexto: (3 líneas máx.)
Opciones consideradas: A (coste/beneficio), B (coste/beneficio), no hacer nada
Decisión: 
Decide: CEO | Input: CTO / Codex / CPO
Métrica de validación + fecha de revisión:
Desacuerdos registrados: (quién y por qué — para la retro, no para el reproche)
```

- Una decisión registrada **no se relitiga** sin datos nuevos ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §6).
- En la fecha de revisión, el Consejo responde: ¿acertamos? Las decisiones erradas con proceso correcto no se penalizan; las acertadas con proceso saltado, sí — el proceso es lo único que escala.

---

## 6. Anti-patrones que este sistema prohíbe explícitamente

1. **La feature del último cliente ruidoso:** un solo dato anecdótico no mueve la cola; se anota, se acumula, y con 3+ menciones independientes entra al filtro.
2. **El "ya que estamos":** ampliar el alcance de una iniciativa en marcha sin repasar por el filtro. El scope creep se decide, no se desliza.
3. **La urgencia fabricada:** "hay que hacerlo ya" sin incidente ni fecha externa real. Pregunta 11 del filtro.
4. **El teatro de datos:** justificar con métricas de muestra insuficiente ([11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md), sección de interpretación). Con n<30, la palabra honesta es "apuesta", y las apuestas se declaran como tales (Confidence <50%).
5. **La decisión por agotamiento:** decidir algo grande al final de una sesión larga. Tipo 1 siempre descansa una noche.
