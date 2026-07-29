# 11 — Metrics Playbook

**AI Trend Hunter · Manual oficial de métricas**
Versión 1.0 · Julio 2026 · Propietario: CPO (definición) + Lead Engineer (instrumentación) · Consumidor principal: Consejo Semanal ([09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md))

Fuentes de datos: Postgres (suscripciones, trends, `agent_executions`), Stripe (facturación), Plausible (comportamiento), Sentry (errores), Meta Ads Manager (adquisición). Regla general: **cada métrica tiene una sola fuente de verdad declarada**; si dos fuentes discrepan, gana la declarada y se investiga la otra.

---

## 1. North Star Metric

**Suscriptores de pago activos** (estado `active` + `trialing` con método de pago válido, fuente: tabla `subscriptions` contrastada con Stripe).

**Por qué esta:** integra todo lo que importa — adquisición (llegaron), activación (vieron valor), conversión (pagaron) y retención (siguen). Es difícil de inflar y fácil de auditar. Una métrica de uso (sesiones, page views) premiaría el ruido; esta premia el valor cobrado.

- **Frecuencia:** semanal en Consejo. **Responsable:** CEO.
- **Objetivo próximo:** 100. **Alerta:** dos semanas consecutivas sin crecer con gasto de adquisición activo → revisión del funnel completo en Consejo.

---

## 2. Métricas por área

Formato de cada métrica: definición · fórmula · frecuencia · responsable · objetivo · umbral de alerta · acción si empeora.

### 2.1 Crecimiento y negocio

| Métrica | Definición / fórmula | Frec. | Resp. | Objetivo | Alerta | Acción si empeora |
|---|---|---|---|---|---|---|
| MRR | Σ suscripciones activas × 39 € (fuente: Stripe) | Semanal | CEO | Crecimiento sostenido | Caída 2 sem. seguidas | Descomponer: ¿churn o adquisición? |
| Trials iniciados | `Trial Started` (webhook, fuente BD) /semana | Semanal | CEO | Según gasto de ads | 0 con ads activos | Auditar funnel técnico completo (fase 10 de [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md)) |
| Conversión trial→pago | pagos reales / trials que terminaron ese periodo | Semanal (fiable con n≥30 acumulado) | CPO | >25% temprano, >40% PMF | <15% con n≥20 | Entrevistas a no-convertidos; revisar activación |
| Churn mensual | cancelaciones del mes / activos al inicio del mes | Mensual | CEO | <5% | >8% | Entrevista de salida a cada cancelación, sin excepción |
| CAC | gasto en ads del periodo / clientes de pago nuevos atribuidos | Mensual | CEO | < 3 meses de margen (~100 €) | CAC > 6 meses de margen | Pausar escalado de gasto; iterar creatividades/segmento |
| Payback | CAC / margen mensual por cliente (~37 €) | Mensual | CEO | <3 meses | >6 meses | Igual que CAC |

### 2.2 Producto (funnel y uso)

| Métrica | Definición / fórmula | Frec. | Resp. | Objetivo | Alerta | Acción |
|---|---|---|---|---|---|---|
| Visitas landing | Plausible, visitantes únicos /semana | Semanal | CPO | Según canal | Caída >50% sin cambio de gasto | Verificar tracking antes que narrativa |
| Landing → pricing | `CTA Clicked` con destino pricing / visitas | Semanal | CPO | >10% | <5% | Revisar propuesta de valor above-the-fold |
| Pricing → checkout | checkouts creados / visitas a pricing | Semanal | CPO | >20% | <10% | Revisar precio/fricción del form |
| Activación | usuarios nuevos con `Dashboard Viewed` + `Opportunity Viewed` en primera sesión / logins nuevos | Semanal | CPO | >60% | <40% | Revisar entrega de email de código y frescura de datos ([04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §4.2) |
| Retención semanal | pagantes con ≥1 sesión en la semana / pagantes totales | Semanal | CPO | >50% | <30% | Entrevistas; considerar (recién entonces) el email semanal |
| Test Sean Ellis | % "muy decepcionado" (encuesta a activos, n≥20) | Trimestral | CPO | >40% | <25% | Reposicionar o pivotar segmento ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §10) |

### 2.3 Calidad del producto (la señal)

