# 02 — Operating System

**AI Trend Hunter · Manual operativo de la empresa**
Versión 1.0 · Julio 2026 · Propietario: CEO · Este es el documento raíz del sistema: todos los demás cuelgan de él.

Este documento define **cómo funciona la empresa**: cómo se trabaja, cómo se prioriza, cómo se decide, cómo se corrige el rumbo y cómo se cancela lo que no funciona. Si un documento de `/governance` contradice a este, gana este hasta que el Consejo resuelva la contradicción.

---

## 1. Principios de funcionamiento

1. **La prioridad es construir una empresa, no más software.** La infraestructura existe y está desplegada. Cada semana que se dedica a features en vez de a clientes es una semana de validación perdida. Fase actual: validación comercial, objetivo 100 clientes de pago.
2. **Producción es la única verdad.** Nada está "hecho" hasta que se ha verificado funcionando en producción con datos reales. Este principio nació de experiencia propia: un cron que "estaba configurado" llevó días caído en silencio porque nadie verificó el primer disparo real. No se repite.
3. **Evidencia sobre opinión.** Toda afirmación relevante ("el checkout funciona", "los usuarios quieren X") debe llevar su evidencia al lado: un dato, un test, una captura, una consulta a la base de datos. Quien afirma, prueba.
4. **Reversibilidad por defecto.** Las decisiones reversibles se toman rápido y en el nivel más bajo posible. Las irreversibles (dinero, datos, clientes, marca) suben al CEO siempre. Clasificación completa en [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md).
5. **Pocas cosas, terminadas.** Es preferible cerrar una iniciativa por semana de verdad (desplegada, verificada, medida) que avanzar cinco a medias. El work-in-progress es inventario, y el inventario es coste.
6. **El coste marginal casi nulo es una ventaja estratégica, no un accidente.** El motor es heurístico, sin LLM en el camino crítico. Cualquier propuesta que introduzca coste variable por cliente necesita justificación extraordinaria ante el Consejo.
7. **Los errores se documentan, no se entierran.** Cada bug relevante encontrado en producción genera: (a) fix, (b) test de regresión, (c) entrada en el informe correspondiente en `/docs`. La memoria institucional es un activo.

---

## 2. Sistema de trabajo

### 2.1 Cadencia

| Ritmo | Qué ocurre | Referencia |
|---|---|---|
| Diario | Ejecución. El cron de ingesta corre a las 08:00 UTC; se revisa Sentry y el estado del pipeline si hay alerta. | [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md), checklist diaria |
| Semanal | Consejo de Dirección: métricas, riesgos, decisiones, priorización de la semana. | [09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md) |
| Mensual | Retrospectiva + revisión de métricas de tendencia + revisión del registro de riesgos. | [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md), [12_RISK_REGISTER.md](12_RISK_REGISTER.md) |
| Trimestral | Revisión de estrategia, OKRs, organigrama y de este propio sistema operativo. | [01_COMPANY_CHART.md](01_COMPANY_CHART.md), [10_NORTH_STAR.md](10_NORTH_STAR.md) |

### 2.2 Unidad de trabajo

La unidad de trabajo es la **iniciativa**: algo que cabe en una semana, tiene una hipótesis, un resultado verificable y un dueño. No hay "proyectos" abiertos sin fecha. Si algo no cabe en una semana, se trocea hasta que quepa; si no se puede trocear, probablemente no está entendido y vuelve a descubrimiento.

Toda iniciativa se formula así antes de empezar:

```
INICIATIVA: <nombre>
HIPÓTESIS: creemos que <acción> producirá <resultado medible> porque <razón>
MÉTRICA: <qué número se mueve y cuánto> (de 11_METRICS_PLAYBOOK)
DUEÑO: <un solo nombre>
COSTE: <horas + dinero>
REVERSIBLE: sí/no → si no, aprobación CEO previa
CADUCIDAD: <fecha en la que se evalúa y se decide continuar/matar>
```

### 2.3 Flujo de ejecución técnica

Definido en detalle en [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md). Resumen: idea → descubrimiento → diseño → desarrollo con tests → revisión (Codex) → deploy → **verificación en producción real** → retro. Ningún paso se salta, ni siquiera para "cambios de una línea": la historia de la empresa incluye un cambio de una línea de configuración que tumbó el pipeline de datos.

---

## 3. Sistema de reuniones

Con un equipo de 1 humano + 3 agentes, las "reuniones" son sesiones de trabajo estructuradas, no calendario. Reglas:

