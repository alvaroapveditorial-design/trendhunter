# Informe: Revisión en vivo del dashboard rediseñado — hallazgos y correcciones

**Fecha:** 26 de julio de 2026
**Destinatario:** ChatGPT / cualquier lector sin contexto previo. Documento complementario a `docs/HANDOFF_CTO.md` (producto y arquitectura completos), `docs/SECURITY_CI_INSTRUMENTATION_REPORT.md` (seguridad/CI/analítica) y `docs/PMF_SPRINT_REPORT.md` (rediseño del dashboard a "decisiones, no métricas"). Este informe cubre lo que pasó **después** de desplegar ese rediseño: una revisión real, en vivo, del producto ya en producción.

## Contexto y metodología

Inmediatamente después de desplegar el rediseño del dashboard (documentado en `PMF_SPRINT_REPORT.md`), el fundador pidió una revisión práctica: ponerse en la piel de un indie hacker que usa la app por primera vez y detectar cualquier cosa que "chirríe". En vez de una auditoría de código en abstracto, esta revisión se hizo **contra la sesión real del fundador, en su propio Chrome, en producción real** (`aitrendhunter.app`) — no en un entorno de pruebas ni con datos ficticios. Cada hallazgo de esta sesión es sobre lo que un cliente de pago real vería hoy, y cada corrección se verificó volviendo a mirar la misma pantalla tras desplegar el fix.

Esto importa para el lector: los hallazgos aquí no son hipotéticos ni de code review — son cosas que estaban literalmente visibles en la cuenta de producción del propio fundador en el momento de la revisión.

## Hallazgos y correcciones, en el orden en que aparecieron

### 1. Megaproyectos ya famosos ocupando el hero y las listas top-5

**Encontrado:** la tendencia "mejor oportunidad" y las listas de Top 5 estaban dominadas por proyectos de IA ya masivos y conocidos globalmente (AutoGPT, Dify, ComfyUI, Open WebUI...), con la etiqueta "Competition: Low — open gap". Esto no tenía sentido: son de los proyectos de código abierto de IA más famosos que existen.

**Causa raíz:** el nivel de "competencia" que calcula el sistema se basa en cuántas fuentes ha visto *este propio producto*, no en awareness real de mercado — un proyecto globalmente famoso puede salir como "hueco abierto" simplemente porque el pipeline nunca lo había visto antes.

**Corrección:** la query de búsqueda de GitHub pasó de `topic:ai stars:>50` (sin techo) a `topic:ai stars:50..3000`, excluyendo explícitamente los proyectos ya masivos. La premisa del producto es detectar oportunidades *antes* de que sean obvias — un proyecto con decenas de miles de estrellas es exactamente lo contrario.

### 2. Las cuatro listas de "Top 5" eran la misma lista repetida

**Encontrado:** "Top 5 opportunities", "Top 5 underserved niches" y "Top 5 accelerating" mostraban casi los mismos 4-5 nombres, solo en distinto orden — no cuatro ángulos distintos, sino uno repetido cuatro veces.

**Corrección:** cada lista ahora excluye explícitamente las tendencias ya mostradas por una lista anterior en la misma respuesta (hero → top opportunities → emerging markets → underserved niches → accelerating, cada una restando las anteriores del pool disponible). Además, `underserved_niches` cambió su criterio de orden de "mayor opportunity_score" a "mayor diferencia entre opportunity y saturación", para que sea un corte de datos genuinamente distinto, no solo una lista sin duplicados por fuerza bruta.

### 3. Contenido que no es una oportunidad de negocio, mal clasificado

**Encontrado:** una guía de entrevistas de Java en chino ("JavaGuide") aparecía en la lista de "oportunidades de SaaS" con la etiqueta "ai saas", con score 100.

**Causa raíz:** la búsqueda de GitHub por `topic:ai` también devuelve guías de referencia, listas "awesome" y material de curso etiquetado "ai" — señal real para un catálogo de cursos, no para una oportunidad de SaaS.

**Corrección:** nuevo filtro (`NON_PRODUCT_MARKERS`) que descarta cualquier repo cuyo nombre/descripción/topics contengan marcadores de contenido de referencia ("interview", "awesome-list", "cheatsheet", "roadmap", "guide", "tutorial", "course"...), antes de que llegue a convertirse en tendencia.

### 4. Al arreglar lo anterior, salió a la luz un problema más grande: contenido irrelevante en Hacker News y RSS

**Encontrado:** con los megaproyectos fuera, el hero pasó a ser **"Hannah Fry Wins Leelavati Prize"** — una noticia sobre una matemática ganando un premio. No tenía absolutamente nada que ver con SaaS.

**Causa raíz:** Hacker News y los feeds de RSS no tenían ningún filtro de relevancia — se ingería cualquier historia del top de HN o cualquier ítem de los feeds configurados, sin comprobar si tenía algo que ver con tecnología, producto o startups.