| Métrica | Definición / fórmula | Frec. | Resp. | Objetivo | Alerta | Acción |
|---|---|---|---|---|---|---|
| Frescura de datos | máx(`last_updated_at`) de trends activos vs. ahora | Diaria (automatizable) | Lead Eng. | <24h | >30h | Incidente: diagnóstico del pipeline (runbook [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §8.1) |
| Éxito del cron | filas `agent_executions` success en ventana 08:00-08:15 UTC | Diaria | Lead Eng. | 7/7 días | 1 fallo | Mismo runbook; postmortem si se repite |
| Basura visible | items off-topic/no-inglés detectados en spot-check semanal del dashboard | Semanal | Lead Eng. | 0 | ≥1 | Fix + ampliar filtro + test de regresión (patrón establecido) |
| Trends activos | count(is_active) | Semanal | CPO | Estable/creciente | Caída >30% en una semana | ¿Limpieza agresiva o fuente caída? Investigar antes de tocar filtros |

### 2.4 Ingeniería

| Métrica | Definición / fórmula | Frec. | Resp. | Objetivo | Alerta | Acción |
|---|---|---|---|---|---|---|
| Errores Sentry nuevos | issues nuevos /semana | Semanal | Lead Eng. | 0 sin triaje | Cualquiera sin causa asignada en 48h | Triaje obligatorio en checklist semanal |
| Suite de tests | nº tests y estado (hoy: 81, verde) | Cada deploy | Lead Eng. | Verde siempre; nº creciente | Rojo | Bloqueo total de deploys ([05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) §5.2) |
| Incidentes con impacto en cliente | count /mes + minutos de impacto | Mensual | Lead Eng. | 0 | ≥1 | Postmortem con los 3 artefactos |
| Regresiones repetidas | bugs que reaparecen tras fix | Mensual | Codex | 0 | ≥1 | El test de regresión falló en su misión: revisar el patrón de test |
| TTFB dominio | curl al dominio público | Mensual | Lead Eng. | <1s | >2s | Diagnóstico de plataforma |

### 2.5 Soporte

| Métrica | Definición | Frec. | Resp. | Objetivo | Alerta | Acción |
|---|---|---|---|---|---|---|
| Mensajes de soporte | recibidos vía `/contact` + email /semana | Semanal | CEO | — (es señal, no target) | Tema repetido ≥3 veces | Candidato automático al filtro de decisión |
| Tiempo de respuesta | mediana hasta primera respuesta | Semanal | CEO | <24h | >48h | Adelantar contratación de soporte ([01_COMPANY_CHART.md](01_COMPANY_CHART.md), Fase 1) |

### 2.6 Infraestructura y finanzas operativas

| Métrica | Definición | Frec. | Resp. | Objetivo | Alerta | Acción |
|---|---|---|---|---|---|---|
| Coste infra total | Railway + Resend + dominios + herramientas /mes | Mensual | CEO | ~50-100 € | >150 € sin causa | Revisar consumo por servicio |
| Coste marginal por cliente | Δcoste infra / Δclientes | Trimestral | CTO | ~0 € | Coste variable detectado | Consejo: viola el principio §7 de [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md) |
| Webhooks Stripe fallidos | pendientes de reintento en Stripe | Semanal | Lead Eng. | 0 | ≥1 sin resolver | Investigar antes del siguiente ciclo de reintento |

---

## 3. Cómo interpretar métricas (obligatorio leer antes de decidir con ellas)

1. **La muestra manda.** Con n<30, los porcentajes son ruido con disfraz. "2 de 5 trials convirtieron" no es "40% de conversión": es *dos personas*. En fase actual, la mayoría de ratios de este playbook se reportan como fracciones crudas ("3/11"), no como porcentajes, hasta acumular n≥30. La señal cualitativa (entrevistas) domina hasta entonces.
2. **Tendencia sobre foto.** Una semana mala no es información; tres semanas descendentes sí. Las alertas de las tablas se disparan por sostenimiento, no por un punto.
3. **Descomponer antes de reaccionar.** "Bajó el MRR" no es accionable; "subió el churn de la cohorte de julio captada por ads" sí. Toda métrica agregada que empeora se descompone (por cohorte, por canal, por semana) antes de decidir nada.
4. **Instrumentación antes que narrativa.** Cuando un número se mueve raro, la primera hipótesis es siempre "se rompió la medición" (ya ocurrió: eventos duplicados por redelivery de webhooks — corregido con idempotencia). Verificar el tracking, luego interpretar.
5. **Las métricas de este documento son las únicas oficiales.** Si en una discusión aparece una métrica que no está aquí, o se añade formalmente (con definición, fórmula y dueño) o no se usa para decidir.
6. **Goodhart vigilado:** cuando una métrica se convierte en objetivo con presión, alguien la deformará sin querer. Antídotos: métricas emparejadas (conversión ↔ churn: subir la primera bajando la calidad del trial infla la segunda), y auditoría trimestral de definiciones.
7. **Prohibido el picking de ventanas.** El periodo de comparación se fija antes de mirar el dato (semana natural, mes natural). Elegir la ventana que hace bonito el número es mentirse con estilo.

---

## 4. Mantenimiento del playbook

- Revisión trimestral: métricas que nadie miró en 90 días se eliminan (una métrica sin lector es coste sin retorno).
- Todo cambio de definición o fórmula se hace por commit con explicación — las series históricas anotan el cambio para no comparar peras con manzanas.
- La automatización del reporte (script que componga la tabla del Consejo desde BD/Stripe/Plausible) es deuda deseable: se prioriza con el resto en [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) cuando el coste manual duela.
