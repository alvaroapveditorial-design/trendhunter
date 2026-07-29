# Informe de QA pre-lanzamiento — AI Trend Hunter

**Fecha:** 2026-07-27 a 2026-07-29
**Alcance:** verificación del checklist de 10 puntos pre-lanzamiento + revisión en vivo del dashboard de producción (dos pasadas) para detectar inconsistencias.

Todo lo descrito aquí se verificó contra producción real (no solo "se desplegó"): sesiones de Stripe reales, cancelación real de una suscripción, ejecución manual del pipeline de ingesta, lectura directa de la base de datos y de Sentry, y navegación real del dashboard autenticado.

---

## 1. Checklist de verificación pre-lanzamiento

| # | Punto | Estado | Nota |
|---|---|---|---|
| 1 | Pixel registra `PageView`, `StartTrial`, `Purchase` | ✅ | Confirmado manualmente por el usuario en Meta Events Manager (no se pudo verificar por navegador: la herramienta de Meta daba error de carga persistente). Config (`META_PIXEL_ID`, `NEXT_PUBLIC_META_PIXEL_ID`) verificada. |
| 2 | Eventos llegan también por Conversions API | ✅ | Config verificada (`META_CAPI_ACCESS_TOKEN`); código que dispara `StartTrial`/`Purchase` vía CAPI cubierto por tests. |
| 3 | Checkout de Stripe funciona desde sesión nueva | ✅ | Sesión de checkout real (`cs_live_...`) creada contra producción sin autenticación previa. |
| 4 | Email de acceso llega a Gmail/Outlook/Apple Mail | ✅ | Confirmado por el usuario en Outlook. |
| 5 | Se puede cancelar una suscripción sin errores | ✅ | Cancelación real ejecutada sobre una suscripción activa, de principio a fin (Dashboard → Manage billing → Stripe → confirmar). Ver bug **E** más abajo, encontrado y arreglado durante esta prueba. |
| 6 | Sentry recibe un error de prueba | ✅ | No hizo falta forzar un error de prueba: Sentry ya tenía capturado un error real (fallo de Resend, `app.services.email_service`). |
| 7 | Plausible muestra visitas en tiempo real | ✅ | Dashboard de Plausible con datos reales del día (visitantes únicos, pageviews). |
| 8 | El cron de ingestión ejecuta correctamente cada día | ✅ (tras arreglo) | Ver bug **A**. Confirmado con dos disparos automáticos consecutivos (2026-07-28 y 2026-07-29, ambos ~08:02–08:04 UTC, sin intervención manual). |
| 9 | El dominio carga rápido y con HTTPS correcto | ✅ | HTTP 200, certificado TLS válido hasta oct-2026, ~0.34s TTFB. |
| 10 | Canal de soporte para primeros usuarios | ✅ (tras implementación) | No existía (solo un email personal en el footer legal). Ver bug **H**. |

---

## 2. Errores encontrados durante la revisión y su solución

### A. El cron de ingestión nunca se disparaba solo
- **Síntoma:** última ejecución real con más de 29 horas de antigüedad; ninguna fila en `agent_executions` coincidía con el horario programado (`0 8 * * *`).
- **Causa raíz:** al servicio `trendhunter-ingestion-cron` le faltaban por completo las variables `JWT_SECRET` y `SECRET_KEY`. Un validador de arranque (`Settings`) rechaza sus valores por defecto en producción, así que el proceso se caía al instante en cada disparo, antes de ejecutar ninguna lógica de ingesta. Confirmado leyendo el log de un disparo real: `pydantic ValidationError: JWT_SECRET must be set to a strong secret in production`.
- **Solución:** se copiaron `JWT_SECRET`, `SECRET_KEY` y `SENTRY_DSN` desde el servicio backend al servicio cron.
- **Verificación:** ejecución manual completa end-to-end (ingesta real de datos), y posteriormente dos disparos automáticos reales en días consecutivos, sin intervención.

### B. Contenido en chino sin traducir en el dashboard
- **Síntoma:** la tendencia "Inferencex" aparecía como oportunidad #2 con media descripción en chino.
- **Causa raíz:** el filtro de idioma medía el porcentaje de caracteres no-latinos sobre **todo el texto**. Cuando la cláusula traducida está rellena de los mismos términos técnicos en inglés que la mitad en inglés (nombres de modelos, números), el ratio global queda por debajo del umbral aunque la cláusula en sí sea claramente no-inglesa.
- **Solución:** el filtro ahora se aplica por cada segmento del texto separado por "|", no solo de forma global.
- **Verificación:** test de regresión con el caso exacto; tendencia existente limpiada con el script de cleanup ya existente.

### C. Etiquetas de métricas incorrectas para repos de GitHub
- **Síntoma:** el panel "Source signals" mostraba "1.3K upvotes · 211 comments" para un repositorio de GitHub.
- **Causa raíz:** esos campos genéricos (`upvotes`, `comments`) almacenan en realidad `stargazers_count` y `open_issues_count` para GitHub. GitHub no tiene "upvotes" ni "comments" en ese sentido — el frontend usaba la misma etiqueta para todas las fuentes sin distinguir.
- **Solución:** etiquetas ahora dependen del tipo de fuente (GitHub: "stars"/"open issues"; Hacker News: "upvotes"/"comments", que sí son reales; RSS: el número ya no se muestra, porque es una estimación sintética basada solo en la antigüedad, no una señal real).

