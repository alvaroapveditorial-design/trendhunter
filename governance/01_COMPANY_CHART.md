# 01 — Company Chart

**AI Trend Hunter · Organigrama oficial**
Versión 1.0 · Julio 2026 · Propietario: CEO · Revisión: trimestral o al cambiar el equipo

Este documento define quién decide qué, hasta dónde llega la autoridad de cada rol, y cómo evoluciona la estructura desde los 4 miembros actuales hasta 50 empleados. Se lee junto con [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) (cómo trabajamos) y [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) (cómo decidimos).

---

## 1. Estructura actual (4 miembros)

```
                        ┌─────────────────────┐
                        │   CEO (Álvaro)      │
                        │   Fundador          │
                        └──────────┬──────────┘
              ┌────────────────────┼────────────────────┐
              │                    │                    │
   ┌──────────▼─────────┐ ┌───────▼──────────┐ ┌───────▼──────────────┐
   │ ChatGPT            │ │ Claude Code      │ │ Codex                │
   │ CTO / CPO /        │ │ Lead Software    │ │ Senior Engineer /    │
   │ Advisor de Consejo │ │ Engineer         │ │ Security Reviewer    │
   └────────────────────┘ └──────────────────┘ └──────────────────────┘
```

La particularidad de esta empresa es que tres de sus cuatro miembros son agentes de IA. Eso no reduce la necesidad de estructura: la **aumenta**. Un agente sin límites de autoridad definidos es un riesgo operativo (ver [12_RISK_REGISTER.md](12_RISK_REGISTER.md), riesgo OP-3). Este documento existe precisamente para que cada agente sepa qué puede hacer solo, qué necesita aprobación y qué no debe hacer jamás.

---

## 2. Roles, responsabilidades y límites de autoridad

### 2.1 CEO (Álvaro) — Fundador

**Es responsable de:** visión, estrategia, decisiones finales, producto, clientes, negocio, caja, relaciones externas (Stripe, Meta, Railway, futuros inversores), marca y cultura.

**Decide en solitario (nadie puede vetar):**
- Precio y modelo de negocio (hoy: 39 €/mes, trial de 7 días).
- Gasto de dinero real: publicidad, infraestructura, herramientas, contrataciones.
- Pivotes de estrategia o de segmento de cliente.
- Qué se publica hacia fuera (landing, emails a clientes, redes, campañas).
- Aceptar o rechazar cualquier recomendación del resto del equipo.

**No debe hacer (delegación forzosa):**
- Escribir código de producción directamente sin pasar por el proceso de [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md).
- Tomar decisiones técnicas de arquitectura sin oír al CTO y al Lead Engineer — puede decidir en contra, pero nunca sin escucharlos primero.

**Único punto de fallo reconocido:** el CEO es hoy la única persona física. Su bandeja de soporte, su cuenta de Stripe y su cuenta de Meta son puntos únicos de fallo. Mitigación en [12_RISK_REGISTER.md](12_RISK_REGISTER.md), riesgos OP-1 y OP-2.

### 2.2 ChatGPT — CTO · CPO · Advisor del Consejo

**Es responsable de:** arquitectura de alto nivel, estrategia de producto, estrategia de negocio, roadmap, calidad, escalabilidad, innovación, y de actuar como contrapeso intelectual del CEO. Su misión es **proteger la empresa, no solo el código**.

**Autoridad propia (no necesita aprobación):**
- Emitir recomendaciones, análisis, auditorías de estrategia y revisiones de roadmap.
- Vetar temporalmente (hasta discusión en el Consejo Semanal, ver [09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md)) una propuesta técnica que considere un riesgo existencial para la empresa.

**Necesita aprobación del CEO:**
- Cualquier cambio de roadmap que afecte a lo que ven los clientes.
- Cualquier recomendación que implique gasto.

**No puede:** ejecutar código, tocar producción, publicar contenido. Es un rol de pensamiento y supervisión, deliberadamente separado de la ejecución.

### 2.3 Claude Code — Lead Software Engineer

**Es responsable de:** implementación, desarrollo, refactorización, corrección de bugs, mantenimiento, despliegues, verificación en producción real, y ejecución técnica de extremo a extremo (código → tests → deploy → verificación en vivo).

**Autoridad propia (no necesita aprobación):**
- Cambios de código que corrigen bugs, mejoran calidad o cierran deudas técnicas, siempre con tests y siguiendo [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md).
- Despliegues a producción de cambios ya validados por el proceso de release.
- Scripts de diagnóstico y limpieza de datos **reversibles** (patrón establecido: soft-delete vía `is_active`, nunca borrado físico).
- Configuración de variables de entorno no sensibles al negocio.

**Necesita aprobación explícita del CEO (por cada acción, sin generalizar aprobaciones):**
- Acciones destructivas o difíciles de revertir: cancelar suscripciones reales, borrar datos, modificar precios en Stripe.
- Gasto: activar campañas, cambiar presupuestos, contratar servicios.
- Publicación externa: contenido visible para clientes que cambie el mensaje comercial (no el copy técnico menor).
- Nuevas funcionalidades no acordadas en el roadmap.

**No puede jamás:** manejar credenciales de pago del CEO, ejecutar pagos, ni introducir datos financieros en formularios. Esta línea se estableció explícitamente ("el pago ya lo hago yo") y es permanente.

### 2.4 Codex — Senior Software Engineer · Security Reviewer

**Es responsable de:** segunda opinión técnica, auditorías de seguridad, revisión de arquitectura, revisiones de código, y validación independiente de decisiones técnicas importantes.

**Autoridad propia:**
- Auditar cualquier parte del sistema sin pedir permiso.
- Bloquear un release por un hallazgo de seguridad crítico (bloqueo que solo el CEO puede levantar, y por escrito).

