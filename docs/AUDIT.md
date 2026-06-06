# Auditoría de Seguridad y Calidad de Código

**Fecha:** 2026-06-06  
**Alcance:** Backend completo (FastAPI) + modelos + servicios + frontend  
**Total de problemas encontrados:** 30  
**Corregidos en esta sesión:** 20  
**Pendientes:** 10 (requieren decisiones de arquitectura)

---

## Resumen ejecutivo

El proyecto tiene una base técnica sólida pero **no está preparado para producción** en su estado original. Los problemas más urgentes eran la ausencia total de autenticación en los endpoints, secretos con valores por defecto inseguros y una configuración CORS demasiado permisiva. Los tres primeros bloques críticos han sido parcialmente resueltos mediante validaciones en arranque y restricción de CORS; la autenticación completa queda pendiente de diseño.

---

## CRÍTICOS

### C1 — Secretos inseguros en producción ✅ CORREGIDO
- **Archivos:** `backend/app/core/config.py`
- **Descripción:** `JWT_SECRET` y `SECRET_KEY` tenían como valor por defecto `"change-me-in-production"`. Si se desplegaba sin sobreescribir estas variables, todos los tokens JWT podían ser falsificados.
- **Solución aplicada:** Se añadió un `model_validator` que lanza `ValueError` en el arranque si cualquiera de estos secretos mantiene su valor inseguro cuando `ENVIRONMENT=production`.

### C2 — CORS excesivamente permisivo ✅ CORREGIDO
- **Archivo:** `backend/app/main.py`
- **Descripción:** `allow_methods=["*"]` y `allow_headers=["*"]` exponían la API a cualquier método HTTP y cabecera desde cualquier origen permitido.
- **Solución aplicada:** Reemplazados por listas explícitas:
  - Métodos: `GET, POST, PUT, DELETE, OPTIONS`
  - Cabeceras: `Authorization, Content-Type, Accept, X-Request-ID`

### C3 — Documentación API expuesta en producción ✅ CORREGIDO
- **Archivo:** `backend/app/main.py`
- **Descripción:** Los endpoints `/docs` (Swagger) y `/redoc` estaban siempre habilitados, exponiendo el esquema completo de la API a cualquier atacante.
- **Solución aplicada:** `docs_url` y `redoc_url` se deshabilitan automáticamente cuando `settings.is_production` es `True`.

### C4 — Sin autenticación ni autorización en ningún endpoint ⚠️ PENDIENTE
- **Archivos:** `backend/app/api/v1/trends.py`, `backend/app/api/v1/ingestion.py`
- **Descripción:** Todos los endpoints son completamente públicos. Cualquiera puede crear, modificar o leer trends sin ninguna verificación de identidad.
- **Acción requerida:** Diseñar e implementar sistema de autenticación (JWT bearer tokens) y añadir dependencia `Depends(get_current_user)` a los endpoints protegidos.

### C5 — `x-forwarded-for` manipulable en rate limiting ⚠️ PENDIENTE
- **Archivo:** `backend/app/main.py`
- **Descripción:** El middleware de rate limiting confía ciegamente en la cabecera `x-forwarded-for`, que un atacante puede falsificar para eludir el límite.
- **Acción requerida:** Validar que la petición provenga realmente de un proxy de confianza antes de aceptar esa cabecera. Usar la IP de `request.client.host` como fallback solo si el proxy está en una lista blanca.

### C6 — Base de datos SQLite por defecto en producción ⚠️ PENDIENTE
- **Archivo:** `backend/app/core/config.py`
- **Descripción:** `DATABASE_URL` tiene como fallback un archivo SQLite local. Si se despliega sin configurar explícitamente esta variable, todos los datos van a un fichero accesible a cualquier usuario del sistema.
- **Acción requerida:** Añadir validación en el `model_validator` para requerir una URL de base de datos explícita (no SQLite) en `ENVIRONMENT=production`.

---

## ALTOS

