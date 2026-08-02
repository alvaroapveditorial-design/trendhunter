# Proyecto Phoenix — Fase 1
## Investigación estratégica de conversión — AI Trend Hunter

**Fecha:** 2 de agosto de 2026
**Encargo:** por qué AI Trend Hunter, con infraestructura estable, pagos funcionando y una campaña activa con métricas de adquisición sanas, sigue en **0 trials** después de aprox. 90 clics / 84 visitas reales.
**Método:** investigación real — navegación en vivo de los tres competidores directos y de los adyacentes citados, lectura del código fuente exacto de la home, `/pricing`, login y checkout de AI Trend Hunter, y los datos reales de campaña/analítica recogidos durante esta misma semana de lanzamiento.
**Convención de este documento:** toda afirmación va etiquetada **[EVIDENCIA]** (observada directamente — captura, código fuente o dato de producción) o **[HIPÓTESIS]** (razonamiento experto no verificado, con su plan de validación). Ninguna afirmación se presenta como hecho si no lo es.

---

## Resumen ejecutivo (léase primero)

**[EVIDENCIA]** El problema no es el canal, ni el precio del clic, ni el producto en sí. El problema está en un punto extremadamente concreto y localizado: **la página que recibe el 88,7% del tráfico de pago (`/pricing`) no contiene ni una sola prueba de que el producto funcione.** Un visitante frío llega ahí, lee un titular, cinco bullets genéricos, y una tarjeta que le pide el email para ir a pagar con tarjeta — sin haber visto jamás un ejemplo real, una cifra verificable, una cara humana, o un solo dato del propio producto.

Los tres competidores directos investigados (Exploding Topics, Glimpse, Trends.vc) comparten, sin excepción, tres elementos que AI Trend Hunter no tiene hoy en ningún sitio de su funnel:
1. **Una forma de experimentar valor real sin pagar y sin tarjeta** (explorador de tendencias público, informe gratuito, o extensión gratuita).
2. **Prueba verificable con nombres reconocibles** (tendencias famosas marcadas "descubierto hace X" — Pickleball, Notion, Perplexity AI, Substack — no ejemplos inventados).
3. **Prueba social humana o corporativa** (logos de Google/Shopify/McKinsey, un testimonio con nombre y cargo, o miles de fundadores con cara visible).

AI Trend Hunter no tiene ninguno de los tres. Esa es, con alta confianza, la causa raíz de la conversión cero — no una hipótesis vaga de "falta de confianza", sino una ausencia estructural específica y localizable en el código de la página que reciben tus visitantes.

---

# FASE 1 — Investigación de competencia

## 1.1 Metodología

Visité en vivo hoy: **Exploding Topics** (incluida su versión Pro/pricing), **Glimpse**, **Trends.vc**, **Google Trends** y **Product Hunt**. No pude completar la comprobación de tabla de precios de Exploding Topics Pro por un fallo de scroll en esa página concreta (irónico, dado el hallazgo de la Fase 2 sobre AI Trend Hunter) — el resto de hallazgos de esa web son de observación directa.

No visité en vivo **Indie Hackers, CB Insights, Ahrefs y Semrush** porque, tras revisar su posicionamiento público, ninguno compite por el mismo comprador con la misma intención de compra que AI Trend Hunter — son herramientas adyacentes, no rivales directos. Los trato con menos profundidad y lo digo explícitamente en cada caso, en vez de simular un análisis exhaustivo que no hice.

## 1.2 Competidores directos (misma promesa: "encuentra la próxima tendencia antes que nadie")

### Exploding Topics *(propiedad de Semrush — dato relevante: ya no es un indie player, es una empresa de datos SEO/marketing con recursos de una compañía cotizada)*

**[EVIDENCIA]**
- Hero: *"Discover Trends 12+ Months Before Everyone Else"* — promesa cuantificada y específica (12+ meses), no vaga como "antes de que sean obvias".
- CTA primario: *"Find Trends Before Competitors"* (orientado a acción/beneficio, no a "empezar prueba"). CTA secundario: *"Free Access"* con flecha — el acceso gratuito está tan destacado como el de pago.
- Justo debajo del hero, **sin scroll casi**: un explorador de tendencias completamente público y gratuito, con gráficas reales de volumen de búsqueda y crecimiento (ej. "Bifacial" 4.4K volumen +94%, "Wolf Haircut" 110K volumen +14%), filtrable por categoría y periodo. **Nadie tiene que registrarse para ver esto.**
- Prueba social corporativa: *"Trusted by brands that refuse to fall behind"* + logos reales de **Google, McKinsey & Company, Shopify, Goldman Sachs, Unilever**.
- En la página de precios (Pro), la prueba de producto usa tendencias que el visitante ya conoce y puede verificar mentalmente: **Pickleball, Substack, Snail Mucin, Air Fryer, Perplexity AI**, cada una con una etiqueta *"DISCOVERED"* marcando el punto en la curva donde la herramienta la señaló, antes del despegue.

**Fortalezas:** marca ya establecida (adquisición por Semrush), prueba de producto sin fricción, prueba social de máximo nivel (Fortune 500).
**Debilidades observables:** la home mezcla contenido de blog con producto (mi extracción de texto capturó un artículo de blog en vez del hero en el primer intento — señal de que la arquitectura de información no es perfectamente limpia); la página de pricing que visité no reveló las cifras de los planes en el tiempo que le dediqué.

