# 04 — CPO Playbook

**AI Trend Hunter · Manual del Chief Product Officer**
Versión 1.0 · Julio 2026 · Propietario: CPO (ChatGPT) · Decisión final de producto: CEO

Este manual define cómo se descubre, valida, construye, mide y elimina producto. Se apoya en [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md) (qué creemos), [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) (cómo priorizamos) y [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) (cómo medimos).

---

## 1. Filosofía de producto

1. **No construimos dashboards; construimos decisiones.** El usuario no paga por ver datos: paga por saber qué oportunidad perseguir esta semana. Cada pantalla debe responder "¿y ahora qué hago?" — por eso el dashboard abre con *una* mejor oportunidad y un brief accionable, no con cuarenta gráficas.
2. **El producto es la calidad de la señal.** Un solo item basura visible (un port de un videojuego de 1998 como "oportunidad SaaS", una descripción en chino sin traducir) destruye más confianza que diez features nuevas la construyen. La calidad de datos es la feature número uno, para siempre.
3. **En fase de validación, la distribución manda sobre el producto.** El producto actual es suficiente para validar. La duda por defecto ante cualquier feature nueva: "¿esto nos acerca a 100 clientes más que gastar el mismo esfuerzo en adquisición?"
4. **Vendemos claridad, no completitud.** Menos tendencias bien filtradas > más tendencias. Menos métricas explicadas > más métricas crudas.
5. **No prometemos lo que no existe.** La landing ya nos mordió una vez prometiendo alertas y exports inexistentes; se corrigió. El copy siempre describe el producto de hoy, con "coming soon" explícito si hace falta.

---

## 2. Product-Market Fit: definición operativa

PMF no es una sensación; aquí se define con números (umbrales en [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md)):

| Señal | Pre-PMF (hoy) | Señal temprana de PMF | PMF |
|---|---|---|---|
| Suscriptores de pago | <10 | 30-100 con canal repetible | >100 y creciendo sin empujar |
| Conversión trial→pago | sin datos suficientes | >25% | >40% |
| Churn mensual | sin datos | <8% | <4% |
| Retención de uso (W1→W4) | sin datos | >30% vuelve en semana 4 | >50% |
| "¿Cómo te sentirías si no pudieras usar AI Trend Hunter?" (test de Sean Ellis) | — | >25% "muy decepcionado" | >40% |

**Regla de honestidad:** hasta tener ≥30 clientes de pago, ninguna métrica de ratio es fiable (muestras minúsculas). En esta fase la señal dominante es **cualitativa**: entrevistas y comportamiento observado de los primeros usuarios, uno a uno.

---

## 3. Validación y entrevistas

**Cadencia:** en fase de validación, el CEO habla con un mínimo de 3 usuarios/prospectos por semana. Sin excepción — es la actividad de producto de mayor valor por hora que existe a esta escala.

**Guion base (adaptar, no leer):**
1. ¿Qué intentabas conseguir cuando probaste el producto? (JTBD, no features)
2. ¿Qué haces hoy para descubrir oportunidades? ¿Qué te cuesta de eso? (alternativa real)
3. Recorre conmigo tu última sesión en el dashboard. ¿Dónde te paraste? ¿Qué ignoraste?
4. ¿Qué tendría que pasar para que pagaras 39 €/mes sin dudar? / ¿Por qué cancelaste?
5. Test de Sean Ellis (pregunta de decepción).

**Reglas de oro:** preguntar por comportamiento pasado, no por intención futura ("¿pagarías?" no vale nada; "¿por qué pagaste/cancelaste?" vale oro). Grabar o anotar en el momento. Cada entrevista deja 5 líneas de síntesis en el registro de aprendizaje, revisadas en el Consejo ([09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md)).

---

## 4. El funnel: activación, conversión, retención

### 4.1 Mapa del funnel real (instrumentado hoy)

```
Anuncio/orgánico → Landing → Pricing → Checkout Stripe (trial 7d)
    → Email código → Login → Dashboard (ACTIVACIÓN)
    → Uso recurrente durante el trial → Conversión a pago → Retención
```

