# Informe: Sprint hacia Product-Market Fit (0 → 100 clientes) — AI Trend Hunter

**Fecha:** 26 de julio de 2026
**Destinatario:** ChatGPT / cualquier lector sin contexto previo. Documentos relacionados: `docs/HANDOFF_CTO.md` (arquitectura y producto completos), `docs/SECURITY_CI_INSTRUMENTATION_REPORT.md` (seguridad/CI/analítica, ya resueltos, no se tocan en este sprint).
**Encargo:** actuar como equipo de producto/growth/UX/founder y aumentar la probabilidad de conseguir los primeros 100 clientes de pago, sin añadir funcionalidad por añadir. Regla aplicada a cada decisión: *¿esto aumenta la probabilidad de que alguien pague 39€/mes?*

Todo lo descrito como "implementado" está commiteado, testeado, **desplegado en producción real** (`aitrendhunter.app`), y verificado con datos reales tras el deploy — incluyendo un backfill de datos de producción necesario para que el cambio se viera bien desde el primer segundo, no en 24 horas.

---

## Problemas detectados (Fase 1 — auditoría de producto)

- **Landing**: describe funcionalidades ("multi-source signal collection", "trend scoring"), no vende una conclusión. El hero es lo único que se acerca a vender un resultado.
- **Dashboard**: antes de este sprint era una tabla de tendencias ordenada por score. El usuario tenía que leer, comparar y decidir por sí mismo qué mirar primero — trabajo cognitivo cobrado a 39€/mes, exactamente el antipatrón "dashboard de métricas" que se pidió eliminar.
- **Trial**: sin ningún momento diseñado de "wow" en los primeros 5 minutos.
- **Activación**: no existía ningún evento del producto que entregara una conclusión ("esto merece la pena") — solo datos para que el usuario sacara su propia conclusión.
- **Retención**: cero mecanismo, ni siquiera de arquitectura, para dar una razón de volver mañana.
- **Monetización a 3 meses**: sin activación ni retención, la única fuerza que sostenía el cobro era la inercia de la tarjeta ya cargada — el tipo de suscripción que se cancela en cuanto alguien mira su extracto.
- **Brecha entre promesa y producto**: la landing ya prometía "SaaS opportunity briefs... who, why now, and where the gap is" — pero el producto real solo entregaba tres frases de plantilla fija por tendencia. La promesa de marketing iba por delante del producto.

## Cambios implementados

### 1. Motor de oportunidades (heurístico, sin LLM, sin coste nuevo)

Cada tendencia calcula ahora, en el mismo pipeline determinista que ya calculaba `trend_score`/`opportunity_score` (ver `docs/HANDOFF_CTO.md` sección 7), un **brief de decisión completo**:

- Resumen ejecutivo, por qué ahora (why now), a quién vendérselo (ICP), qué problema resuelve, nivel de competencia, MVP recomendado a construir, modelos de monetización sugeridos, riesgos detectados.
- Un desglose explicable de 5 sub-scores (**Market, Competition, Urgency, Viability, Potential**) que sustentan el `opportunity_score` ya existente — no es un segundo sistema de scoring paralelo, es la misma fórmula desglosada para que se entienda de dónde sale el número.
- **Deliberadamente sin LLM**: no hay `OPENAI_API_KEY` ni `ANTHROPIC_API_KEY` configuradas, y añadirlas cambiaría el margen del negocio (hoy el coste marginal por cliente es ≈0). Todo el texto sale de reglas y plantillas sobre datos ya calculados — mismo enfoque honesto que el scoring original, solo que estructurado como brief en vez de cuatro números sueltos.
- Se detectó y corrigió en QA local, **antes de tocar producción**, que la primera versión del brief salía en español mezclado con un producto que es 100% en inglés — capturado con una revisión visual real en navegador antes del deploy, no después.
- De paso, se corrigió un bug preexistente de capitalización ("Ai Agents" → "AI Agents") que se volvió mucho más visible al ponerlo en el titular principal del dashboard.

### 2. Dashboard rediseñado: de tabla a decisión

La primera pantalla del dashboard ahora abre con:

- **🔥 Best opportunity this week**: la tendencia con mayor `opportunity_score`, con su brief completo visible sin necesidad de ningún clic — resumen, por qué ahora, ICP, problema, competencia, señal de mercado, MVP a construir, formas de monetizar, riesgos, y los 5 sub-scores.
- **4 listas de Top 5** debajo: Top 5 oportunidades, Top 5 mercados emergentes (una tendencia representativa por categoría), Top 5 nichos infraatendidos (buen score + baja saturación), Top 5 acelerando (mayor momentum). Cada tarjeta enlaza directamente al brief completo de esa tendencia.
- La lista filtrable y el panel de detalle que ya existían **se mantienen intactos debajo**, bajo el rótulo "Explore all trends" — no se ha quitado ninguna funcionalidad, se ha añadido una capa de decisión encima.
- Nuevo endpoint `GET /api/v1/trends/spotlight` que entrega todo este bundle en una sola llamada (eficiente para la carga inicial del dashboard).

### 3. Copy de landing corregido para que coincida con el producto real

La feature #5 de la landing describía un "Operating dashboard" genérico con una etiqueta "MVP dashboard" — quedaba desactualizada frente al rediseño y, encima, sonaba a producto a medio hacer. Reescrita para describir exactamente lo que el dashboard hace ahora: abrir con la mejor oportunidad ya explicada, sin tabla que interpretar primero.

### 4. Onboarding (Fase 4) — resuelto como efecto colateral del punto 2, no como pieza aparte

Se pidió explícitamente no construir un dashboard vacío ni un tour — y no hacía falta: al ser el dashboard mismo el que abre con "estas son las 3-5 oportunidades que deberías mirar" (hero + top 5), el primer minuto, primer clic (brief completo), segundo clic (otra oportunidad del top 5) y tercer clic (MVP recomendado dentro del mismo brief) ya están cubiertos por el rediseño de la sección 2, sin necesitar ninguna pieza de UI adicional de onboarding.

### 5. Retención (Fase 6) — solo arquitectura, tal como se pidió

No se ha implementado ninguna notificación. El mecanismo recomendado, listo para construir cuando se decida:

- Aprovechar el cron diario ya existente (`trendhunter-ingestion-cron`, corre a las 08:00 UTC) para, después de re-ingerir señales, comprobar si la mejor oportunidad de la semana ha cambiado desde el último email enviado a cada suscriptor.
- Reutilizar Resend (ya integrado, ya en modo live) para mandar un email semanal con el nuevo "Best opportunity this week" — mismo dato que ya se calcula para el hero del dashboard, cero trabajo de cómputo nuevo.
- Necesitaría una única tabla o columna nueva para rastrear el último envío por suscriptor (no implementada todavía, a propósito).

## Archivos modificados

**Backend**
- `backend/app/models/base.py` — nueva columna `opportunity_brief` (JSON) en `trends`.
- `backend/migrations/versions/0005_opportunity_brief.py` — migración Alembic, verificada de punta a punta en local antes de desplegar.
- `backend/app/services/detector_service.py` — `CATEGORY_PROFILES`, `_build_opportunity_brief()`, `_titlecase()` (fix de acrónimos).
- `backend/app/services/trend_service.py` — `best_opportunity()`, `top_opportunities()`, `emerging_markets()`, `underserved_niches()`, `accelerating()`.
- `backend/app/api/v1/trends.py` — nuevo endpoint `GET /trends/spotlight`.
- `backend/app/schemas/schemas.py` — `OpportunityScores`, `OpportunityBrief`, `TrendSpotlightResponse`.
- `backend/scripts/backfill_opportunity_briefs.py` — script de backfill one-off (ejecutado ya en producción).
- `backend/tests/test_trends_api.py`, `test_ingestion_api.py`, `test_rss_ingestion.py` — tests nuevos y assertions actualizadas al fix de acrónimos.

**Frontend**
- `frontend/src/app/dashboard/page.tsx` — hero + 4 listas top-5, fix de `selectedSlug` para que los enlaces del top-5 seleccionen correctamente el detalle aunque el trend no esté en la lista filtrada actual.
- `frontend/src/app/globals.css` — estilos nuevos (`.spotlight*`, `.top5*`).
- `frontend/src/app/page.tsx` — copy de la feature del dashboard actualizado.
- `frontend/src/lib/api.ts` — `getTrendSpotlight()`.
- `frontend/src/types/trend.ts` — tipos `OpportunityBrief`, `OpportunityScores`, `TrendSpotlight`.