### Glimpse

**[EVIDENCIA]**
- Hero: *"Discover trends before they're trending"* + subtítulo que ya diferencia la fuente de datos: *"Unlock the power of search data and tap directly into the minds of consumers"* — deja claro desde la primera línea que su materia prima es el comportamiento de búsqueda, no repos de GitHub ni hilos de Hacker News.
- Debajo del hero, la misma técnica que Exploding Topics pero más explícita: una fila de tendencias **famosas y verificables** — Perplexity AI, Mouth Tape, Canva, SHEIN, Pickleball, Pimple Patches, OnlyFans, Substack, TikTok, Remote Jobs, Notion — cada una con *"Predicted [X] Years Ago"*. Es prueba social por reconocimiento inmediato: el visitante no tiene que confiar en la palabra de Glimpse, reconoce la tendencia él mismo.
- Insignia explícita **"IT'S FREE"** junto al botón "Sign Up", repetida dos veces en la página.
- Testimonio con nombre y cargo reales: *"Luke Esbenson, Senior Culinary Development Manager"*.
- Cifras duras y específicas: *"120X more trends than the closest competitor"*, *"95%+ backtested accuracy"* en su forecasting, valoración **4.91 (170,000+ users)**, presencia en **132+ países**.
- Segmentación explícita por rol/caso de uso: SEO, Ecommerce, Market Research, PR, Investing — cada uno con su propia narrativa de "por qué te sirve a ti".
- Canal de distribución adicional: extensión de Chrome (reduce fricción de descubrimiento y uso recurrente).

**Fortalezas:** el conjunto de pruebas (nombres reconocibles + testimonio humano + cifras verificables + gratis) es el más completo de los tres competidores.
**Debilidades:** propuesta muy centrada en "datos de búsqueda" — más orientada a marketing/ecommerce que a "qué SaaS construir", así que su solapamiento real con el ICP de AI Trend Hunter (fundadores técnicos buscando oportunidades de producto) es parcial.

### Trends.vc

**[EVIDENCIA]** — este es, con diferencia, el competidor más parecido en audiencia (fundadores/indie hackers, no marketers ni analistas de marca).
- Insignia *"🏆 Product Hunt — #1 Product of the Month"* arriba del todo — prueba social prestada de una comunidad que el propio público objetivo de AI Trend Hunter conoce y respeta.
- Hero: *"Dive into new markets and ideas with 54,782 like-minded founders."* — el número exacto (no "50,000+") transmite más veracidad que un número redondeado, y "like-minded founders" habla directamente a la identidad del visitante, no a una función abstracta.
- Subtítulo con promesa de ahorro de tiempo cuantificada: *"Save 2,000+ hours of market research with free 5-minute reports on AI, Crypto and more."*
- Grid visual de **caras reales de fundadores** (fotos, no iconos ni avatares genéricos) — refuerzo visual inmediato de "esto lo usa gente real como tú".
- Entrada: solo email, botón *"Get Started"*. Sin tarjeta. El modelo es freemium de contenido: primero entregan valor real gratis (los informes de 5 minutos), y "Trends Pro" es la puerta de pago que aparece **después**, cuando ya hay confianza construida.

**Fortalezas:** la audiencia y el tono encajan casi exactamente con el ICP declarado de AI Trend Hunter ("Founder / co-founder", "Indie hacker" son literalmente dos de las cinco opciones del propio formulario de "Stay in the loop" de AI Trend Hunter). Es el competidor que más debería estudiarse.
**Debilidades:** formato de "informes" es más pesado/editorial que un dashboard en vivo — probablemente menos "fresco" día a día que lo que promete AI Trend Hunter.

## 1.3 Adyacentes / no competidores directos — tratados con menos profundidad, y digo por qué

**Google Trends [EVIDENCIA, visitado hoy]:** gratuito, universal, datos de búsqueda en crudo sin ninguna curación, scoring ni narrativa de oportunidad ("terremoto Murcia", "quiebra" y nombres propios mezclados sin criterio de negocio en la vista que vi). Es el **suelo de comparación implícito**: cualquier visitante que ya conozca Google Trends evaluará a AI Trend Hunter preguntándose "¿por qué pagar 39€/mes por esto en vez de usar lo gratis?" — y hoy la landing no responde a esa pregunta explícitamente en ningún sitio.

**Product Hunt [EVIDENCIA, visitado hoy]:** comunidad de descubrimiento y lanzamiento de productos, no un competidor de scoring de tendencias — de hecho, es más una **fuente de señal potencial** (lanzamientos ordenados por votos) que una empresa rival. Ya aparece nombrado como fuente de RSS en la configuración del propio backend de AI Trend Hunter (`producthunt` en `RSS_FEED_URLS`), aunque no está activo como feed por defecto. Tratarlo como "competidor" en el brief original es, con respeto, una categorización imprecisa — es más útil pensarlo como canal de distribución/lanzamiento y como fuente de datos, no como rival.

