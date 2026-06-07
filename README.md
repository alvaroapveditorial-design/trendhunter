# AI Trend Hunter

**Plataforma de detección temprana de tendencias impulsada por IA para descubrir oportunidades antes de que el mercado se sature.**

AI Trend Hunter es un SaaS moderno que analiza señales públicas, detecta tendencias emergentes, las puntúa y las convierte en oportunidades accionables para emprendedores, equipos de producto y builders.

El enfoque del proyecto es privacy-first: fuentes públicas, mínima exposición de datos personales y arquitectura preparada para cumplimiento GDPR.

---

## Funcionalidades Principales

- **Detección de tendencias**: monitorización de señales emergentes en fuentes públicas.
- **Scoring inteligente**: puntuación por momentum, velocidad, oportunidad y saturación.
- **Pipeline de ingestión**: señales manuales, demo local, collector de Hacker News, feeds RSS y GitHub.
- **Dashboard MVP**: visualización de tendencias, fuentes, categorías y ejecuciones recientes.
- **Opportunity finder**: traducción de señales en posibles ideas SaaS o negocios.
- **Alertas y reportes**: planificados para fases posteriores.
- **Arquitectura privacy-first**: sin PII por defecto, fuentes públicas y analítica mínima.

---

## Estado Actual Del MVP

El repositorio ya incluye un MVP ejecutable:

- Backend FastAPI con `/health` y endpoints de tendencias.
- Base de datos SQLite local por defecto en `backend/trendhunter.db`.
- Creación automática de tablas en desarrollo local.
- Seed inicial con tendencias demo.
- Dashboard Next.js conectado al backend.
- Pipeline heurístico que convierte señales en tendencias puntuadas.
- Collector de Hacker News para señales públicas reales.
- Collector RSS/Atom para una segunda fuente pública sin API key.
- Collector de repositorios GitHub para señales dev/AI.
- Historial básico de ejecuciones de ingestión.
- Rate limiting in-memory para endpoints mutables de ingestión.
- Docker y Alembic configurados para levantar el MVP completo.

No necesitas OpenAI, Supabase, Redis, Qdrant ni PostgreSQL para la primera ejecución local.

Consulta también [docs/MVP_CHECKLIST.md](docs/MVP_CHECKLIST.md) para la checklist ejecutable, [docs/MVP_STATUS.md](docs/MVP_STATUS.md) para el estado resumido y [docs/RAILWAY_DEPLOYMENT.md](docs/RAILWAY_DEPLOYMENT.md) para el despliegue elegido.

---

## Arquitectura

```text
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                  │
│              Dashboard | Tendencias | Acciones          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                    │
│        Trend API | Ingestion API | Health checks        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴──────────────┬─────────────┐
        ▼                           ▼             ▼
┌──────────────┐ ┌──────────────────────┐ ┌────────────┐
│ Detector MVP │ │  Worker Queue        │ │ Vector DB  │
│ Heurístico   │ │  Celery + Redis      │ │ Qdrant     │
└──────────────┘ │  Planificado         │ │ Planificado│
                 └──────────────────────┘ └────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│              Base de Datos SQLite/PostgreSQL            │
│             Tendencias | Fuentes | Ejecuciones          │
└─────────────────────────────────────────────────────────┘
```

### Patrones De Diseño

- **Clean Architecture**: separación clara entre API, dominio, servicios y persistencia.
- **Domain-Driven Design lite**: modelos de dominio para tendencias, fuentes y agentes.
- **Service layer**: lógica de negocio aislada de los endpoints.
- **Repository pattern**: acceso a datos abstraído.
- **Agent orchestration**: detector heurístico actual; LangGraph planificado.

---

## Stack Técnico

### Frontend

- Next.js 16
- TypeScript
- React 18
- CSS global/modules para el MVP
- Data fetching server-rendered

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite local
- PostgreSQL planificado para producción
- Alembic para migraciones
- Detector heurístico actual
- LangGraph, OpenAI/Claude, Celery, Redis y Qdrant planificados

### Infraestructura

- Docker y `docker-compose.yml`
- Railway como target de deploy del MVP
- Backend y frontend dockerizados
- CI/CD planificado con GitHub Actions
- Health checks y logging estructurado

### Integraciones Planificadas

- Supabase Auth para autenticación
- Stripe para billing
- Plausible para analítica privacy-first
- Resend para emails
- OpenAI GPT-4 / Claude para insights LLM

---

## Arranque Rápido

### Requisitos

- Python 3.11+
- Node.js
- Docker opcional para levantar el stack completo

PostgreSQL, Redis y Qdrant están planificados para fases posteriores; el MVP local funciona con SQLite.

### Backend

```bash
cd trendhunter/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

La API quedará disponible en `http://localhost:8000`.

### Frontend

En otra terminal:

```bash
cd trendhunter/frontend
npm install
npm run dev
```

Abre `http://localhost:3000` con el backend corriendo en el puerto `8000`.

---