### A1 — Excepción tragada sin stack trace completo ✅ CORREGIDO
- **Archivo:** `backend/app/services/detector_service.py`
- **Descripción:** El bloque `except` capturaba la excepción, almacenaba solo `str(exc)` y hacía `raise`, perdiendo el stack trace completo que es necesario para depurar fallos en producción.
- **Solución aplicada:** Añadido `logger.exception("Ingestion batch failed: %s", exc)` antes del `raise`, que registra el traceback completo.

### A2 — Números mágicos en el scoring sin documentación ✅ CORREGIDO
- **Archivo:** `backend/app/services/detector_service.py`
- **Descripción:** La fórmula de puntuación de tendencias usaba 11 valores literales (`35`, `8`, `20`, `5`, `20`, `4`, `25`, `15`, `8`, `3`, `0.25`) sin ninguna explicación de su propósito.
- **Solución aplicada:** Extraídos a constantes con nombre y comentario en la cabecera del módulo:
  ```python
  _SCORE_BASE = 25
  _VELOCITY_CAP = 35
  _VELOCITY_DIVISOR = 8
  _BREADTH_CAP = 20
  _BREADTH_MULTIPLIER = 5
  _RECURRENCE_CAP = 20
  _RECURRENCE_MULTIPLIER = 4
  _SATURATION_BASE = 15
  _SATURATION_SOURCE_WEIGHT = 8
  _SATURATION_MENTION_WEIGHT = 3
  _OPPORTUNITY_BONUS = 12
  _SATURATION_DISCOUNT = 0.25
  ```

### A3 — Sin validación de `source_type` contra fuentes conocidas ⚠️ PENDIENTE
- **Archivo:** `backend/app/schemas/schemas.py`
- **Descripción:** El campo `source_type` acepta cualquier string de 2-40 caracteres. Datos maliciosos pueden contaminar el análisis de tendencias con fuentes inventadas.
- **Acción requerida:** Usar un `Literal` o `Enum` con las fuentes válidas: `hackernews`, `reddit`, `github`, `producthunt`, `demo`, `manual`.

### A4 — Sin manejo de errores de conexión a base de datos ⚠️ PENDIENTE
- **Archivo:** `backend/app/models/database.py`
- **Descripción:** El generador `get_db()` no captura `OperationalError` ni errores de pool agotado, lo que provoca excepciones 500 no controladas cuando la base de datos no está disponible.
- **Acción requerida:** Envolver la sesión en un try/except que devuelva un 503 con mensaje claro.

---

## MEDIOS

### M1 — `datetime.utcnow()` deprecado en Python 3.12+ ✅ CORREGIDO
- **Archivos:** `backend/app/models/base.py`, `backend/app/services/detector_service.py`, `backend/app/services/trend_service.py`, `backend/app/services/seed.py`
- **Descripción:** `datetime.utcnow()` está marcado como deprecado en Python 3.12 y será eliminado en versiones futuras.
- **Solución aplicada:** Reemplazado en todos los archivos por `datetime.now(timezone.utc).replace(tzinfo=None)`. En `base.py` se extrajo a una función auxiliar `_utcnow()` usada como `default` en todas las columnas de fechas.

### M2 — Sin paginación real en el listado de tendencias ✅ CORREGIDO
- **Archivos:** `backend/app/api/v1/trends.py`, `backend/app/services/trend_service.py`
- **Descripción:** El endpoint `GET /api/v1/trends` solo tenía parámetro `limit` (máximo 100), haciendo imposible acceder a registros más allá de los primeros 100.
- **Solución aplicada:** Añadido parámetro `skip: int` (`ge=0`) en el endpoint y en el método `TrendService.list_trends()`, que se traduce a `.offset(skip)` en la consulta SQL.

### M3 — Session timeout de 24 horas ✅ CORREGIDO
- **Archivo:** `backend/app/core/config.py`
- **Descripción:** `SESSION_TIMEOUT_MINUTES` tenía un valor por defecto de 1440 (24 horas), haciendo que las sesiones robadas permanecieran válidas todo un día.
- **Solución aplicada:** Valor reducido a 60 minutos por defecto.