**Indie Hackers [no visitado — juicio informado, no observación directa]:** comunidad de fundadores, no un producto de detección de tendencias. Mismo caso que Product Hunt: relevante como canal de distribución y como lugar donde vive el ICP, irrelevante como competidor de producto.

**CB Insights [no visitado — juicio informado]:** herramienta de inteligencia de mercado de gama enterprise, con precios de miles de dólares/año y compradores corporativos (VCs, equipos de estrategia). No compite por el mismo comprador que AI Trend Hunter (indie hacker/fundador solo, 39€/mes) — es una referencia de "a qué categoría aspiras a llegar algún día", no un rival de conversión hoy.

**Ahrefs / Semrush [no visitados — juicio informado]:** herramientas SEO con módulos de tendencias de palabras clave como *feature secundaria*, no su producto principal. Interesante que Semrush haya comprado Exploding Topics — confirma que el propio Semrush considera "detección de tendencias" un mercado adyacente lo bastante valioso como para adquirirlo en vez de construirlo. Señal de mercado real, no de competencia directa hoy.

## 1.4 Tabla comparativa

| | **AI Trend Hunter** | **Exploding Topics** | **Glimpse** | **Trends.vc** |
|---|---|---|---|---|
| Propuesta de valor | Detectar oportunidades SaaS antes de que sean obvias | Detectar tendencias 12+ meses antes | Detectar tendencias antes de que exploten (vía datos de búsqueda) | Explorar nuevos mercados con una comunidad de fundadores |
| Entrada gratuita sin tarjeta | ❌ No existe | ✅ Explorador público completo | ✅ "IT'S FREE" | ✅ Informes gratis |
| Prueba con ejemplos reconocibles | ❌ Ejemplos ficticios ("Self-hosted LLM gateways") | ✅ Pickleball, Air Fryer, Perplexity AI | ✅ Notion, Canva, SHEIN, TikTok | ⚠️ No verificado en visita de hoy |
| Prueba social (logos/testimonios) | ❌ Ninguna | ✅ Google, McKinsey, Shopify, Goldman Sachs | ✅ Testimonio con nombre + cifras + 4.91★ | ✅ Product Hunt #1 + 54.782 fundadores con cara |
| Precio de entrada | 39€/mes, tarjeta requerida desde el día 1 | Freemium | Freemium | Freemium (contenido) → Pro de pago |
| Audiencia | Fundadores/indie hackers (declarado) | Marketers, marcas, analistas | Marketers, ecommerce, PR, analistas | Fundadores/indie hackers (igual que AI Trend Hunter) |
| Fuentes de datos | GitHub, Hacker News, RSS (coste marginal ~0) | Búsqueda web + redes | Búsqueda web masiva | Curación editorial |
| Dashboard visible antes de pagar | ❌ Mockup con datos falsos únicamente | ✅ Datos reales navegables | ✅ Datos reales navegables | ✅ Informes reales gratis |

**Conclusión de Fase 1:** AI Trend Hunter es la única de las cuatro que exige pago (con tarjeta) antes de mostrar una sola pieza de valor real. Esto no es una opinión de diseño — es una desviación estructural del estándar de toda su categoría, observada en el 100% de los competidores directos investigados.

---

# FASE 2 — Auditoría de fricción psicológica

No busco bugs (ya se hizo esa auditoría técnica días atrás). Busco por qué una persona racionalmente interesada decide no continuar.

## 2.1 Home (`aitrendhunter.app/`)

**[EVIDENCIA — código fuente]** El hero muestra un mockup de dashboard con datos **inventados y fijos en el código**: *"1,284 signals processed"*, *"142 Tracked trends +18"*, *"23 New this week +6"*, *"Avg. momentum +34%"*. Ningún texto cercano indica que sea una ilustración. El dashboard real de producción tiene ~20 tendencias activas hoy.

**Fricción psicológica:** esto no es solo "poco elegante" — genera un **riesgo de disonancia post-compra**. El cerebro humano ancla expectativas en la primera cifra grande que ve. Si alguien paga esperando el volumen del mockup y entra a un dashboard con una fracción de esos datos, la sensación no es neutra: es la de haber sido *engañado*, aunque nadie mintiera explícitamente por escrito. Es el tipo de micro-decepción que no genera una queja (nadie escribe "me prometisteis 142 tendencias") pero sí una cancelación silenciosa.

**[EVIDENCIA — código fuente]** Las tarjetas de "Sample output" usan ejemplos **ficticios**: "Self-hosted LLM gateways", "AI agents for QA testing", "AI compliance automation" — con scores y gráficas también inventados. Ningún visitante puede verificar si esa predicción fue real.

**Fricción psicológica:** contrasta directamente con el patrón de los tres competidores (Fase 1): ellos prueban su afirmación con hechos que el visitante ya puede confirmar por sí mismo (Pickleball, Notion, Substack). AI Trend Hunter pide **fe**, no ofrece **verificación**. Psicológicamente, pedir fe a un desconocido frío es la petición más cara que existe en un funnel — y aquí se pide en el primer scroll.

**[EVIDENCIA — código fuente]** La franja de "fuentes" lista seis elementos (GitHub, Hacker News, RSS feeds, Product changelogs, Release notes, Dev forums) cuando el producto real integra tres (GitHub, HN, RSS — los otros tres son subconjuntos de RSS). Un visitante técnico —el ICP declarado— es precisamente el tipo de persona que lee con atención y detecta esta clase de inflación.