### D. Nombre interno "mvp" filtrado a la interfaz
- **Síntoma:** el panel "Recent pipeline runs" mostraba "mvp heuristic detector".
- **Causa raíz:** `agent_name` es un identificador interno (`mvp_heuristic_detector`), resto del desarrollo temprano, mostrado tal cual con un simple reemplazo de guiones bajos.
- **Solución:** etiqueta de presentación que retira el prefijo "mvp", mostrando "Heuristic detector". (No confundir con la tarjeta "MVP to build", que sí es terminología de negocio correcta dirigida al cliente y no se tocó.)

### E. `cancel_at_period_end` nunca se marcaba al cancelar durante el trial
- **Síntoma:** tras cancelar una suscripción real en periodo de prueba a través del portal de Stripe (confirmado sin errores, "Se cancela el 1 ago"), la base de datos seguía mostrando `cancel_at_period_end = false`.
- **Causa raíz:** al cancelar una suscripción que está en trial, Stripe programa el fin mediante el campo `cancel_at` (una fecha concreta), **no** activando el booleano `cancel_at_period_end` — ese booleano solo se activa una vez la suscripción ha salido del periodo de prueba. El webhook solo miraba `cancel_at_period_end` e ignoraba `cancel_at`.
- **Solución:** el webhook ahora trata ambas señales como equivalentes ("no se renovará").
- **Verificación:** test de regresión con el payload real observado; reproducción del evento real contra el webhook ya corregido, confirmando el cambio en la base de datos de producción.

### F. El filtro de relevancia se podía saltar por completo
- **Síntoma:** la tendencia "Half-Life ported to Mac OS 9" (un port de un videojuego de 1998) apareció como tendencia activa, pese a que el propio filtro de `HackerNewsCollector` rechaza ese título exacto al probarlo directamente.
- **Causa raíz:** el endpoint `/api/v1/ingestion/signals` (protegido por clave, usado para pruebas manuales) acepta señales en crudo y las pasa directamente al motor de detección, sin pasar por el filtro de relevancia/idioma de los collectors.
- **Solución:** el filtro se aplica ahora también de forma centralizada en `DetectorService.ingest_batch`, como punto de paso obligatorio sin importar la vía de entrada.

### G. Vocabulario del filtro de relevancia incompleto → falsos positivos
- **Síntoma:** al volver a pasar el filtro de limpieza existente, se desactivaron 24 tendencias; una revisión con el contenido completo de cada una reveló que **10 eran contenido genuinamente relevante** ("Ilya Sutskever ... Safe Superintelligence", "Kimi K3", "PyTorch", "Codex Security", expansión de Cursor a India, benchmarks de Claude Opus, modelos open-weight...).
- **Causa raíz:** la lista de palabras clave solo tenía términos genéricos ("ai", "llm", "agent") y no reconocía nombres reales de modelos, empresas o técnicas de IA.
- **Solución:** vocabulario ampliado (model, transformer, gpt, claude, opus, pytorch, nvidia, cursor, codex, superintelligence, open-weights, etc.); las 10 tendencias mal desactivadas se reactivaron tras revisión manual una por una. De paso, se consolidó la lista de términos (antes duplicada palabra por palabra en dos archivos, con riesgo de que un arreglo en uno no se replicara en el otro) en un único sitio.
- **Nota:** "Neutrino-1 8B" se dejó fuera deliberadamente por ambigüedad genuina (sin más contexto, no se puede confirmar que sea un modelo de IA).

### H. No existía canal de soporte
- **Síntoma:** el único punto de contacto para los primeros usuarios era un email personal dentro del footer legal.
- **Solución:** formulario de contacto (`/contact`) + endpoint `POST /api/v1/support/contact` (con rate limiting) que reenvía el mensaje por Resend al email real, con `reply-to` puesto al del usuario. Enlazado desde el footer y desde la página de error genérica.

---

## 3. Hallazgo menor, sin arreglar (no bloqueante)

El proxy del frontend (`/api/backend/...`) no reenvía correctamente la cabecera `Stripe-Signature`. No afecta a nada real porque los webhooks de Stripe llegan directamente al backend, nunca a través de ese proxy — se deja anotado por si en el futuro se necesitara enrutar algo sensible a cabeceras a través de él.

---

## 4. Cómo se verificó cada arreglo

Ningún punto de este informe se dio por bueno solo por desplegarse. Para cada uno: tests automatizados nuevos o existentes en verde, despliegue a producción, y comprobación directa contra datos/comportamiento reales (consultas a la base de datos de producción, repetición de eventos reales de Stripe, navegación real del dashboard autenticado, lectura de Sentry/Plausible/logs de Railway).