1. **Una sola reunión obligatoria:** el Consejo Semanal ([09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md)). Todo lo demás es trabajo.
2. **Toda sesión de trabajo con decisiones termina en un registro escrito** (acta, commit, o documento en `/docs`). Lo que no está escrito no se decidió.
3. **Prohibidas las reuniones de estado.** El estado se lee en las métricas y en el repositorio, no se narra.
4. Cuando haya empleados humanos: máximo 2 reuniones recurrentes por persona y semana; toda reunión tiene orden del día previo o no se celebra.

---

## 4. Sistema de priorización

1. Todo lo priorizable pasa por la puntuación de [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) (impacto en ingresos/retención/WOW vs. coste y riesgo).
2. La cola de trabajo semanal tiene **máximo 3 iniciativas**. La cuarta espera. Si entra algo urgente, algo sale — se dice explícitamente qué.
3. Orden de prelación permanente cuando hay conflicto:
   1. Incidentes que afectan a clientes de pago (caída, datos erróneos visibles, cobros incorrectos).
   2. Seguridad ([12_RISK_REGISTER.md](12_RISK_REGISTER.md), riesgos SEC-*).
   3. Todo lo que acerque a los primeros 100 clientes (adquisición, activación, conversión).
   4. Calidad de datos del producto (las señales son el producto).
   5. Deuda técnica con dolor medido.
   6. Todo lo demás.
4. **Regla de los 90 días:** ante cualquier propuesta, preguntarse "¿qué pasa si esperamos 90 días?". Si la respuesta es "nada grave", la propuesta compite en la cola normal, sin urgencia artificial.

---

## 5. Gestión de riesgos

- El registro vivo está en [12_RISK_REGISTER.md](12_RISK_REGISTER.md). Se revisa mensualmente en Consejo.
- Cualquier miembro puede añadir un riesgo en cualquier momento; nadie necesita permiso para señalar un peligro.
- Un riesgo con probabilidad alta e impacto alto genera automáticamente una iniciativa de mitigación en la cola (entra en prelación 2).
- Los incidentes reales alimentan el registro: cada postmortem revisa si el riesgo estaba registrado, y si no, por qué.

---

## 6. Gestión de conflictos

1. Los conflictos entre roles se resuelven primero con datos: cada parte trae evidencia, no adjetivos.
2. Si los datos no bastan (conflicto de valores o de apuesta), se aplica la tabla de desempate de [01_COMPANY_CHART.md](01_COMPANY_CHART.md), sección 3.
3. Formato obligatorio de escalado: contexto en 3 líneas, opciones con coste, recomendación de cada parte. El CEO decide, el acta lo registra, y la decisión no se relitiga sin datos nuevos.
4. **Desacuerdo y compromiso** (disagree and commit): una vez decidido, todos ejecutan como si la decisión fuera suya. El acta preserva el desacuerdo para la retrospectiva, no para el reproche.

---

## 7. Roadmap y objetivos

### 7.1 Creación del roadmap
- El roadmap es **trimestral, temático y corto**: máximo 3 temas por trimestre (ej.: "conversión del trial", "calidad de señales", "canal de adquisición repetible").
- Lo propone el CPO/CTO (ChatGPT) a partir de: métricas ([11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md)), feedback de clientes ([04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md)) y riesgos. Lo aprueba el CEO.
- El roadmap no es una lista de features: es una lista de **resultados** ("subir activación del 40% al 55%"), y las features son hipótesis para lograrlos.

### 7.2 Definición de objetivos
- OKRs trimestrales: 1 objetivo, máximo 3 resultados clave, todos numéricos, todos trazables a una métrica del playbook.
- El OKR del trimestre actual (fase de validación): **conseguir los primeros clientes de pago con un canal repetible**, medido por suscriptores activos de pago, conversión trial→pago y CAC.

### 7.3 Seguimiento
- Semanal en Consejo: cada resultado clave con su número actual, su tendencia y un semáforo honesto (verde/ámbar/rojo). Prohibido el "verde diplomático".
- Un resultado clave en rojo dos semanas seguidas obliga a una decisión explícita: reforzar, reformular o abandonar.

### 7.4 Retrospectivas
Mensual, 30 minutos, formato fijo: (1) qué movió métricas y por qué, (2) qué no y por qué, (3) qué error operativo cometimos y qué regla nueva lo previene, (4) qué regla existente sobra. Las reglas nuevas se incorporan al documento de governance correspondiente — así es como este sistema mejora.

---

## 8. Sistema de mejora continua