**Fricción psicológica:** micro-pérdida de confianza acumulativa. Ninguna mentira grave, pero cada pequeña sobre-promesa detectada resta credibilidad a todo lo demás que dice la página, incluidas las afirmaciones que sí son ciertas.

**[EVIDENCIA — código fuente + observación de scroll]** La sección "Use cases" admite abiertamente que 2 de sus 4 casos dependen de funciones no construidas ("Keyword alerts coming soon", "PDF export coming soon").

**Fricción psicológica:** es honesto (no promete lo que no existe activamente), pero el efecto neto es que la mitad de la sección diseñada para generar deseo termina generando la sensación de "vuelve en unos meses" — exactamente lo contrario del efecto perseguido en un hero de conversión.

## 2.2 `/pricing` — el hallazgo central de este informe

**[EVIDENCIA — código fuente, `frontend/src/app/pricing/page.tsx`]** La navegación de esta página contiene únicamente el logo y un botón "View dashboard". No hay enlaces a "Why", "How it works", "Features" ni "Sample output" — el visitante que aterriza aquí (el 88,7% del tráfico de pago, ver Fase 3) no tiene, sin salir del flujo, ninguna vía visible para entender el producto más allá de:

> *"Detect emerging SaaS opportunities with public signals, trend scoring, and actionable briefs. No open free plan: a short trial to validate real value."*

Cinco bullets genéricos ("Emerging trends dashboard", "GitHub, Hacker News, and RSS as initial sources"...) y una tarjeta de pago.

**Fricción psicológica — esta es la fricción #1 de todo el funnel:** en psicología del consumidor esto se llama **"trust gap antes del compromiso"**. Pedir un método de pago (aunque sea "solo" un trial) exige que el visitante ya haya cruzado un umbral de confianza suficiente para asumir riesgo percibido (¿me cobrarán sin avisar? ¿podré cancelar fácilmente? ¿esto realmente funciona?). Esa confianza normalmente se construye en las páginas anteriores del funnel — pero el 88,7% del tráfico **nunca pasa por ellas**. Llegan directamente al punto de máxima exigencia de confianza con el mínimo de confianza acumulada. Es estructuralmente el peor sitio posible para aterrizar en frío.

**[EVIDENCIA — código fuente, `PricingCheckout.tsx`]** Mecánicamente, el formulario en sí es *bueno*: solo pide email, y delega la tarjeta a Stripe Checkout (una superficie de confianza reconocida). Esto descarta una hipótesis fácil pero incorrecta: **el problema no es "el formulario es largo o complicado".** El formulario es, de hecho, ejemplar. El problema es todo lo que falta *antes* del formulario, no el formulario mismo.

## 2.3 Onboarding / registro (login por código)

**[EVIDENCIA — código fuente]** El login es sin contraseña, por código de 6 dígitos enviado al email — patrón moderno, de baja fricción, correcto.

**[EVIDENCIA — dato de producción, hallado en auditorías previas de esta misma semana]** El remitente de esos emails sigue siendo `onboarding@resend.dev` (dominio de pruebas de Resend), no un dominio propio verificado.

**Fricción psicológica:** un email de "código de acceso" que llega desde un dominio que no es el tuyo activa, en el cerebro de cualquier usuario medianamente cauto, el mismo patrón de reconocimiento que un email de phishing — remitente desconocido pidiendo que se introduzca un código. Es plausible que **algunos de los pocos usuarios que sí llegan a pedir el código no confíen en el email y abandonen ahí**, aunque hoy no hay datos para confirmarlo (0 intentos de login reales por ahora, ver Fase 3).

## 2.4 Dashboard (tras pago)

**[EVIDENCIA — observación directa de sesiones anteriores esta semana]** El dashboard real es sólido: abre con "Best opportunity this week" totalmente narrado (mercado, competencia, urgencia, viabilidad, potencial, por qué ahora, quién compraría, MVP a construir, formas de monetizar, riesgos), seguido de shortlists rankeadas. Esto es, honestamente, **mejor que lo que cualquiera de los tres competidores directos enseña en su propio marketing** — ninguno de ellos muestra un brief tan completo y accionable en su home pública.

**La paradoja central de este informe:** el producto real es más fuerte que su propia página de ventas. AI Trend Hunter no tiene un problema de producto. Tiene un problema de **que nadie ve el producto antes de pagar por él.**

---

# FASE 3 — Customer journey (mapa psicológico, segundo a segundo)

**[EVIDENCIA — Plausible, 28 jul-2 ago]** Base real: de 47 visitantes de Facebook, el **88,7% entra directamente en `/pricing`** (no en la home). Solo 3 llegaron a `/login`, solo 3 a `/dashboard`. 0 trials creados en la base de datos.

### Recorrido real (el que ocurre hoy, para el 88,7%)

