# 09 — Weekly Council

**AI Trend Hunter · Consejo de Dirección**
Versión 1.0 · Julio 2026 · Propietario: CEO · Es la única reunión obligatoria de la empresa ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §3)

---

## 1. Qué es y qué no es

El Consejo Semanal es el órgano donde la empresa se mira a sí misma con números, decide, y deja constancia. **No es** una reunión de estado (el estado se lee, no se narra), ni una sesión de trabajo (el trabajo ocurre el resto de la semana), ni un ritual (si una sección no aporta una semana, se salta y se anota que se saltó).

## 2. Logística

- **Frecuencia:** semanal, mismo día y hora (recomendado: lunes, primera hora — la semana se planifica antes de ejecutarse).
- **Duración objetivo:** 45-60 minutos. Si excede 90, se corta y lo pendiente abre el orden del día siguiente.
- **Participantes:** CEO (preside y decide), ChatGPT (CTO/CPO — prepara análisis), Claude Code (Lead Engineer — trae estado técnico y métricas), Codex (solo cuando hay puntos de seguridad/arquitectura). Futuro: cada nuevo lead humano se incorpora con voz; el voto sigue el organigrama ([01_COMPANY_CHART.md](01_COMPANY_CHART.md)).
- **Preparación obligatoria:** los números se recopilan **antes** (checklist semanal de [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §9.2 + métricas de [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md)). Un Consejo sin números preparados se pospone, no se improvisa.

## 3. Orden del día (fijo)

### 3.1 Métricas (10 min) — los números primero, siempre
KPIs obligatorios en cada Consejo, con valor actual, semana anterior y tendencia:

| Bloque | KPIs mínimos |
|---|---|
| Negocio | Suscriptores de pago activos (North Star) · trials iniciados · conversión trial→pago · churn/cancelaciones · MRR |
| Funnel | Visitas landing · CTR landing→pricing · checkouts iniciados · activación de nuevos usuarios |
| Adquisición | Gasto en ads · CPC · coste por trial (CAC provisional) |
| Técnico | Errores Sentry nuevos · disparos del cron (¿corrió los 7 días?) · incidentes |
| Soporte | Mensajes recibidos · tiempo de respuesta · temas recurrentes |

Regla de lectura: primero el número, luego la explicación. Prohibido narrativizar sin dato ("siento que va mejor" no abre debate; un número sí). Cautela estadística de [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) §interpretación aplicada en voz alta cuando la muestra sea pequeña.

### 3.2 Revisión de OKRs (5 min)
Cada resultado clave del trimestre: número actual, semáforo honesto, y — si está en rojo dos semanas seguidas — decisión forzada: reforzar, reformular o abandonar ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §7.3).

### 3.3 Revisión comercial y de producto (10 min)
- Síntesis de las entrevistas/conversaciones con usuarios de la semana (mínimo esperado: 3 — [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §3). Qué se aprendió, qué patrón se acumula.
- Feedback de soporte: ¿algo se repite? (2+ repeticiones = candidato al filtro de decisión).
- Estado de los experimentos activos contra sus umbrales predefinidos.

### 3.4 Revisión técnica (5 min)
- Incidentes de la semana y sus postmortems ([08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) fase 11).
- Deuda técnica: ¿algo cruzó su umbral de urgencia? ([03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §4).
- Calidad de datos del producto (spot-check del dashboard: la señal es sagrada).

### 3.5 Revisión financiera (5 min)
- Caja y burn: gasto de infraestructura + ads vs. ingresos. A esta escala son cuatro números; se miran igual, todas las semanas — el hábito vale más que la cifra.
- Punto de equilibrio operativo (hoy: 2-3 suscripciones cubren infraestructura) y distancia a él.

### 3.6 Riesgos (5 min)
- ¿Algún indicador temprano de [12_RISK_REGISTER.md](12_RISK_REGISTER.md) se activó?
- ¿Riesgo nuevo detectado esta semana? (cualquiera puede traerlo, sin permiso previo)
- Una vez al mes, esta sección se expande a la revisión completa del registro.

### 3.7 Decisiones (10 min)
- Decisiones Tipo 1 pendientes, presentadas con el formato de [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) §5 (contexto, opciones con coste, recomendaciones).
- Escalados de conflicto pendientes ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §3).
- El CEO decide o pospone explícitamente con fecha ("lo decidimos el día X con el dato Y"). No hay tercera opción: la ausencia de decisión es una decisión que se registra como tal.

### 3.8 Roadmap y cola de la semana (5 min)
- Se cierra la cola: **máximo 3 iniciativas**, cada una con dueño, métrica y caducidad.
- Se dice explícitamente qué se decidió NO hacer (el coste de oportunidad se nombra, no se esconde).

## 4. Acta

Formato fijo, breve, en el registro de actas (documento o carpeta `governance/actas/`, un archivo por mes):

```
# Consejo YYYY-MM-DD
ASISTENTES:
NÚMEROS CLAVE: (tabla mínima: North Star, MRR, trials, conversión, churn, incidentes)
SEMÁFOROS OKR: KR1 🟢/🟡/🔴 ...
DECISIONES: (formato DECISIÓN #YYYY-NN de 07_DECISION_FRAMEWORK)
COLA DE LA SEMANA: 1) ... 2) ... 3) ...
EXPLÍCITAMENTE NO HACEMOS: ...
RIESGOS NUEVOS/ACTIVADOS: ...
SEGUIMIENTO PENDIENTE: (qué se revisa la semana que viene y quién lo trae)
```

Reglas del acta:
- Se escribe durante o inmediatamente después del Consejo, nunca "luego".
- Lo que no está en el acta no se decidió ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §3.2).
- La primera sección del Consejo siguiente revisa el "seguimiento pendiente" del acta anterior — así se cierra el bucle y nada se evapora.

## 5. Seguimiento entre Consejos

- Las decisiones con fecha de revisión entran automáticamente en el orden del día de esa fecha.
- Un incidente grave entre Consejos no espera al lunes: se gestiona con la regla de urgencia ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §3) y se postmortemiza en el siguiente Consejo.
- Si el CEO no puede celebrar el Consejo una semana, se publica igualmente el acta con los números y las decisiones se posponen — los números no descansan.