**Raíz**
- `docs/PMF_SPRINT_REPORT.md` — este informe.

## Verificación realizada (no solo "debería funcionar")

- 60/60 tests backend en verde, incluidos 2 nuevos que comprueban que el brief se genera con todos sus campos y que el bundle de spotlight excluye correctamente la tendencia hero de la lista de top 5.
- Migración probada de cero contra una base local antes de tocar producción.
- **QA visual real**: backend y frontend levantados en local, login real (código de un solo uso), datos reales ingeridos, capturas de pantalla del hero y las listas top-5 revisadas antes de desplegar — así se detectó el bug de idioma español.
- Tras el deploy: `curl` confirma el endpoint `/trends/spotlight` protegido y funcionando; se detectó que las 40 tendencias ya existentes en producción no tenían brief todavía (se habían ingerido antes de este cambio) y **se corrigió con un backfill inmediato** en vez de dejar el hero vacío durante 24 horas hasta el próximo cron.
- Las 4 pruebas de Playwright, incluida la del paywall, siguen en verde contra producción tras el deploy.

## Impacto esperado

**Activación esperada**: alta confianza de mejora. El evento de activación ("esto merece la pena") ahora tiene un momento concreto y medible: ver el hero completo en el primer dashboard view. Ya existe instrumentación previa (`Dashboard Viewed`, `Trend Viewed`, `Opportunity Viewed` vía Plausible, ver `SECURITY_CI_INSTRUMENTATION_REPORT.md`) para medir esto en cuanto haya tráfico real — recomendado: mirar en Plausible si `Trend Viewed` ocurre en el primer minuto de sesión ahora, frente a antes.

**Conversión esperada**: mejora moderada-alta en el tramo trial→pago. La hipótesis de negocio no probada más grande de este producto ("¿alguien paga 39€/mes por esto?") ahora se prueba con la versión del producto que sí cumple lo que la landing promete, no con una versión que prometía de más. Es la variable de mayor apalancamiento del embudo completo.

**Retención esperada**: sin cambio todavía — el mecanismo de vuelta (email semanal) está diseñado pero no construido, tal como se pidió. Es, con diferencia, el hueco más grande que queda abierto tras este sprint.

**Monetización a 3 meses**: mejora indirecta vía activación/conversión. No se ha tocado precio, trial ni checkout (ya resueltos y verificados en el sprint de seguridad anterior).

## Tabla RICE (Fase 7-8) — todo lo evaluado, no solo lo implementado

RICE = (Reach × Impact × Confidence) / Effort. Reach y Effort en escala relativa 1-10 dado que el producto no tiene todavía volumen de usuarios real que dé cifras absolutas fiables; Impact en la escala estándar (0.25/0.5/1/2/3); Confidence en %.