| Momento | Qué ve | Qué piensa | Qué siente | Qué le falta |
|---|---|---|---|---|
| 0-2s | Anuncio de Facebook → clic | "Vale, veamos qué es esto" | Curiosidad neutra | — |
| 2-4s | Llega a `/pricing`. Nav mínima, sin "Learn more" | "¿Ya estoy en la página de pago? ¿Y el producto?" | Ligera sorpresa/desorientación | Contexto |
| 4-10s | Lee: "Try AI Trend Hunter for 7 days" + una frase | "Vale, detecta oportunidades SaaS. ¿Cómo? ¿Con qué datos?" | Interés moderado, aún sin fricción grave | Una demostración |
| 10-15s | Lee los 5 bullets | "Esto podría ser útil, pero no veo *ningún* ejemplo" | Duda empieza a aparecer | Prueba, no promesas |
| 15-20s | Ve la tarjeta de pago: 39€/mes, "First charge after the 7-day trial" | "Me están pidiendo la tarjeta sin haberme enseñado nada" | **Fricción de confianza — el momento crítico** | Reducir el riesgo percibido |
| 20-25s | Busca instintivamente "¿hay una demo? ¿un ejemplo? ¿opiniones?" | No encuentra nada de eso en esta página | Frustración leve, sensación de vacío | Cualquiera de las 3 pruebas de la Fase 1 |
| 25-30s | Decisión | "Mejor me lo pienso" / cierra la pestaña | Abandono silencioso, sin señal negativa explícita (no hay queja, no hay error — simplemente se va) | — |

**[HIPÓTESIS, con evidencia parcial de apoyo]** El patrón de "3 de 47 llegaron a `/login`" sugiere que existe un subconjunto pequeño pero real de visitantes con **intención ya alta antes de hacer clic en el anuncio** (quizá porque ya conocían el concepto, o el copy del propio anuncio les convenció del todo) — y que ESOS sí toleran la falta de prueba en `/pricing` porque no la necesitaban. El 85% restante sí la necesitaba y no la encontró. Esto es coherente con la fricción identificada, pero no está confirmado con entrevistas reales — validar hablando con esos 3 usuarios si es posible identificarlos, o con las próximas semanas de tráfico.

### Recorrido del 11,3% que sí ve la home primero

Aquí el journey es más largo pero more informativo — y termina en el mismo sitio: la home no tiene botón de compra sin fricción visible hasta que se hace scroll largo, así que quien empieza en la home y quiere probar el producto también termina, tarde o temprano, en la misma `/pricing` desnuda. La home añade contexto, pero no cierra el journey — solo lo aplaza.

---

# FASE 4 — Psicología del producto

**¿Qué compra realmente el cliente? [HIPÓTESIS fundamentada]** No compra "datos". Compra **una reducción de la ansiedad de estar construyendo lo equivocado**. El comprador de este producto (fundador solo, indie hacker) vive con una duda de fondo constante: *"¿y si dedico los próximos 6 meses a algo que nadie quiere?"* AI Trend Hunter vende alivio de esa ansiedad, no un dashboard.

**¿Qué problema cree que resuelve?** "Encontrar ideas de producto." (superficial, es lo que dice el copy)

**¿Qué problema resuelve realmente?** Reduce el coste de oportunidad de una mala decisión de producto — pero **esto nunca se dice explícitamente en ningún sitio del funnel actual**. El copy vende el mecanismo (señales públicas → scoring → briefs) en vez de vender el alivio emocional. Es un error clásico de producto técnico vendido por técnicos: se explica el *cómo* mejor que el *por qué me importa*.

**Emociones que aparecen en el journey real:**
- Curiosidad (al hacer clic en el anuncio) → **[EVIDENCIA]** el CTR de 1,27-1,70% y CPC de 0,28€ son saludables, confirman que el anuncio genera curiosidad real.
- Duda (al no encontrar prueba) → **[HIPÓTESIS]**, coherente con el patrón de abandono observado.
- Ninguna emoción de "WOW" — porque no hay ningún momento diseñado para provocarla antes del pago (ver Fase 6).

**Qué genera confianza (en la categoría, según competidores):** nombres reconocibles, cifras verificables, caras humanas, exploración gratuita.
**Qué genera confianza hoy en AI Trend Hunter:** nada de lo anterior está presente en `/pricing`.
**Qué genera miedo:** pedir la tarjeta sin haber demostrado nada es, literalmente, el patrón superficial de una estafa de suscripción — no porque lo sea, sino porque el cerebro no distingue intención, solo patrones. "Trial pide tarjeta + no hay prueba visible" activa el mismo circuito de alerta que un dark pattern, aunque aquí no lo haya (el propio código confirma cobro solo tras el trial, cancelación fácil vía Stripe).
**Qué genera curiosidad:** el propio dashboard real, que nadie ve antes de pagar.

---

# FASE 5 — Propuesta de valor: análisis crítico

**¿Es clara?** **[EVIDENCIA]** Sí, a nivel de mecanismo: "detecta oportunidades SaaS emergentes antes de que sean obvias, con GitHub/HN/RSS." Se entiende en menos de 10 segundos qué *hace*.

**¿Es memorable?** **[HIPÓTESIS]** No especialmente. "Detect emerging SaaS opportunities before they're obvious" es correcta pero intercambiable — Exploding Topics dice casi lo mismo con más fuerza ("12+ Months Before Everyone Else"). No hay una frase ancla que sobreviva 24 horas en la memoria de quien la lee.