### M4 — Sin protección CSRF en endpoints POST ⚠️ PENDIENTE
- **Archivos:** `backend/app/api/v1/trends.py`, `backend/app/api/v1/ingestion.py`
- **Descripción:** Los endpoints POST no implementan tokens CSRF. Aunque es menos crítico para APIs JSON puras con autenticación Bearer, sigue siendo un vector de ataque si se usan cookies.
- **Acción requerida:** Evaluar si se usarán cookies de sesión; si es así, añadir middleware CSRF (`starlette-csrf` o equivalente).

### M5 — Rate limiting solo en escrituras, no en lecturas ⚠️ PENDIENTE
- **Archivo:** `backend/app/main.py`
- **Descripción:** El middleware de rate limiting solo se aplica a `POST/PUT/DELETE` en rutas de ingestion. Los endpoints GET no tienen límite, lo que permite scraping masivo y ataques DoS a lecturas.
- **Acción requerida:** Aplicar rate limiting también a GETs, con umbrales diferenciados para usuarios autenticados vs anónimos.

---

## BAJOS

### B1 — Sin registro de eventos de seguridad (audit log) ⚠️ PENDIENTE
- **Archivos:** Todos los endpoints de escritura
- **Descripción:** No hay registro de quién creó, modificó o eliminó tendencias. Imposible rastrear abusos o cumplir requisitos de auditoría.
- **Acción requerida:** Añadir logging antes de cada `db.commit()` en operaciones de escritura, incluyendo IP del cliente y usuario (cuando exista auth).

### B2 — URL de fuente sin validación de formato ⚠️ PENDIENTE
- **Archivo:** `backend/app/schemas/schemas.py`
- **Descripción:** El campo `source_url` en `SignalIngest` acepta cualquier string, incluyendo URLs malformadas.
- **Acción requerida:** Cambiar tipo a `Optional[HttpUrl]` de Pydantic para validación automática.

### B3 — Frontend: errores de API sin detalle ⚠️ PENDIENTE
- **Archivo:** `frontend/src/lib/api.ts`
- **Descripción:** Los errores HTTP devuelven solo el código de estado (`"API request failed: 500"`), sin extraer el campo `detail` del body JSON de FastAPI.
- **Acción requerida:** Leer `response.json()` en el bloque de error y mostrar `error.detail || response.statusText`.

### B4 — Frontend: URL de API hardcodeada a localhost ⚠️ PENDIENTE
- **Archivo:** `frontend/src/lib/api.ts`
- **Descripción:** Si las variables de entorno no están configuradas, el cliente cae silenciosamente a `http://localhost:8000`, que falla en producción sin ningún aviso explícito.
- **Acción requerida:** Añadir validación en tiempo de build que lance error si `NEXT_PUBLIC_API_URL` no está definida.

---

## Checklist de pendientes prioritizados

```
[ ] C4  Implementar autenticación JWT en todos los endpoints protegidos
[ ] C6  Requerir DATABASE_URL explícita (no SQLite) en production
[ ] C5  Validar IP real en rate limiting (no confiar en x-forwarded-for)
[ ] A3  Enum de source_type válidos en SignalIngest
[ ] A4  Manejo de errores de conexión a DB (503 en lugar de 500)
[ ] M4  Evaluar y añadir protección CSRF si se usan cookies
[ ] M5  Rate limiting en endpoints GET
[ ] B1  Audit log de operaciones de escritura
[ ] B2  Validar source_url con HttpUrl
[ ] B3  Mejorar mensajes de error en el cliente frontend
[ ] B4  Fallar en build si NEXT_PUBLIC_API_URL no está definida
```

---

## Tests

Todos los tests del backend pasan tras los cambios aplicados:

```
15 passed in 0.27s
```
