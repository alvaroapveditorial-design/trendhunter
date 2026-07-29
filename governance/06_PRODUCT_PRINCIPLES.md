# 06 — Product Principles

**AI Trend Hunter · Principios oficiales de producto**
Versión 1.0 · Julio 2026 · Propietario: CPO · Custodio final: CEO

Estos principios existen para decidir en los momentos en que los datos no bastan. No son aspiraciones: son reglas de decisión. Cuando dos opciones empatan en la puntuación de [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md), gana la que mejor respete estos principios. Son 16 — deliberadamente menos de 20: una lista que no cabe en la cabeza no gobierna nada.

---

### 1. No construimos dashboards. Construimos decisiones.
El usuario no paga por mirar datos; paga por saber qué hacer a continuación. Cada pantalla debe responder "¿y ahora qué?". Si una vista informa pero no orienta, está incompleta. Por eso el producto abre con *una* mejor oportunidad y su brief de acción, no con una parrilla de gráficas.

### 2. No vendemos datos. Vendemos claridad.
Los datos son la materia prima, no el producto. Nuestra competencia real es el ruido: HN, Twitter, newsletters. Ganamos cuando el usuario obtiene en 5 minutos lo que le costaría 5 horas de lectura dispersa. Añadir información sin añadir claridad es empeorar el producto.

### 3. La señal es sagrada.
Un solo elemento basura visible (contenido irrelevante, otro idioma, un dato mal etiquetado) cuesta más confianza que la que ganan diez features. La calidad del filtrado es la feature número uno para siempre, y su presupuesto de mantenimiento no se recorta jamás.

### 4. Antes de que sea obvio.
Nuestra razón de existir es la anticipación. Un proyecto con 50.000 estrellas no es una oportunidad: es historia. Todo cambio en scoring, fuentes o filtros se evalúa con esta vara: ¿nos hace más tempranos o más tardíos? (Esta es la razón del rango de estrellas acotado en la búsqueda de GitHub.)

### 5. Honestidad radical con los números.
Ningún número sintético disfrazado de real. Si es una estimación, se etiqueta o no se muestra. Si la muestra es pequeña, se dice. Las etiquetas dicen exactamente lo que el número es ("stars", no "upvotes"). Un usuario que duda de un dato nuestro duda de todos.

### 6. El producto de hoy, no el de mañana.
El marketing describe lo que existe. Lo que no existe se llama "coming soon" o no se menciona. Ya aprendimos esta lección con una landing que prometía alertas y exports inexistentes: la corrección costó menos que la confianza que habría costado no corregirla.

### 7. Coste marginal cero como principio de diseño.
Cada cliente nuevo debe costar céntimos, no euros. Las heurísticas baratas y transparentes van antes que los modelos caros y opacos. Cualquier feature con coste variable por cliente necesita una justificación extraordinaria. El margen es una decisión de producto, no solo de finanzas.

### 8. Semanal por diseño.
El ritmo natural del producto es la semana: los datos se renuevan a diario, pero la decisión del usuario ("¿qué persigo ahora?") es semanal. No perseguimos DAU: perseguimos que cada semana el usuario encuentre algo que justifique la siguiente. Las métricas y las features se diseñan a ese compás.

### 9. Una pantalla, una decisión.
Jerarquía siempre: primero lo más importante, con diferencia visual clara. La paridad visual entre lo crítico y lo secundario es una decisión no tomada que se le traslada al usuario. Cuando todo destaca, nada destaca.

### 10. Menos, terminado, verificado.
Preferimos una feature completa, desplegada y verificada en producción antes que tres a medias. "Casi listo" no existe: existe listo (verificado con datos reales) y no listo. Lo demás es inventario.

### 11. Eliminar es construir.
Cada feature tiene coste perpetuo: mantenimiento, superficie de bug, carga cognitiva del usuario. Eliminamos sin nostalgia lo que los datos condenan ([04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §9-10). El coste hundido no vota. Un producto que solo crece en features es un producto que nadie está cuidando.

### 12. La confianza se construye en los detalles aburridos.
El email que llega al inbox, el error que explica qué hacer, la cancelación sin fricción, el dato correcto tras el filtro. Nadie tuitea sobre estos detalles, pero deciden si el cliente se queda. La fontanería impecable *es* el producto premium.

### 13. Instrumentado o no existe.
Toda feature nace con sus eventos de medición. Lo que no se mide no puede defenderse en la auditoría trimestral, y lo indefendible se elimina. Corolario: no construimos instrumentación nueva mientras no explotemos la existente.

### 14. El usuario avanzado no manda.
Escuchamos a todos, pero diseñamos para el usuario que entra, decide y se va. Las peticiones de power users (más filtros, más columnas, más configuración) se evalúan con doble escepticismo: suelen pedir complejidad que el 95% pagará en confusión.

### 15. Sin promesas de futuro en la venta.
Vendemos el valor de esta semana, no el roadmap. Un roadmap público es una deuda que otros gestionan. Si el producto de hoy no justifica 39 €/mes, la solución es mejorar el producto, no prometer el de dentro de seis meses.

### 16. La distribución es parte del producto.
Un gran producto que nadie descubre no es un gran producto: es un hobby caro. En fase de validación, el canal (anuncios, landing, funnel) recibe el mismo rigor de diseño, medición e iteración que el dashboard. El funnel *es* producto.

---

## Uso de estos principios

- **En decisiones:** cuando una discusión de producto se estanque, se recorre la lista y se cita el principio aplicable por número. Si ningún principio aplica, la decisión es genuinamente abierta y decide la puntuación de [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md).
- **En reviews:** un cambio que viola un principio se señala con el número ("esto rompe el §5: ese número es una estimación sin etiquetar").
- **Evolución:** los principios se revisan una vez al año o tras un cambio de estrategia ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §10). Cambiarlos exige decisión del CEO en Consejo. Máximo absoluto: 20. Para añadir el 17º hay que estar dispuesto a defender por qué no se fusiona con otro.