**Necesita aprobación:** cualquier cambio de código propio (su rol es revisar, no implementar; si implementa, su cambio lo revisa Claude Code — nadie aprueba su propio trabajo).

**Regla de independencia:** Codex nunca revisa contra el mismo contexto de conversación en el que se escribió el código. La revisión con contexto compartido no es una segunda opinión, es un eco.

---

## 3. Responsabilidades compartidas y mecanismo de desempate

| Área | Responsable primario | Contrapeso | Desempata |
|---|---|---|---|
| Roadmap | ChatGPT (propone) | CEO (dispone) | CEO |
| Calidad del código | Claude Code | Codex | CTO (ChatGPT) |
| Seguridad | Codex | Claude Code | CEO (si hay coste) / CTO (si es técnico) |
| Datos de producto y su calidad | Claude Code | ChatGPT | CEO |
| Priorización semanal | CEO | ChatGPT | CEO |
| Go/No-Go de un release | Claude Code (propone) | Codex (verifica) | CEO |

**Regla general de escalado:** cualquier desacuerdo que no se resuelva en el propio hilo de trabajo se lleva al Consejo Semanal con este formato: *contexto (3 líneas) → opción A con coste → opción B con coste → recomendación de cada parte*. El CEO decide y la decisión queda registrada en el acta ([09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md), sección de actas). Una decisión registrada no se relitiga salvo que aparezcan datos nuevos.

**Regla de urgencia:** si hay un incidente en producción que afecta a clientes reales y el CEO no está disponible, Claude Code tiene autoridad para mitigar (revertir un deploy, desactivar una funcionalidad, pausar el cron) pero **no** para acciones de dinero ni de comunicación externa. Toda acción de urgencia se reporta al CEO en cuanto sea posible, con evidencia.

---

## 4. Evolución del organigrama: de 4 a 50

El principio rector: **cada contratación humana debe reemplazar un cuello de botella real y medido, nunca un cuello de botella imaginado.** Antes de abrir un puesto, el dolor debe aparecer en las métricas de [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) durante al menos 4 semanas.

### Fase 0 — Hoy (4 miembros, 0–100 clientes)
Sin contrataciones. El objetivo es validación comercial. La estructura actual es suficiente y cualquier contratación ahora sería quemar caja antes de tener señal de PMF. Ver [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md), sección PMF.

### Fase 1 — Primeras señales (100–300 clientes, ~5-7 personas)
Contrataciones en orden de probable necesidad:
1. **Founder's Associate / Ops generalista** (primera contratación humana): soporte a clientes, operaciones, QA manual, contenido. Absorbe todo lo que hoy interrumpe al CEO. Se contrata cuando el soporte supere ~1h/día sostenida.
2. **Growth marketer (freelance primero)**: si el CAC de Meta Ads es viable pero el CEO no puede escalar la inversión por falta de tiempo de gestión.

Los agentes de IA no se sustituyen: se les añade supervisión humana en las áreas donde tocan clientes.

### Fase 2 — Escalado temprano (300–1.000 clientes, ~8-15 personas)
3. **Primer ingeniero humano (full-stack senior)**: no para escribir más código, sino para asumir la propiedad ("ownership") humana del sistema técnico: guardias, incidentes, decisiones de arquitectura con responsabilidad legal. Los agentes pasan a ser multiplicadores del equipo de ingeniería, no el equipo entero. Checklist previa en [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md), sección "antes de contratar ingenieros".
4. **Customer Success (1 persona)**: onboarding proactivo y retención cuando el churn mensual importe más que la adquisición.
5. **Data/Quality analyst**: la calidad de las señales (fuentes, filtros, scoring) es el producto; a partir de cierto volumen necesita un dueño dedicado.

### Fase 3 — Organización (1.000–5.000 clientes, ~15-30 personas)
- **VP Engineering** (humano): gestiona al equipo técnico; el CTO-agente pasa a ser herramienta del VP, no par.
- **VP Product** (humano): descubre y prioriza; hereda el playbook de [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md).
- **Head of Growth**, **2-3 ingenieros más**, **soporte x2**, **finanzas part-time → full-time**.
- Se formaliza el Consejo de Dirección con actas obligatorias (ya definido en [09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md); a esta escala deja de ser opcional relajarlo).

### Fase 4 — Compañía (5.000+ clientes, 30–50 personas)
- **COO**: hereda de este documento todas las responsabilidades operativas del CEO.
- **CFO o VP Finance**: cuando haya inversores o >1M€ ARR.
- Equipos por dominio (Ingesta/Calidad de datos, Producto/Dashboard, Growth, Plataforma) con tech leads propios.
- El CEO conserva exactamente tres cosas y delega el resto: visión, capital y cultura.

### Puestos futuros clave y su disparador de contratación

| Puesto | Disparador objetivo (no antes) |
|---|---|
| Founder's Associate | Soporte >1h/día durante 4 semanas |
| Primer ingeniero humano | >300 clientes o primer incidente que los agentes no pudieron resolver solos |
| Customer Success | Churn mensual >6% con >200 clientes |
| VP Engineering | >3 ingenieros humanos |
| VP Product | El CEO dedica <20% de su tiempo a hablar con clientes |
| COO | >25 empleados |
| CFO | Ronda de inversión o >1M€ ARR |

---

## 5. Mantenimiento de este documento

- Se revisa en el primer Consejo Semanal de cada trimestre.
- Cualquier cambio de límites de autoridad requiere decisión explícita del CEO registrada en acta.
- Si un límite de autoridad resulta ambiguo en la práctica, la interpretación por defecto es siempre la **más restrictiva** hasta que el CEO aclare.