Eventos ya instrumentados: `Landing Viewed`, `CTA Clicked`, `Trial Started`, `Login`, `Dashboard Viewed`, `Trend Viewed`, `Opportunity Viewed`, `Trial Converted`, `Trial Expired` (Plausible + CAPI). No se construye instrumentación nueva hasta explotar la existente.

### 4.2 Activación
**Definición:** un usuario está activado cuando, en su primera sesión, ve el hero de "Best opportunity this week" **y** abre al menos un brief de oportunidad (`Opportunity Viewed`). Es el momento WOW diseñado: "esto sabe algo que yo no sé".

Palancas de activación en orden: (1) el primer email de código llega rápido y a inbox — por eso el dominio de email propio es prioridad ([03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md), deuda técnica), (2) el dashboard carga con datos frescos del día, (3) la mejor oportunidad del día es genuinamente interesante (calidad de señal).

### 4.3 Conversión (trial → pago)
El trial es de 7 días: el usuario debe experimentar el ciclo de valor **dos veces** (los datos se renuevan a diario; una semana = 7 renovaciones). Palancas: recordatorio de valor durante el trial (pendiente: email de día 3 con "lo que encontramos esta semana"), fricción cero en el portal de billing (ya operativo), y claridad de precio.

### 4.4 Retención
El ciclo natural de uso es **semanal** ("¿qué oportunidad hay esta semana?"). La métrica de retención se mide en semanas, no en días — un producto de decisión semanal con DAU bajo no está roto, está siendo lo que es. Palanca futura más prometedora (hipótesis, no compromiso): resumen semanal por email que devuelva al usuario al dashboard. Se construirá **cuando los datos muestren** que los usuarios activados dejan de volver — no antes ("no construir el email de retención antes de tener el problema de retención", decisión ya registrada en `docs/PMF_SPRINT_REPORT.md`).

### 4.5 WOW
El WOW de este producto es específico: **"me ha enseñado una oportunidad concreta que no conocía, con un plan de acción"**. Todo el diseño del dashboard sirve a ese momento (hero → scores → brief → señales fuente). Cualquier propuesta de diseño se evalúa contra: ¿acorta o alarga el camino al WOW?

---

## 5. JTBD — Jobs to be Done

**Job principal:** *"Cuando estoy decidiendo qué construir/lanzar a continuación, quiero descubrir oportunidades emergentes antes de que sean obvias, para no gastar meses en un mercado saturado o inexistente."*

**Contratado contra las alternativas reales:** doomscrollear HN/Twitter (gratis, ruidoso, sin memoria), newsletters de tendencias (genéricas, tarde), investigación manual (cara en tiempo). Nuestro diferencial: señal filtrada + scoring + brief accionable + diario.

**Jobs secundarios detectados (aún sin explotar):** justificar una decisión ante socios/inversores ("no lo digo yo, lo dicen las señales"); vigilar un nicho concreto (aún sin feature de watchlist — no prometida, no construida).

---

## 6. Hipótesis, experimentos y A/B testing

### 6.1 Formato de hipótesis (obligatorio antes de construir nada)
```
Creemos que [cambio] producirá [efecto en métrica X de Y a Z]
porque [razón basada en evidencia].
Lo mediremos con [evento/métrica] durante [plazo].
Éxito si [umbral]. Si no: [matar / iterar / entender].
```

### 6.2 Qué método usar según el volumen
- **<100 clientes (hoy): nada de A/B tests.** Con decenas de usuarios, un A/B test es teatro estadístico. Se usan: entrevistas, observación de sesiones (Plausible), y **apuestas secuenciales** (cambiar, medir antes/después durante 2-4 semanas contra umbral predefinido, aceptando el ruido).
- **100-1.000:** A/B solo en el funnel de mayor tráfico (landing→pricing), con cambios grandes (no colores de botón: propuestas de valor, precios, estructura). Duración mínima: 2 semanas o significancia, lo que llegue después.
- **>1.000:** A/B testing sistemático con proceso formal.

**Regla anti-autoengaño:** el umbral de éxito se escribe antes de lanzar. Mover el poste después de chutar invalida el experimento — se registra como "no concluyente", nunca como éxito.

---

## 7. Métricas de producto

Definidas con fórmula, dueño y umbral en [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md). Las cinco que el CPO mira cada semana: activación de nuevos trials, conversión trial→pago, retención semanal de pagos, churn mensual, y la North Star (suscriptores de pago activos). Todo lo demás es diagnóstico, no dirección.

