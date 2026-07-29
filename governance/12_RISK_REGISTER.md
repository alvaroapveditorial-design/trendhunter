# 12 — Risk Register

**AI Trend Hunter · Registro oficial de riesgos**
Versión 1.0 · Julio 2026 · Propietario: CEO · Auditor técnico: Codex · Revisión: mensual en Consejo ([09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md) §3.6)

**Escalas:** Probabilidad: Baja / Media / Alta. Impacto: Bajo (molestia) / Medio (daña métricas o clientes puntuales) / Alto (amenaza ingresos, confianza o continuidad). **Prioridad** = combinación; todo Alta×Alto o Alta×Medio exige mitigación activa en cola ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §5).

---

## 1. Riesgos técnicos (TEC)

### TEC-1 · Pipeline de ingesta deja de correr en silencio
- **Descripción:** el cron falla y el producto sirve datos viejos sin que nadie lo note. **Ya ocurrió** (variable `JWT_SECRET` ausente: días de datos congelados).
- **Prob.:** Media (mitigado, no eliminado) · **Impacto:** Alto (el producto pierde su razón de ser a diario) · **Prioridad:** ALTA
- **Indicadores tempranos:** `agent_executions` sin filas en ventana 08:00-08:15 UTC; frescura >24h ([11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) §2.3).
- **Mitigación:** Sentry en el cron (hecho) · variables completas en todos los servicios como regla de deploy (hecho, [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) fase 9) · **pendiente:** alerta automática diaria de frescura ([03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §8.1).
- **Responsable:** Lead Engineer · **Estado:** mitigación parcial, alerta pendiente · **Revisión:** agosto 2026

### TEC-2 · Degradación de la calidad de la señal
- **Descripción:** contenido basura (off-topic, otro idioma, mal etiquetado) llega al dashboard. **Ya ocurrió tres veces** (descripción bilingüe que diluía el filtro, bypass del filtro por endpoint raw, vocabulario insuficiente que causó falsos positivos).
- **Prob.:** Alta (los filtros heurísticos fallan por vocabulario nuevo por naturaleza) · **Impacto:** Alto (la señal es el producto — [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md) §3) · **Prioridad:** ALTA
- **Indicadores tempranos:** spot-check semanal con hallazgos; queja de usuario; caída brusca de trends activos (limpieza agresiva = el riesgo inverso, falsos positivos del filtro).
- **Mitigación:** gate centralizado en `DetectorService` (hecho) · single source of truth de términos (hecho) · tests de regresión por cada caso (hecho) · spot-check semanal permanente · revisión del vocabulario al cambiar el paisaje de fuentes.
- **Responsable:** Lead Engineer · **Estado:** vivo, gestión continua · **Revisión:** mensual

### TEC-3 · Pérdida de datos (Postgres único)
- **Descripción:** corrupción o borrado del Postgres de Railway sin restauración probada.
- **Prob.:** Baja · **Impacto:** Alto (suscripciones y trends; lo primero es reconstruible desde Stripe con dolor, lo segundo parcialmente) · **Prioridad:** MEDIA-ALTA
- **Indicadores tempranos:** ninguno fiable — por eso la mitigación es preventiva.
- **Mitigación pendiente (en checklist 100 clientes):** verificar backups de Railway **restaurando uno de verdad** y documentar RPO/RTO.
- **Responsable:** Lead Engineer · **Estado:** abierto · **Revisión:** antes de 100 clientes

### TEC-4 · Arquitectura single-process alcanza su límite
- **Descripción:** rate limiting in-memory, un solo proceso, sin réplicas: correcto hoy, roto si se escala horizontalmente sin rediseño.
- **Prob.:** Baja a corto plazo · **Impacto:** Medio · **Prioridad:** BAJA (deuda registrada, [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §4)
- **Indicador temprano:** p95 latencia >500ms sostenido; decisión de añadir réplicas.
- **Mitigación:** documentada la condición de disparo; migrar rate limit a almacén compartido llegado el momento.
- **Responsable:** CTO · **Estado:** aceptado conscientemente · **Revisión:** al planificar 1.000 clientes

## 2. Riesgos de dependencia (DEP)

### DEP-1 · Cambios o límites en fuentes de datos (GitHub, HN, RSS)
- **Descripción:** una fuente cambia su API, limita el acceso o degrada su feed; el pipeline pierde una pata.
- **Prob.:** Media · **Impacto:** Alto · **Prioridad:** ALTA
- **Indicadores tempranos:** errores HTTP del collector en Sentry; caída de `records_processed` de una fuente en `agent_executions`.
- **Mitigación:** tres fuentes independientes (hecho — ninguna supera ~50% de la señal) · manejo de errores por fuente aislado (un collector caído no tumba el run) · candidatas de reemplazo identificadas en frío (Product Hunt, Reddit ya contemplados en config).
- **Responsable:** Lead Engineer · **Estado:** mitigación estructural hecha · **Revisión:** trimestral

### DEP-2 · Dependencia de plataforma (Railway)
- **Descripción:** subida de precios, degradación o cierre de Railway.
- **Prob.:** Baja · **Impacto:** Medio (todo es portable: Docker + Postgres estándar) · **Prioridad:** BAJA
- **Mitigación:** contenedores estándar (hecho) · plan B documentado (pendiente, basta un párrafo: proveedor alternativo + pasos) · backups fuera de Railway cuando TEC-3 se resuelva.
- **Responsable:** CTO · **Estado:** aceptado · **Revisión:** semestral

### DEP-3 · Suspensión de cuenta publicitaria de Meta
- **Descripción:** Meta deshabilita la cuenta de ads (ya ocurrió una vez por un fallo de pago; se recuperó). Sin ella, el único canal activo de adquisición se apaga.
- **Prob.:** Media (las cuentas nuevas con poco historial son frágiles) · **Impacto:** Alto en fase de validación · **Prioridad:** ALTA
- **Indicadores tempranos:** avisos de facturación, rechazos de anuncios, gasto en 0 € con campaña activa.
- **Mitigación:** método de pago saneado (hecho) · presupuestos modestos y campañas conservadoras (hecho: 5 €/día) · **canal alternativo en construcción como seguro:** contenido/orgánico — no depender jamás de un solo canal de adquisición.
- **Responsable:** CEO · **Estado:** vivo · **Revisión:** mensual

## 3. Riesgos de producto y comerciales (COM)

### COM-1 · No hay demanda suficiente al precio actual (riesgo existencial de la fase)
- **Descripción:** el producto no convierte a 39 €/mes: el problema no duele lo bastante o la solución no lo resuelve lo bastante.
- **Prob.:** Media (aún sin datos suficientes — es exactamente lo que la fase de validación debe responder) · **Impacto:** Alto · **Prioridad:** ALTA
- **Indicadores tempranos:** conversión trial→pago persistentemente <15% con activación sana; test de Sean Ellis <25%; entrevistas con patrón "interesante pero no pagaría".
- **Mitigación:** proceso de validación disciplinado ([04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) §2-3: 3 entrevistas/semana, umbrales escritos) · disposición real a pivotar precio/segmento/propuesta con la metodología de [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §10 — este riesgo no se mitiga con esperanza, se mitiga con velocidad de aprendizaje.
- **Responsable:** CEO · **Estado:** abierto, es el riesgo central del trimestre · **Revisión:** semanal en Consejo

### COM-2 · Competencia con distribución superior
- **Descripción:** un player con audiencia (newsletter grande, herramienta establecida) lanza algo equivalente.
- **Prob.:** Media · **Impacto:** Medio (el mercado es grande; el peligro real es COM-1, no los competidores) · **Prioridad:** MEDIA
- **Indicadores tempranos:** lanzamientos en PH/HN de la categoría; menciones en entrevistas.
- **Mitigación:** velocidad + foco en calidad de señal + relación directa con los primeros 100 (un competidor puede copiar features; no puede copiar confianza acumulada).
- **Responsable:** CEO · **Estado:** vigilancia pasiva · **Revisión:** trimestral

### COM-3 · Churn estructural por naturaleza del producto
- **Descripción:** el usuario encuentra su oportunidad y se va ("ya tengo mi idea"); el producto es de compra puntual disfrazada de suscripción.
- **Prob.:** Media · **Impacto:** Alto en LTV · **Prioridad:** MEDIA-ALTA (aún sin datos)
- **Indicadores tempranos:** churn concentrado en el mes 1-2 con satisfacción alta en la salida ("me encantó, ya no lo necesito").
- **Mitigación futura (hipótesis, no compromiso):** valor recurrente más allá del descubrimiento — vigilancia continua del nicho elegido, briefs de seguimiento. Se decide con datos de churn reales, no antes.
- **Responsable:** CPO · **Estado:** hipótesis a vigilar · **Revisión:** al tener 3 meses de datos de churn

## 4. Riesgos financieros (FIN)

### FIN-1 · CAC insostenible en el canal de pago
- **Descripción:** Meta Ads trae trials pero el coste por cliente convertido supera lo que el margen soporta.
- **Prob.:** Media · **Impacto:** Medio (el burn es pequeño y controlable) · **Prioridad:** MEDIA
- **Indicadores tempranos:** payback >6 meses ([11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) §2.1); coste por trial creciente 3 semanas seguidas.
- **Mitigación:** presupuesto contenido (5 €/día) hasta ver conversión real · regla escrita: no escalar gasto sin payback <3 meses demostrado · canal orgánico en paralelo.
- **Responsable:** CEO · **Estado:** vivo (campaña activa) · **Revisión:** semanal mientras haya gasto

### FIN-2 · Concentración de ingresos en un solo procesador (Stripe)
- **Prob.:** Baja · **Impacto:** Alto pero improbable · **Prioridad:** BAJA
- **Mitigación:** cumplimiento escrupuloso de términos · datos de suscripción replicados en BD propia (hecho) — con eso, migrar de procesador es doloroso pero posible.
- **Responsable:** CEO · **Estado:** aceptado · **Revisión:** anual

## 5. Riesgos legales (LEG)

### LEG-1 · Privacidad y datos personales (GDPR)
- **Descripción:** tratamos emails y datos de facturación de clientes (España/UE). Base actual: legal footer, privacidad publicada, Plausible sin cookies, minimización real de datos.
- **Prob.:** Baja (exposición minimizada por diseño) · **Impacto:** Medio · **Prioridad:** MEDIA
- **Indicadores tempranos:** solicitud de derechos (acceso/borrado) sin procedimiento; queja.
- **Mitigación:** procedimiento simple escrito de alta/baja/borrado de datos (pendiente, 1 página) · registro de subprocesadores (Railway, Stripe, Resend, Plausible, Meta) en la política (revisar que esté completo).
- **Responsable:** CEO · **Estado:** base sólida, formalización pendiente · **Revisión:** antes de 100 clientes

### LEG-2 · Uso de datos de fuentes públicas
- **Descripción:** los términos de uso de las fuentes (APIs públicas de GitHub/HN, feeds RSS) podrían cambiar o interpretarse restrictivamente.
- **Prob.:** Baja (uso de APIs públicas oficiales, volumen mínimo, con atribución y enlace a la fuente) · **Impacto:** Medio · **Prioridad:** BAJA
- **Mitigación:** solo APIs/feeds públicos y oficiales (hecho) · atribución visible (hecho) · revisión de términos al añadir cualquier fuente nueva (regla).
- **Responsable:** CTO · **Estado:** aceptado · **Revisión:** al añadir fuentes

## 6. Riesgos operativos (OP)

### OP-1 · Bus factor = 1 (el CEO es la única persona)
- **Descripción:** vacaciones, enfermedad o indisponibilidad del CEO detienen soporte, pagos, decisiones y cuentas (Stripe, Meta, Railway, dominio están a su nombre).
- **Prob.:** Alta (la vida ocurre) · **Impacto:** Alto sostenido / Bajo puntual · **Prioridad:** ALTA
- **Mitigación:** la automatización ya cubre la operación diaria (ingesta, cobros, emails corren solos) · runbooks y `/governance` reducen dependencia de memoria (en curso) · gestor de contraseñas con acceso de emergencia documentado (pendiente) · los agentes pueden diagnosticar y mitigar incidentes técnicos dentro de sus límites de autoridad ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §3).
- **Responsable:** CEO · **Estado:** parcial · **Revisión:** trimestral

### OP-2 · Canal de soporte desborda al CEO
- **Descripción:** con crecimiento, el soporte (formulario + email personal) consume el tiempo de la única persona.
- **Prob.:** Media (deseable: significaría tracción) · **Impacto:** Medio · **Prioridad:** MEDIA
- **Indicadores tempranos:** >1h/día en soporte durante 4 semanas ([01_COMPANY_CHART.md](01_COMPANY_CHART.md), disparador de Fase 1); tiempo de respuesta >48h.
- **Mitigación:** formulario centralizado con reply-to (hecho) · FAQ pública cuando los temas se repitan · primera contratación según organigrama.
- **Responsable:** CEO · **Estado:** vigilancia · **Revisión:** mensual

### OP-3 · Acción autónoma errónea de un agente
- **Descripción:** un agente ejecuta algo dañino fuera de sus límites (gasto, borrado, comunicación externa) por ambigüedad de instrucciones.
- **Prob.:** Baja (límites escritos + historial de respetarlos) · **Impacto:** Alto en el peor caso · **Prioridad:** MEDIA-ALTA
- **Mitigación:** límites de autoridad explícitos con lista de "jamás" ([01_COMPANY_CHART.md](01_COMPANY_CHART.md) §2) · interpretación restrictiva por defecto ante ambigüedad (§5) · acciones irreversibles requieren aprobación por acción, sin generalizar · reversibilidad por defecto en todo lo demás (soft-deletes, rollbacks).
- **Responsable:** CEO · **Estado:** gestionado por diseño · **Revisión:** trimestral

## 7. Riesgos de seguridad (SEC)

### SEC-1 · Compromiso de credenciales (Stripe live key, tokens, admin key)
- **Prob.:** Baja · **Impacto:** Alto (dinero real, datos de clientes) · **Prioridad:** ALTA
- **Indicadores tempranos:** actividad anómala en Stripe; llamadas admin no reconocidas; alertas de GitHub por secretos.
- **Mitigación:** secretos solo en env vars de Railway (hecho) · no persistencia de secretos usados en diagnóstico (práctica establecida) · rotación semestral o ante sospecha ([03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) §9.3) · fail-closed en endpoints admin (hecho).
- **Responsable:** Codex (auditoría) + Lead Engineer (ejecución) · **Estado:** gestionado · **Revisión:** mensual

### SEC-2 · Abuso de endpoints públicos (spam de signup/contact, scraping, fuerza bruta de códigos)
- **Prob.:** Media (todo endpoint público lo sufre tarde o temprano) · **Impacto:** Bajo-Medio (coste de Resend, ruido, degradación) · **Prioridad:** MEDIA
- **Indicadores tempranos:** picos de 429 en logs; consumo anómalo de Resend; signups basura.
- **Mitigación:** rate limiting por IP en escrituras públicas y auth (hecho: 5 req/15min en request-code) · códigos de 6 dígitos con caducidad de 10 min · validación estricta de inputs (hecho) · vigilancia de consumo en checklist mensual.
- **Responsable:** Lead Engineer · **Estado:** gestionado · **Revisión:** mensual

---

## 8. Metodología para mantener este registro vivo

1. **Entrada continua:** cualquier miembro añade riesgos en cualquier momento, sin permiso ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §5). Formato mínimo: descripción + probabilidad + impacto estimados; el Consejo lo calibra.
2. **Revisión mensual en Consejo** (sección expandida de §3.6 de [09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md)): por cada riesgo ALTA — ¿cambió la probabilidad? ¿se activó algún indicador temprano? ¿avanzó la mitigación pendiente? Riesgos MEDIA/BAJA: repaso trimestral.
3. **Bucle con incidentes:** todo postmortem ([08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) fase 11) responde: ¿estaba este riesgo registrado? Si no → se añade y se pregunta por qué no se vio. Si sí → se recalibra y se evalúa si la mitigación falló.
4. **Los riesgos se cierran, no se acumulan:** un riesgo cuya condición desapareció se marca cerrado con fecha y motivo (se conserva como historial). Un registro con 50 riesgos zombis no protege: anestesia.
5. **Regla de honestidad:** este registro existe para incomodar. Si dos revisiones seguidas no cambian nada en él, la sospecha correcta no es "estamos seguros", es "hemos dejado de mirar".