**¿Es diferente?** **[EVIDENCIA de Fase 1]** Sí, y esto es importante no perderlo: AI Trend Hunter es el único de los cuatro analizados que basa su señal en **actividad de desarrolladores** (repos, commits, hilos técnicos) en vez de en volumen de búsqueda de consumidores. Para el ICP de fundador técnico, señal temprana desde GitHub es, argumentablemente, *más* temprana que señal de búsqueda (la gente busca después de que el producto ya existe y tiene tracción; el código se escribe antes). **Esta diferenciación real casi no se explota en el copy actual** — se menciona como lista de fuentes, no como argumento de superioridad temporal.

**¿Es defendible?** **[HIPÓTESIS, con matices]** El coste marginal casi cero (heurísticas, sin LLM) es una ventaja de negocio real y ya documentada internamente, pero no es una ventaja *defendible frente al cliente* — al cliente no le importa tu margen, le importa el resultado. La verdadera defendibilidad a largo plazo sería la calidad acumulada del scoring con el tiempo, que hoy es demasiado joven para demostrarse.

**¿Se entiende en menos de 10 segundos?** Sí, en la home. **No, en `/pricing`** — ahí se entiende el *precio* en 10 segundos, pero no el *valor*, porque no hay prueba, solo afirmación.

---

# FASE 6 — Efecto WOW

**¿Cuándo aparece hoy?** **[EVIDENCIA]** Solo después de: clic en anuncio → llegar a `/pricing` → dar el email → completar el pago en Stripe → recibir un email de un dominio no verificado → pedir un código → iniciar sesión → llegar al dashboard. El WOW real del producto (el brief de "Best opportunity this week", completo y accionable) existe — pero está enterrado al final de una cadena de al menos 6-7 pasos de fricción y compromiso económico.

**¿Cuándo debería aparecer?** En los primeros 10 segundos de `/pricing`, o antes. El WOW no puede vivir exclusivamente detrás del muro de pago si el objetivo es convertir tráfico frío.

**¿Qué debería provocar?** La misma reacción que genera ver "Pickleball — DISCOVERED 4.9 years ago" en Glimpse: *"espera... esto realmente lo habría visto venir"*. Es un WOW de **verificación retroactiva**, el más barato de producir (no requiere IA nueva, requiere elegir 3-5 ejemplos históricos reales de tu propio dataset y contar la historia).

**Cómo conseguirlo — ejemplos de otros SaaS:**
- **Notion / Figma:** WOW mediante plantilla o archivo de ejemplo real interactivo antes de pedir cuenta.
- **Loom:** WOW mediante un vídeo de ejemplo ya grabado, cero fricción, en la home.
- **Superhuman:** WOW retrasado deliberadamente, pero compensado con onboarding 1:1 humano — modelo caro, no aplicable aquí a esta escala.
- **Los tres competidores de Fase 1:** WOW mediante "reconocimiento" (ver una tendencia que ya conoces, marcada como detectada temprano) — el patrón más replicable y barato para AI Trend Hunter dado que ya tiene datos reales de GitHub/HN acumulados.

---

# FASE 7 — Puntos de fuga, ordenados

Sin modificar código, solo razonamiento sobre lo observado. Escala: Probabilidad / Impacto / Facilidad de solución (Alta/Media/Baja).

| # | Punto de fuga | Prob. | Impacto | Facilidad |
|---|---|---|---|---|
| 1 | `/pricing` sin ninguna prueba de valor antes de pedir pago | **[EVIDENCIA]** Alta | Alto | Media (contenido, no rediseño) |
| 2 | Sin ejemplos verificables/reconocibles (todo es ficticio) | **[EVIDENCIA]** Alta | Alto | Media (requiere elegir casos reales del propio histórico) |
| 3 | Sin prueba social de ningún tipo (logos, testimonios, cifras de usuarios) | **[EVIDENCIA]** Alta | Medio-Alto | Baja al principio (no hay usuarios aún que dar como testimonio — ver Fase 9) |
| 4 | Pedir tarjeta sin exploración gratuita previa | **[HIPÓTESIS bien fundamentada]** Media-Alta | Alto | Alta (mecánicamente ya existe el checkout; falta la puerta gratuita antes) |
| 5 | Mockup de dashboard con cifras infladas vs. realidad | **[EVIDENCIA]** Media | Medio (a largo plazo, vía cancelaciones tempranas) | Alta (cambiar 4 números) |
| 6 | Email de login desde dominio no verificado | **[EVIDENCIA de config]** Baja-Media (solo afecta a quien ya llegó tan lejos) | Medio | Media (ya identificado como deuda técnica previa) |
| 7 | Posibles vacíos de scroll en la home (hallazgo de ayer) | **[HIPÓTESIS, con caveat de método]** Baja-Media | Medio | Media |
| 8 | Value prop memorable pero no diferenciada frente a Exploding Topics/Glimpse | **[HIPÓTESIS]** Media | Medio | Media (es un ejercicio de copy, no de producto) |

---

# FASE 8 — Hipótesis completas