**Corrección:** ambos collectors ahora exigen que el título (y, en RSS, también el resumen) contenga al menos un término de una lista de relevancia (ai, startup, funding, developer tools, privacy, producto, lanzamiento...) antes de convertirse en señal. El feed de Product Hunt queda exento de este filtro porque, por construcción, todo su contenido son lanzamientos de producto — aplicar el filtro ahí solo eliminaba productos reales con descripciones sencillas.

### 5. Las puntuaciones se repetían de forma idéntica entre tendencias distintas

**Encontrado:** varias tendencias completamente distintas (repos diferentes, de dominios diferentes) mostraban exactamente el mismo trend_score (81, luego 85) una tras otra. Un usuario que comparase dos o tres tendencias seguidas notaría el patrón y dejaría de confiar en el número.

**Causa raíz, primera capa:** el "engagement" (estrellas, comentarios, forks) sigue una distribución de ley de potencia, no lineal. La fórmula de velocidad usaba un divisor lineal que tocaba su techo (35 puntos) en cuanto un repo superaba ~280 unidades de engagement — trivial dentro del rango de 50 a 3.000 estrellas ya filtrado. Cualquier repo por encima de ese umbral puntuaba exactamente igual.

**Corrección, primera capa:** la velocidad pasó de una fórmula lineal (`engagement / 8`, con techo) a una escala logarítmica (`log10(engagement + 1) * 10`, con el mismo techo de 35). Esto reparte la diferenciación por todo el rango práctico en vez de aplanar la mayoría contra el techo.

**Causa raíz, segunda capa:** tras el fix anterior, las puntuaciones seguían agrupándose — esta vez porque la búsqueda de GitHub ordenaba por estrellas descendente *dentro* de un rango ya acotado (50-3.000), así que los resultados siempre eran los repos más cercanos al techo del rango (2.500-3.000 estrellas), justo donde la escala logarítmica comprime más.

**Corrección, segunda capa:** el orden de búsqueda pasó de `sort=stars` a `sort=updated` (repos más recientemente activos), lo que da variedad real de estrellas dentro del rango en vez de concentrarse siempre en el techo.

**Verificación:** tras ambos fixes, una consulta directa a producción mostró tendencias con scores 86.0, 82.6, 73.9, 73.4, 73.3, 73.1 — variedad real, no repetición.

### 6. Purga y reingesta limpias

Dado que se habían disparado varias reingestas manuales seguidas durante las pruebas de este mismo día (inflando artificialmente la "recurrencia" de algunos repos que aparecían en más de una tanda), se desactivaron todas las tendencias activas y se hizo una única reingesta limpia, para que lo que viera el fundador fuera un reflejo honesto del pipeline ya arreglado, no una mezcla de datos de antes y después del fix.

### 7. El nombre del producto en Stripe

**Encontrado:** al abrir "Manage billing" (que sí funcionó correctamente — confirma que el fix de seguridad de la sesión anterior, el portal de facturación atado a la sesión real, funciona con un usuario real), el producto mostrado en el portal de Stripe se llamaba literalmente **"tren hunter test"**, con descripción en español — visible justo en el momento en que un cliente revisa con más lupa qué está pagando.

**Corrección:** llamada directa a la API de Stripe (con la clave live ya configurada en Railway) para renombrar el producto a **"AI Trend Hunter Pro"** con una descripción en inglés coherente con el resto del producto. Se comprobó también el "statement descriptor" (lo que aparece en el extracto bancario real del cliente) — ese ya estaba correctamente configurado como "AI TREND HUNTER", no requería cambio. Verificado recargando el portal real tras el cambio.

### 8. Contenido en chino sin traducir

**Encontrado:** dos tendencias reales (no basura, productos legítimos) tenían su descripción en chino, tal cual venía del repositorio de GitHub de origen: "Lanhu Mcp" (descripción íntegramente en chino) y "Token Monitor" (descripción mayormente en inglés con una frase completa en chino pegada al final).

**Causa:** el producto es 100% en inglés (landing, pricing, dashboard) y no existe ningún paso de traducción (no hay LLM ni servicio de traducción configurado — coste cero es una ventaja de margen consciente de este producto, documentada en `HANDOFF_CTO.md`). Sin traducción posible, la única opción honesta es no mostrar el contenido no traducible.

**Corrección:** nuevo módulo compartido `text_filters.py` con `looks_non_english()`, que detecta cuándo una parte significativa del texto cae en rangos Unicode de chino/japonés/coreano/cirílico/árabe. Aplicado en los tres collectors. Primer despliegue con umbral de 15% no capturó el caso de "Token Monitor" (14,37%, justo por debajo) — se bajó a 10% tras comprobar el caso real, con un test de regresión que fija ese caso exacto.

