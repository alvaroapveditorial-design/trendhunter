# Phoenix Fase 2 — Baseline

**Fecha de captura:** 2 de agosto de 2026, antes de cualquier cambio de código de esta fase.
**Fuente:** Meta Ads Manager (cuenta Duskwell Ads, campaña "Nueva campaña de Tráfico"), Plausible (`aitrendhunter.app`), base de datos de producción (`subscriptions`).

## Campaña (28 jul – 2 ago, ahora pausada)

| Métrica | Valor |
|---|---|
| Clics en el enlace | ~90 |
| Visitas a página de destino (Meta) | ~84 |
| CPC | ~0,28 € |
| Coste por visita | ~0,30 € |
| Gasto total | ~25,3 € (hasta el momento de la pausa) |
| Trials creados en `subscriptions` desde el lanzamiento | **0** |
| Conversión visita → trial | **0%** |
| % del tráfico de Facebook que aterriza en `/pricing` (Plausible, entry pages) | **88,7%** (47 de 53 visitantes únicos) |

## Eventos de conversión — estado histórico en Plausible

Verificado en el panel de Plausible (rango 1 jul – 2 ago 2026, sitio `aitrendhunter.app`), pestaña Goals: **no hay Goals configurados** para ninguno de los 12 eventos requeridos en el brief. Plausible registra eventos custom enviados vía `window.plausible()` o la Events API aunque no tengan un Goal explícito configurado, pero sin un Goal no aparecen desglosados en el panel de reporting estándar que he podido inspeccionar en esta sesión.

**No invento cifras que no puedo verificar.** Lo que sí puedo confirmar con evidencia de código (no de reporting):
- `Checkout Started` — el código ya lo dispara (`PricingCheckout.tsx`) desde antes de esta fase, así que existen eventos históricos, pero no tengo una cifra exacta verificada en el dashboard de Plausible en esta sesión.
- `Trial Started` — el código ya lo dispara server-side en el webhook de Stripe (`billing.py`) para pagos completados; con 0 trials reales desde el lanzamiento de campaña, el conteo esperado en el periodo de campaña es 0.
- `Pricing CTA Clicked`, `Checkout Created`, `Stripe Checkout Completed`, `Login Code Requested`, `First Trend Opened` — **no existían en el código antes de esta fase.** Su histórico es, por definición, cero porque nunca se dispararon.

**Acción recomendada tras el despliegue de esta fase:** configurar Goals en Plausible para los 12 eventos del `ANALYTICS_EVENT_MAP.md`, para que las próximas mediciones sí sean auditables directamente desde el panel sin depender de consultas manuales.

## Conclusión

La línea base de conversión es, sin ambigüedad, **cero** en el tramo medible (visita → trial). El resto de esta fase se mide contra este cero.