### H1 — Falta de prueba de valor en `/pricing` es la causa dominante
- **Explicación:** el visitante frío no tiene forma de verificar la promesa antes de asumir riesgo de pago.
- **Evidencia:** 88,7% del tráfico entra por ahí; 0 conversiones; código confirma ausencia total de prueba en esa página; los 3 competidores directos resuelven esto explícitamente.
- **Probabilidad:** Alta.
- **Impacto si se corrige:** Alto — es la hipótesis con mayor apalancamiento porque afecta al mayor volumen de tráfico.
- **Cómo validarla:** añadir 2-3 elementos de prueba (ejemplo real, cifra, o testimonio si existe) a `/pricing` y medir conversión trial en las siguientes 2 semanas al mismo volumen de tráfico.
- **Cómo descartarla:** si tras añadir prueba de valor la conversión sigue en 0 con volumen comparable, la causa está en otro sitio (precio, ICP del anuncio, o producto).

### H2 — El precio con tarjeta upfront sin capa gratuita es una barrera estructural
- **Explicación:** en una categoría donde el 100% de los competidores directos ofrece entrada gratuita, pedir tarjeta de entrada puede sentirse fuera de norma.
- **Evidencia:** patrón unánime en Fase 1; sin datos propios de A/B que lo confirmen.
- **Probabilidad:** Media-Alta.
- **Impacto:** Alto, pero requiere decisión de negocio (no solo de copy) — afecta directamente al modelo de monetización.
- **Cómo validarla:** ofrecer una versión mínima gratuita (ej. ver el top-5 de la semana sin login) y medir si sube la tasa de email capturado / intención.
- **Cómo descartarla:** si se lanza una capa gratuita y no mueve ni el tráfico a `/login` ni las conversiones, la barrera no era el precio de entrada.

### H3 — El anuncio atrae la intención correcta, pero el mensaje del anuncio y el de `/pricing` no coinciden en tono/expectativa
- **Explicación:** no he auditado la creatividad exacta del anuncio en este informe; si promete algo distinto a lo que `/pricing` entrega, generaría el mismo efecto.
- **Evidencia:** ninguna directa en este documento — **es una hipótesis abierta que Fase 1 no cubrió** y que debería auditarse por separado.
- **Probabilidad:** Baja-Media (el CPC y CTR sanos sugieren que el anuncio comunica bien su promesa, pero no descarta un desajuste con la página de aterrizaje).
- **Cómo validarla:** comparar textualmente el copy del anuncio activo con el copy de `/pricing`.

### H4 — El volumen de tráfico (84 visitas) es simplemente insuficiente para esperar conversiones todavía
- **Explicación:** con un funnel sano de doble dígito bajo de porcentaje, 84 visitas puede no ser estadísticamente suficiente para esperar ni una sola conversión.
- **Evidencia:** cierto en términos puramente estadísticos — pero no explica por qué **ni siquiera hay intentos fallidos de checkout** ni un solo email introducido en el formulario de pricing (dato a confirmar con Plausible/eventos `Checkout Started`).
- **Probabilidad:** Media como explicación *parcial*, Baja como explicación *única* — porque no compite con H1, la complementa. Incluso con poco volumen, cabría esperar *algún* intento de checkout si la página generara suficiente confianza para probar.
- **Cómo validarla/descartarla:** revisar en Plausible cuántos eventos `Checkout Started` existen (el código ya trackea esto en `PricingCheckout.tsx`). Si el número es 0, refuerza H1 (nadie ni lo intenta). Si hay varios intentos fallidos, la causa está en el checkout técnico o en el precio en el último paso, no en la falta de confianza previa.

### H5 — El precio de 39€/mes es percibido como alto para el nivel de confianza generado
- **Explicación:** el precio en sí no es descabellado para la categoría, pero percepción de precio es relativa a la confianza acumulada — el mismo precio se siente "razonable" con prueba social y "caro" sin ella.
- **Evidencia:** ninguna directa; es coherente con H1 pero no independiente de ella.
- **Probabilidad:** Media, mayormente como síntoma de H1 más que como causa propia.
- **Cómo validarla:** difícil de aislar sin resolver H1 primero; un test de precio antes de resolver la confianza contaminaría la lectura del experimento.

---

# FASE 9 — Plan Phoenix (roadmap)

## Qué cambiar primero (0-2 semanas, máximo apalancamiento, mínimo esfuerzo)

1. **Añadir 3-5 ejemplos reales y verificables a `/pricing` y a la home**, sustituyendo los ficticios. Usar tendencias reales ya detectadas por el propio pipeline en las últimas semanas que hoy resulten fáciles de reconocer o explicar (aunque no sean "famosas" como Pickleball, sí pueden mostrarse con su fecha real de detección — la honestidad del dato es el punto, no la fama del ejemplo).
2. **Corregir el mockup del hero** para que sus cifras coincidan con el volumen real actual, o etiquetarlo explícitamente como ilustrativo.
3. **Añadir un enlace de contexto en la nav de `/pricing`** ("¿Cómo funciona?" hacia la home) — coste de implementación mínimo, cierra el vacío más evidente del journey del 88,7%.
4. **Verificar el dato de `Checkout Started`** en Plausible (ya instrumentado) para confirmar o descartar H4 antes de gastar más presupuesto de campaña.

## Qué cambiar después (2-6 semanas, requiere más diseño/decisión)