### 9. Verificaciones adicionales (todo correcto, sin cambios necesarios)

Durante la misma sesión se probó explícitamente y se confirmó que funciona bien:

- Selección de tendencias desde la lista principal y desde las listas de Top 5 (resaltado correcto, carga del brief correspondiente).
- Buscador: no distingue mayúsculas/minúsculas, busca en título **y** descripción (probado con "PYTHON" en mayúsculas, encontró "Clawcodex" por una mención de Python en su descripción, no en el título).
- Filtros de categoría, fuente y score mínimo, incluido el estado vacío ("No trends found") cuando no hay resultados.
- "Clear filters" resetea correctamente la URL.
- "Recent pipeline runs" y "Source signals" muestran datos reales y trazables.
- Expiración de sesión a los 60 minutos funcionando como está diseñado (se disparó de forma natural durante la propia revisión, por la duración de la sesión de trabajo — comportamiento correcto, no un fallo).

## Aclaración de producto importante para quien diseñe el roadmap

Durante la revisión, el fundador preguntó si el dashboard requiere interacción. La respuesta, confirmada por el diseño ya implementado: **no**. La parte superior (mejor oportunidad de la semana + las cuatro listas de Top 5) es puramente informativa — se entra, se lee, y ya se ha obtenido el valor completo sin tocar nada. Todo lo que hay debajo ("Explore all trends": buscador, filtros, exploración manual) es opcional, pensado para cuando el usuario ya tiene algo concreto en mente y quiere comprobar si el producto lo está vigilando — no es la vía principal de generar valor. Esto confirma que el objetivo del rediseño de la sesión anterior ("un dashboard de decisiones, no de métricas") se cumplió: el producto se consume como un briefing, no se opera como una herramienta.

## Archivos modificados en esta sesión de revisión

**Backend**
- `backend/app/services/github_collector.py` — techo de estrellas, orden por actividad reciente, filtro de contenido de referencia, filtro de idioma.
- `backend/app/services/hackernews_collector.py` — filtro de relevancia, filtro de idioma.
- `backend/app/services/rss_collector.py` — filtro de relevancia (con excepción para Product Hunt), filtro de idioma.
- `backend/app/services/detector_service.py` — velocidad en escala logarítmica.
- `backend/app/services/trend_service.py` — exclusión cruzada entre las cuatro listas, `underserved_niches` reordenado por diferencia oportunidad/saturación.
- `backend/app/services/text_filters.py` — **nuevo**. Detección de contenido no-inglés compartida por los tres collectors.
- `backend/scripts/deactivate_oversized_repos.py`, `deactivate_reference_content.py`, `deactivate_off_topic_signals.py`, `deactivate_non_english_signals.py`, `purge_and_reset_trends.py` — **nuevos**, scripts de limpieza one-off, todos con borrado reversible (`is_active=False`, nunca borrado físico).
- `backend/tests/test_github_ingestion.py`, `test_text_filters.py` (nuevo) — tests de regresión para cada hallazgo.

**Stripe (configuración externa, no código)**
- Producto `prod_UwatBpkhUcg3zf`: nombre y descripción actualizados vía API directa.

**Documentación**
- `docs/DASHBOARD_QA_WALKTHROUGH_REPORT.md` — este informe.

## Estado final verificado en producción

- 72 tests de backend en verde.
- Pool de tendencias activas reconstruido limpio tras todos los fixes: puntuaciones diferenciadas, sin megaproyectos, sin contenido de referencia, sin ruido de noticias generales, sin texto sin traducir.
- Portal de facturación de Stripe verificado con el nombre de producto correcto, en la cuenta real del fundador.
- Cada corrección se verificó dos veces: primero contra la API de producción directamente (`curl`), después visualmente en el navegador real del fundador con su sesión activa.

## Pendientes / notas residuales

- La diversidad de categorías sigue siendo baja ahora mismo (casi todo "ai_saas") porque la búsqueda de GitHub está intrínsecamente acotada a `topic:ai` — esto es estructural, no un bug, y mejorará según se acumule más señal de Hacker News y RSS (que sí cubren más categorías) en los próximos días.
- El pool de tendencias es todavía pequeño (15-30 según el momento) tras las sucesivas purgas de hoy — se repondrá solo con el cron diario existente, sin necesitar intervención.
- No se ha probado el flujo completo de "Log out" en la sesión real del fundador (para no interrumpir su propia revisión) — ya estaba cubierto por los tests automatizados de la sesión de seguridad anterior.
- El umbral del filtro de idioma (10%) es una heurística ajustada a los casos reales vistos hasta ahora; si aparecen casos nuevos de contenido parcialmente no-inglés que se cuelen, es una constante de una línea (`text_filters.py`) fácil de volver a ajustar.