---

## 8. Frameworks de priorización: cuál y cuándo

- **RICE** (Reach × Impact × Confidence / Effort): para comparar iniciativas de producto entre sí en la planificación trimestral. Es el framework por defecto de esta empresa porque castiga el esfuerzo y premia el alcance — exactamente el sesgo correcto en fase de validación con recursos mínimos.
- **ICE** (Impact × Confidence × Ease): versión rápida para triaje semanal de ideas pequeñas (<1 día). No requiere estimar alcance; suficiente para ordenar la cola corta.
- **MoSCoW** (Must/Should/Could/Won't): solo para acotar el alcance *dentro* de una iniciativa ya decidida ("para lanzar el formulario de soporte, Must: endpoint + página; Won't: adjuntos"). Nunca para decidir entre iniciativas — no compara.
- Las preguntas cualitativas de filtro previo (¿aumenta ingresos? ¿reduce churn? ¿qué pasa si nunca se hace?) están en [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) y se aplican **antes** de puntuar: la mayoría de las ideas deben morir en el filtro, no en la puntuación.

---

## 9. Cómo detectar funcionalidades inútiles

Auditoría trimestral de features contra datos de uso (Plausible). Señales de inutilidad:

1. **Uso <5% de usuarios activos** durante un trimestre completo.
2. **No participa en ningún camino hacia el WOW** (sección 4.5) ni hacia conversión/retención.
3. **Nadie la menciona en entrevistas** ni al preguntar "¿qué echarías de menos?".
4. **Genera soporte o bugs desproporcionados** a su uso.
5. **Existe porque "ya estaba hecha"**, no porque alguien la eligiera hoy (test del coste hundido: ¿la construiríamos hoy? — misma regla que en [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md), sección 12).

Una feature con 2+ señales entra en la lista de eliminación candidata del siguiente Consejo.

---

## 10. Cómo eliminar funcionalidades

Eliminar es una feature: reduce superficie de bug, de mantenimiento y de confusión. Proceso:

1. **Medir impacto real:** ¿quién la usa? (datos, no memoria). Si la usan clientes de pago identificables, hablar con ellos antes.
2. **Decisión en Consejo** con puntuación estándar: el "impacto" de eliminar es mantenimiento evitado + claridad ganada; el "coste" es el valor perdido por los usuarios reales (no imaginados).
3. **Eliminación reversible primero:** ocultar/desactivar (soft) 2-4 semanas antes de borrar código. Si nadie protesta, se borra de verdad — el código muerto no se comenta: se elimina (está en git si hiciera falta).
4. **Comunicación:** si la usaba alguien de pago, aviso previo con alternativa. Si no la usaba nadie, no se anuncia (anunciar eliminaciones de features que nadie usaba solo genera ansiedad).
5. **Registrar la lección:** ¿por qué se construyó algo que hubo que eliminar? Esa respuesta mejora el filtro de entrada ([07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md)) — el objetivo a largo plazo es eliminar menos porque se construye mejor.

---

## 11. Diseño de experiencias: reglas de la casa

1. **Una pantalla, una decisión.** El dashboard decide por jerarquía: primero la mejor oportunidad, luego el top-5 por ángulo, luego la exploración. Nunca paridad visual entre lo importante y lo secundario.
2. **Los números siempre con contexto.** "2.6K stars · 14 open issues" y no "2.6K upvotes" — la etiqueta correcta según la fuente (lección real: una etiqueta incorrecta hace dudar de todos los datos).
3. **Sin datos sintéticos disfrazados de reales.** Si un número es una estimación (el "engagement" de RSS), o se etiqueta como tal o no se muestra. Se optó por no mostrarlo.
4. **Errores en lenguaje de cliente:** qué pasó, qué hacer, cómo contactar. Jamás trazas, jamás "revisa que el backend esté en localhost".
5. **La terminología interna no se filtra a la UI** (lección: "mvp heuristic detector" visible en el panel de runs). Nombres internos ≠ nombres de cliente.
6. **Copy en inglés para el producto, es el mercado objetivo; consistencia total** entre landing, dashboard y emails.