## Probar La API

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/trends
curl http://localhost:8000/api/v1/trends/meta/categories
curl http://localhost:8000/api/v1/trends/ai-copilots-vertical-saas
curl http://localhost:8000/api/v1/ingestion/runs
curl -X POST http://localhost:8000/api/v1/ingestion/demo
curl -X POST "http://localhost:8000/api/v1/ingestion/hackernews?feed=top&limit=10"
curl http://localhost:8000/api/v1/ingestion/rss/feeds
curl -X POST "http://localhost:8000/api/v1/ingestion/rss?feed=techcrunch_startups&limit=10"
curl -X POST "http://localhost:8000/api/v1/ingestion/github?limit=10"
```

Documentación automática:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Endpoints Actuales

- `GET /health`: estado de la API.
- `GET /api/v1/trends`: lista tendencias activas.
- `GET /api/v1/trends?category=ai_saas&min_score=70`: filtra tendencias.
- `GET /api/v1/trends/meta/categories`: lista categorías.
- `GET /api/v1/trends/{id_or_slug}`: detalle de tendencia con fuentes.
- `POST /api/v1/trends`: crea una tendencia manualmente.
- `POST /api/v1/ingestion/demo`: ejecuta el detector demo local.
- `POST /api/v1/ingestion/signals`: analiza señales raw y crea/actualiza tendencias.
- `POST /api/v1/ingestion/hackernews?feed=top&limit=10`: recoge historias de Hacker News y las analiza.
- `GET /api/v1/ingestion/rss/feeds`: lista feeds RSS configurados.
- `POST /api/v1/ingestion/rss?feed=techcrunch_startups&limit=10`: recoge items RSS/Atom y los analiza.
- `POST /api/v1/ingestion/github?limit=10`: recoge repositorios públicos de GitHub y los analiza.
- `GET /api/v1/ingestion/runs`: lista ejecuciones recientes del pipeline.

Los endpoints mutables de `/api/v1/ingestion` están protegidos por rate limiting in-memory. Se configura con `RATE_LIMIT_ENABLED`, `RATE_LIMIT_REQUESTS` y `RATE_LIMIT_PERIOD`.

---

## Ejemplo De Ingestión De Señales

```bash
curl -X POST http://localhost:8000/api/v1/ingestion/signals \
  -H "Content-Type: application/json" \
  -d '{
    "signals": [
      {
        "title": "AI assistants for restaurant inventory planning",
        "content": "Operators are asking for AI tools that predict ingredient demand and reduce waste.",
        "source_type": "manual",
        "source_id": "restaurant-inventory-ai",
        "upvotes": 88,
        "comments": 17,
        "shares": 9,
        "keywords": ["restaurant inventory AI", "demand planning"],
        "category": "ai_saas"
      }
    ]
  }'
```

El detector MVP guarda cada ejecución en `agent_executions`, almacena evidencia en `trend_sources` y recalcula scores de tendencia, oportunidad, saturación y momentum.

---

## Hacker News Collector

Hacker News no requiere API key:

```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/hackernews?feed=top&limit=10"
```

Feeds soportados:

- `top`
- `new`
- `best`
- `ask`
- `show`
- `job`

## RSS Collector

RSS no requiere API key:

```bash
curl http://localhost:8000/api/v1/ingestion/rss/feeds
curl -X POST "http://localhost:8000/api/v1/ingestion/rss?feed=techcrunch_startups&limit=10"
```

Feeds configurados por defecto:

- `techcrunch_startups`
- `producthunt`
- `hn_frontpage`

## GitHub Collector

GitHub funciona sin API key para pruebas, aunque `GITHUB_TOKEN` mejora rate limits:

```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/github?limit=10"
curl -X POST "http://localhost:8000/api/v1/ingestion/github?q=topic:ai%20stars:%3E100&limit=5"
```

---

## Comandos Del Frontend

```bash
cd frontend
npm run lint
npm run build
npm run smoke
npm run dev
```

- `npm run lint`: validación TypeScript.
- `npm run build`: build de producción de Next.js.
- `npm run smoke`: smoke E2E con Playwright contra Railway o `PLAYWRIGHT_BASE_URL`.
- `npm run dev`: servidor local de desarrollo.

---

## Docker

```bash
docker compose up --build
```

Levanta:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

El contenedor del backend ejecuta `alembic upgrade head` antes de arrancar Uvicorn.

---

## Migraciones

```bash
cd backend
alembic upgrade head
```

En desarrollo local, `AUTO_CREATE_TABLES=true` sigue activo por comodidad. Docker usa `AUTO_CREATE_TABLES=false` y arranca con Alembic.

---

## Tests

Backend:

```bash
cd backend
pytest tests/ -v
```

Frontend:

```bash
cd frontend
npm run lint
npm run build
npm run smoke
```

---

## Variables Relevantes

- `DATABASE_URL`: por defecto `sqlite:///./trendhunter.db`.
- `NEXT_PUBLIC_API_URL`: URL del backend para el frontend, por defecto `http://localhost:8000`.
- `HACKERNEWS_API_URL`: API pública de Hacker News.
- `HACKERNEWS_DEFAULT_LIMIT`: límite por defecto de historias a recoger.
- `RSS_DEFAULT_FEED`: feed RSS configurado por defecto.
- `RSS_FEED_URLS`: feeds RSS en formato `clave=url,clave=url`.
- `GITHUB_API_URL`: API pública de GitHub.
- `GITHUB_DEFAULT_LIMIT`: límite por defecto de repositorios a recoger.
- `GITHUB_SEARCH_QUERY`: query por defecto para GitHub search.
- `AUTO_CREATE_TABLES`: `true` para comodidad local; en Docker se usa `false`.
- `RATE_LIMIT_ENABLED`: activa/desactiva rate limiting.
- `RATE_LIMIT_REQUESTS`: número de requests permitidas por ventana.
- `RATE_LIMIT_PERIOD`: ventana de rate limit en segundos.