- **Cada bug de producción deja tres artefactos:** fix + test de regresión + lección escrita. Ya es práctica real del equipo (ver `docs/PRE_LAUNCH_QA_REPORT.md`) y se eleva aquí a norma.
- **Cada fricción operativa repetida dos veces se automatiza o se documenta** (script en `backend/scripts/`, entrada en playbook, o checklist nueva).
- **Los documentos de governance son código:** viven en el repo, se cambian por commit, y su historial es auditable. Un documento que lleva dos trimestres sin tocarse y sin usarse se archiva — la documentación muerta es peor que la ausente.

---

## 9. Metodología para tomar decisiones

Definida en [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md). Resumen operativo:

- **Tipo 1 (irreversibles / caras):** dinero, datos de clientes, precio, marca, arquitectura fundamental. Decide el CEO con input escrito de CTO y, si es técnico, de Codex. Nunca en caliente: mínimo una noche entre propuesta y decisión, salvo incidente activo.
- **Tipo 2 (reversibles):** se deciden en el nivel más bajo con autoridad ([01_COMPANY_CHART.md](01_COMPANY_CHART.md), sección 2) y se comunican después. Pedir perdón, no permiso — pero dejar rastro.
- Toda decisión Tipo 1 se registra: fecha, contexto, opciones consideradas, decisión, quién, y fecha de revisión.

---

## 10. Metodología para cambiar de estrategia

Un cambio de estrategia (pivote de segmento, de precio, de propuesta de valor) exige las cuatro condiciones:

1. **Evidencia acumulada, no anécdota:** mínimo 4 semanas de datos o 15 conversaciones con clientes apuntando en la misma dirección.
2. **La estrategia actual tuvo una oportunidad real:** se ejecutó lo planeado (no se está pivotando para huir de la ejecución pendiente).
3. **Hipótesis nueva formulada por escrito** con la misma plantilla de iniciativa (sección 2.2), antes de abandonar la anterior.
4. **Decisión del CEO en Consejo, registrada**, con fecha de evaluación del pivote (máximo 90 días).

Lo que no exige: permiso de nadie externo, consenso unánime, ni certeza. Exige honestidad sobre por qué se cambia.

---

## 11. Metodología para validar hipótesis

Detallada en [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md), secciones de experimentos. Principios no negociables:

1. Toda hipótesis se escribe **antes** de mirar los datos que la validarían.
2. Se define el umbral de éxito antes de lanzar ("si la conversión no llega al X% en N semanas, la hipótesis es falsa").
3. Con el volumen actual (decenas de usuarios), los A/B tests formales son matemáticamente inviables: se usan **apuestas secuenciales** (antes/después con umbral) y señal cualitativa (entrevistas). No fingimos rigor estadístico que el tamaño de muestra no permite — ver [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md), sección de interpretación.
4. Una hipótesis falsada es un éxito del sistema, no un fracaso del proponente. Se celebra el aprendizaje barato.

---

## 12. Metodología para cancelar proyectos

Los proyectos no mueren solos; hay que matarlos. Sistema:

1. **Toda iniciativa nace con fecha de caducidad** (campo obligatorio de la plantilla). En esa fecha se decide: continuar (con nueva fecha), matar, o congelar con condición de reapertura explícita.
2. **Criterios de cancelación automática** (cualquiera basta para forzar la conversación):
   - La métrica objetivo no se movió en el plazo definido.
   - El coste real superó el doble del estimado.
   - La razón original de la iniciativa ya no existe.
   - Su dueño no puede dedicarle tiempo esta semana ni la siguiente.
3. **El coste hundido no vota.** La única pregunta válida es: "sabiendo lo que sabemos hoy, ¿empezaríamos esto?". Si la respuesta es no, se cancela hoy.
4. Cancelar deja rastro: 5 líneas en el acta con lo aprendido. Lo cancelado con aprendizaje documentado fue barato; lo cancelado en silencio se repetirá.
5. Esto aplica también a **funcionalidades ya construidas**: el proceso para eliminarlas está en [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md), sección "cómo eliminar funcionalidades".

---

## 13. Qué hace que este sistema funcione

Este sistema está diseñado para una empresa de 4 miembros que quiere llegar a 50 sin colapsar. Tres advertencias a los futuros miembros del equipo:

- **El sistema es mínimo a propósito.** Cada proceso aquí existe porque su ausencia ya costó algo real. No añadas proceso preventivo; añade proceso cicatrizal.
- **El sistema se aplica también cuando estorba.** Especialmente cuando estorba: la tentación de saltarse el proceso siempre llega disfrazada de urgencia.
- **El sistema se cambia por escrito, no por erosión.** Si una regla es mala, se cambia en Consejo y por commit. Incumplirla en silencio pudre todas las demás.
