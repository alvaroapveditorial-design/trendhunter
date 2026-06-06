# MVP Status

## Evaluación

Puntuación actual verificada: **78/100**.

Se mantiene cerca de 80 porque existe el loop real, aunque faltan deploy Railway ejecutado, auth, segunda fuente y smoke Docker/Railway validado:

`Hacker News/manual signal -> detector -> trend score -> dashboard -> run history`

## Terminado

- Backend FastAPI local.
- Frontend Next.js dashboard.
- SQLite local por defecto.
- API de tendencias.
- Pipeline heurística.
- Ingestion manual/demo.
- Hacker News collector.
- Historial básico de ejecuciones.
- Estados de loading/error en acciones principales del dashboard.
- Página de error del dashboard cuando el backend no está disponible.
- Manejo 502 controlado si Hacker News falla.
- Dockerfiles para backend y frontend.
- `docker-compose.yml` mínimo para levantar el MVP completo.
- Railway elegido como target de deploy.
- Config-as-code Railway añadida para backend y frontend.
- Alembic configurado con migración inicial.
- Dependencias backend limpiadas para instalar solo el MVP real y evitar conflictos de paquetes futuros.
- Rate limiting in-memory para endpoints mutables de ingestion.
- Tests backend.
- Build frontend.

## Parcialmente Terminado

- Producto UX: usable como dashboard, pero sin landing comercial completa.
- Agentes: hay registro y detector simple, pero no LangGraph real.
- IA: placeholders/config, sin llamadas LLM.
- Seguridad: validación básica y rate limiting local; falta auth y rate limiting distribuido.
- Producción: base Docker/Alembic creada, pendiente de endurecer para un proveedor concreto.

## Pendiente

- Deploy Railway ejecutado.
- Auth.
- Rate limiting distribuido si se escala a varias instancias.
- Tests frontend/smoke automatizado.
- Segunda fuente real.
- Reportes/alertas.

## Bloqueado Por Credenciales o Servicios

- OpenAI/Anthropic: insights LLM.
- Supabase: auth.
- Stripe: billing.
- Reddit/Product Hunt/GitHub con rate limits altos: tokens opcionales.

## Cómo Probar

Backend:

```bash
cd backend
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run lint
npm run build
npm run dev
```

Docker:

```bash
docker compose up --build
```

Migraciones:

```bash
cd backend
alembic upgrade head
```

Flujo manual:

1. Abrir `http://localhost:3000`.
2. Pulsar `Run demo ingestion`.
3. Pulsar `Pull Hacker News`.
4. Ver nuevas tendencias o actualizaciones.
5. Revisar `Recent pipeline runs` en el panel derecho.

## Cambios Recientes

- Las acciones principales del dashboard ahora muestran estado de ejecución y errores.
- El dashboard tiene una pantalla de error con botón de retry si no puede cargar datos.
- El endpoint de Hacker News devuelve `502` con mensaje estable si falla la red externa.

## Variables Relevantes

- `DATABASE_URL`: por defecto `sqlite:///./trendhunter.db`.
- `NEXT_PUBLIC_API_URL`: URL del backend para el frontend, por defecto `http://localhost:8000`.
- `HACKERNEWS_API_URL`: API pública de Hacker News.
- `HACKERNEWS_DEFAULT_LIMIT`: límite por defecto de historias a recoger.
- `AUTO_CREATE_TABLES`: `true` para comodidad local; en Docker se usa `false` porque corre Alembic.
- `RATE_LIMIT_ENABLED`: activa/desactiva rate limiting.
- `RATE_LIMIT_REQUESTS`: número de requests permitidas por ventana.
- `RATE_LIMIT_PERIOD`: ventana de rate limit en segundos.

## Rate Limiting

El MVP protege `POST /api/v1/ingestion/*` con un rate limiter in-memory por IP y ruta.
Esto es suficiente para una demo o una sola instancia. Para producción multi-instancia,
hay que cambiarlo por Redis o un rate limiter del proveedor de hosting.

## Deploy/Docker

Target elegido: Railway. Guía operativa en `docs/RAILWAY_DEPLOYMENT.md`.

El compose actual levanta:

- Backend en `http://localhost:8000`.
- Frontend en `http://localhost:3000`.
- SQLite persistida en volumen Docker `backend_data`.

El backend ejecuta `alembic upgrade head` antes de iniciar Uvicorn.