Consulta [.env.example](.env.example) para la configuración completa.

---

## Esquema De Datos Principal

- `users`: usuarios y suscripciones futuras.
- `trends`: tendencias detectadas y metadatos.
- `trend_sources`: evidencia y fuentes de cada tendencia.
- `alerts`: configuración futura de alertas.
- `agent_executions`: logs de ejecuciones del pipeline.
- `trend_embeddings`: embeddings para similitud, planificado con Qdrant.

---

## Sistema De Agentes

### Arquitectura Multiagente Planificada

1. **Source Collector Agent**
   - Recoge datos de Reddit, GitHub, Hacker News, Product Hunt y otras fuentes.
   - Usa APIs oficiales, RSS y deduplicación.

2. **Noise Filter Agent**
   - Reduce spam y falsos positivos.
   - Combina heurísticas y scoring LLM.

3. **Trend Analyzer Agent**
   - Calcula momentum, velocidad y saturación.
   - Genera `trend_score` de 0 a 100.
   - Detecta patrones de crecimiento.

4. **Opportunity Finder Agent**
   - Mapea tendencias a oportunidades SaaS o negocio.
   - Identifica huecos de mercado.
   - Sugiere ideas de contenido.

5. **Competitor Watcher Agent**
   - Vigila startups emergentes.
   - Monitoriza productos virales y keywords en tendencia.

6. **Report Generator Agent**
   - Crea dashboards y PDFs.
   - Genera insights y envía alertas.

---

## Privacidad Y Seguridad

### Arquitectura Privacy-First

- No se almacena PII por defecto.
- Solo fuentes públicas.
- Preparado para GDPR.
- Retención de datos configurable.
- Analítica anonimizada planificada con Plausible.
- Cookies mínimas.
- Headers seguros.
- Rate limiting en endpoints mutables.

### Seguridad Técnica

- Validación y sanitización de inputs.
- Prevención de SQL injection mediante ORM.
- Protección XSS desde frontend/framework.
- Autenticación y autorización planificadas.
- Audit logging planificado.

---

## Roadmap

### Fase 1: MVP Actual

- [x] Arquitectura base.
- [x] Backend FastAPI.
- [x] SQLite local.
- [x] Seed demo.
- [x] Endpoints de listar/detallar/crear tendencias.
- [x] Dashboard frontend MVP.
- [x] Pipeline heurístico local.
- [x] Collector público de Hacker News.
- [x] Collector público RSS/Atom.
- [x] Collector público de GitHub.
- [x] Tests backend.
- [x] Build frontend.
- [x] Target de deploy elegido: Railway.
- [ ] Orquestación básica de agentes.
- [ ] Autenticación.

### Fase 2: Detección Mejorada

- [ ] Capacidades avanzadas de agentes.
- [ ] Actualización de tendencias en tiempo real.
- [ ] Sistema de alertas personalizadas.
- [ ] Generación de reportes PDF.
- [ ] Monitorización de competidores.

### Fase 3: Escala Y Analítica

- [ ] Analítica avanzada.
- [ ] Colaboración por equipos.
- [ ] Integraciones personalizadas.
- [ ] Funciones enterprise.
- [ ] SLA y soporte.

### Fase 4: Marketplace

- [ ] Marketplace de APIs.
- [ ] Apps de terceros.
- [ ] Suscripciones de datos.
- [ ] White-label.

---

## Documentación

- [Plan de ejecución](docs/EXECUTION_PLAN.md)
- [Estado del MVP](docs/MVP_STATUS.md)
- [Siguientes pasos](docs/NEXT_STEPS.md)
- [Guía de testing](docs/TESTING.md)
- [Deploy Railway](docs/RAILWAY_DEPLOYMENT.md)
- [Backend](backend/README.md)
- [Frontend](frontend/README.md)

---

## Soporte

- Documentación: [docs/](docs/)
- Issues: `https://github.com/trendhunter/trendhunter/issues`
- Email: `support@trendhunter.io`

---

## Licencia

MIT License. Consulta `LICENSE` si existe en el repositorio.

---

**AI Trend Hunter** - Detecta tendencias. Encuentra oportunidades. Escala antes.