5. **Diseñar una capa de exploración gratuita** (aunque sea limitada: top-3 de la semana visible sin cuenta) — valida H2 sin comprometer el modelo de negocio de raíz.
6. **Reescribir el copy de propuesta de valor** para vender el alivio emocional (Fase 4), no solo el mecanismo — probar 2-3 variantes de titular.
7. **Verificar dominio de email propio** para Resend (deuda ya identificada, ahora con justificación de conversión, no solo de imagen).
8. **Auditar el copy exacto del anuncio de Meta** contra el copy de `/pricing` (cierra H3).

## Qué nunca cambiaría (fortalezas reales a proteger)

- El checkout técnico (email → Stripe) — es de los mejores elementos de todo el funnel, no tocar.
- El coste marginal casi nulo del motor de detección — ventaja de negocio real, no sacrificarla por presión de "hacerlo más impresionante" con IA cara.
- La honestidad de no prometer features que no existen ("coming soon") — es un valor correcto; el problema no es la honestidad, es la ausencia total de prueba en positivo.
- El propio dashboard post-pago — es más fuerte que su marketing; no hace falta rehacerlo, hace falta enseñarlo antes.

## Qué debe esperar

- Cualquier rediseño visual completo de la home — el problema no es estético, es de contenido/prueba. Rediseñar ahora sería resolver el síntoma equivocado.
- Añadir más fuentes de datos o features nuevas — no hay evidencia de que el producto necesite ser "más grande"; necesita ser *demostrado*.
- Experimentos de precio — contaminarían la lectura mientras H1 siga sin resolver.

## Experimentos a ejecutar y cómo medir éxito

| Experimento | Métrica | Criterio de éxito |
|---|---|---|
| Añadir prueba real a `/pricing` | `Checkout Started` / visitas a `/pricing` | Al menos 1 intento de checkout cada ~30-40 visitas (referencia: la mayoría de landing pages SaaS con confianza sana rondan 3-8% de intención de checkout; hoy es 0%) |
| Capa gratuita de exploración | Visitas a `/dashboard` sin cuenta / visitas a `/pricing` | Movimiento medible en intención, aunque no convierta aún a pago |
| Nuevo copy de propuesta de valor | Tiempo en página + scroll depth en `/pricing` | Aumento frente a la línea base actual |

---

# FASE 10 — Recomendación ejecutiva

Si yo fuera la CPO contratada por un fondo para rescatar esto:

## Próximos 30 días
Resolver H1 en su totalidad antes de tocar cualquier otra cosa. Es barato, es rápido, y es la única hipótesis que explica el 100% del patrón observado (mucho tráfico de calidad, cero fricción técnica, cero conversión). No subiría el presupuesto de la campaña ni un euro hasta no haber corregido `/pricing` — cada euro adicional hoy compra más visitas al mismo agujero.

## Próximos 90 días
Con H1 resuelta y midiendo resultado real, decidir con datos si hace falta una capa gratuita (H2). Empezar a construir prueba social genuina: los primeros 5-10 clientes de pago, aunque sean pocos, dan testimonios reales que valen más que cualquier copy. Reescribir la propuesta de valor around el alivio emocional, no el mecanismo técnico.

## Qué NO haría
No tocaría el precio todavía — cambiar precio sin confianza resuelta es adivinar a ciegas. No invertiría en una segunda campaña o canal nuevo mientras el primero siga sin convertir — el problema no es de alcance, es de conversión en el punto de aterrizaje. No construiría features nuevas — el producto ya es mejor que su propio marketing.

## Riesgos que veo
- **Riesgo de agotamiento de caja de marketing sin aprendizaje:** seguir gastando en el canal actual sin arreglar `/pricing` quema presupuesto sin generar ni señal de aprendizaje útil (0 conversiones no enseña nada sobre optimización de creatividad o audiencia).
- **Riesgo de sobrecorrección:** después de leer este informe, la tentación será rediseñar toda la landing de golpe. Eso perdería la trazabilidad de qué cambio realmente movió la aguja.
- **Riesgo de que H1 no sea suficiente por sí sola:** aunque la evidencia es fuerte, sigue siendo una hipótesis hasta que se mida con tráfico nuevo. Hay que estar dispuesto a que el resultado no sea el esperado y pasar a H2/H3 sin apego emocional a la primera teoría.

## Oportunidades que veo
- **AI Trend Hunter tiene una diferenciación real y sin explotar:** señal desde código fuente, no desde búsqueda de consumo. Es un ángulo genuinamente distinto de los tres competidores directos y casi no se usa hoy en el mensaje.
- **El coste marginal casi nulo permite ofrecer una capa gratuita sin miedo al coste variable** — algo que muchos competidores con infraestructura más cara no pueden regalar tan barato.
- **El producto post-pago ya es competitivo, incluso superior en algunos aspectos** (el brief de oportunidad es más completo que lo que muestra públicamente cualquiera de los tres rivales) — el trabajo pendiente es de distribución de esa prueba, no de construcción de más producto.

---

*Fin de la Fase 1 del Proyecto Phoenix. Este documento es la base de decisión; ninguna de sus recomendaciones se ha implementado todavía — a la espera de tu validación como CEO antes de tocar código, siguiendo el proceso de decisión ya establecido en `/governance/07_DECISION_FRAMEWORK.md`.*