| # | Cambio | Reach | Impact | Confidence | Effort | RICE | Estado |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Hero "Best opportunity" + motor de brief heurístico | 10 | 3 | 80% | 3 | **8.0** | ✅ Implementado |
| 2 | Fix de copy de landing (feature #5, dashboard) | 8 | 1 | 70% | 0.25 | **22.4** | ✅ Implementado |
| 3 | Fix de capitalización de acrónimos (AI/API/SaaS) | 10 | 0.5 | 90% | 0.25 | **18.0** | ✅ Implementado |
| 4 | Email semanal de retención (arquitectura lista, sin construir) | 10 | 2 | 70% | 2 | **7.0** | 📐 Diseñado, no implementado (pedido explícito) |
| 5 | Insights generados por LLM real en vez de heurística | 10 | 2 | 40% | 5 | **1.6** | ⛔ Descartado por ahora — requiere credencial y cambia el margen del negocio |
| 6 | Reescribir las 5 features de la landing (no solo la #5) | 8 | 1 | 50% | 1.5 | **2.67** | ⛔ Diferido — riesgo real de romper un layout HTML/CSS hecho a mano por ganancia incierta |
| 7 | Tour de onboarding / checklist de bienvenida | — | — | — | — | — | ⛔ Descartado — el propio encargo pedía evitarlo, y el hero ya resuelve el mismo problema |
| 8 | Quitar la tarjeta obligatoria en el trial | — | — | — | — | — | Fuera de alcance — decisión de negocio ya tomada y revertida conscientemente en una sesión anterior |

**Justificación de las puntuaciones más altas**: los cambios #2 y #3 tienen el RICE más alto de la tabla no porque sean los más importantes en términos absolutos, sino porque su `Effort` es casi cero — son el tipo de cambio que siempre hay que hacer primero. El cambio #1 es el que de verdad mueve la aguja (Impact=3, el máximo de la escala) y por eso se hizo primero pese a tener más esfuerzo, ya que sin él los cambios de copy no tendrían nada honesto que vender.

## Próximos pasos

1. **Email semanal de retención** (RICE 7.0, ítem #4) — el hueco más grande que queda. Requiere: una tabla/columna para rastrear el último envío por suscriptor, y enganchar el envío al cron diario ya existente.
2. **Medir de verdad, no asumir**: los eventos de Plausible (`Dashboard Viewed`, `Trend Viewed`, `Opportunity Viewed`) ya están instrumentados — en cuanto haya un puñado de sesiones reales, revisar si la gente efectivamente interactúa con el hero y el top-5 antes de tocar nada más.
3. **Backfill continuo garantizado**: el cron diario ya recalculará `opportunity_brief` para tendencias nuevas o re-tocadas automáticamente; no hace falta volver a correr el script de backfill salvo que se añada otro campo estructurado nuevo en el futuro.
4. Revisar si el resto de la landing (features #1-4) merece la misma pasada de "esto ya es verdad, dilo mejor" ahora que el producto cumple más de lo que promete.

---

## La pregunta final: si esto fuera tu SaaS, ¿qué harías en los próximos 30 días?

Respuesta directa, sin adornos:

**No construiría nada más.** Lo que se ha hecho hoy — que el producto por fin entregue en el primer segundo lo que la landing lleva meses prometiendo — es la pieza de producto más importante que faltaba, y ya está en producción. A partir de aquí, los siguientes 30 días son de **validación con personas reales, no de código**.

Concretamente:

1. **Semana 1**: hablar con 15-20 personas del público objetivo (indie hackers, PMs, scouts) enseñándoles el dashboard real — no la landing, el dashboard — y preguntar directamente: "¿pagarías 39€/mes por esto tal como lo ves ahora?". Si la respuesta mayoritaria es no, averiguar por qué antes de gastar un euro en ads. Esto es más barato y más rápido que cualquier otro experimento posible.
2. **Semana 1-2, en paralelo**: lanzar la campaña de Meta Ads que ya está configurada y con tracking verificado desde el sprint anterior. El presupuesto bajo (~300-500€/mes) ya decidido es correcto para esta fase — no subirlo hasta tener una tasa de conversión trial→pago real que lo justifique.
3. **Semana 2-3**: con los primeros clics de pago reales (aunque sean 3, 5, 10), mirar en Plausible si de verdad interactúan con el hero/top-5 antes de cancelar o quedarse. Si el patrón es "ven el hero, no vuelven al segundo día", el problema no es el dashboard, es la retención — y ahí es donde construiría el email semanal de retención, no antes, porque hoy no hay datos que confirmen que hace falta.
4. **No tocaría el motor heurístico ni añadiría LLM todavía.** Cuesta dinero real por primera vez en la vida de este producto, y sin haber validado que el heurístico actual ya convence a un cliente de pago, gastar en IA generativa sería optimizar la parte del producto que nadie ha confirmado que sea el cuello de botella.
5. **Sí revisaría el copy del resto de la landing** (features #1-4) con el mismo criterio que se aplicó hoy a la #5 — es gratis, es rápido, y ahora el producto por fin sostiene promesas más ambiciosas de las que hacía antes.

La palanca más grande de las próximas 100 clientes no es más ingeniería. Es descubrir, con datos de personas reales pagando, si el salto de "tabla de tendencias" a "oportunidad explicada" que se acaba de construir es realmente lo que faltaba — y ese experimento ya se puede correr hoy mismo, sin escribir una línea más de código.
