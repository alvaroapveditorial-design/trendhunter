# /governance — El sistema operativo de AI Trend Hunter

Esta carpeta contiene el sistema completo de gobierno de la empresa: cómo se estructura, cómo funciona, cómo decide, cómo mide y cómo gestiona el riesgo. Los documentos forman un único sistema coherente con referencias cruzadas — no son doce documentos: son uno en doce capítulos.

**Cómo leerlo por primera vez:** empieza por [10_NORTH_STAR.md](10_NORTH_STAR.md) (por qué existimos), sigue con [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) (cómo funcionamos) y [01_COMPANY_CHART.md](01_COMPANY_CHART.md) (quién decide qué). El resto son manuales de área que se consultan cuando toca.

| Doc | Qué gobierna | Propietario |
|---|---|---|
| [01_COMPANY_CHART.md](01_COMPANY_CHART.md) | Organigrama, límites de autoridad, escalado, evolución 4→50 | CEO |
| [02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) | Cómo funciona la empresa (documento raíz) | CEO |
| [03_CTO_PLAYBOOK.md](03_CTO_PLAYBOOK.md) | Filosofía técnica, checklists, preparación por escala | CTO |
| [04_CPO_PLAYBOOK.md](04_CPO_PLAYBOOK.md) | Producto: PMF, validación, funnel, experimentos | CPO |
| [05_ENGINEERING_STANDARDS.md](05_ENGINEERING_STANDARDS.md) | Estándar de código, tests, CI/CD, seguridad | Lead Engineer |
| [06_PRODUCT_PRINCIPLES.md](06_PRODUCT_PRINCIPLES.md) | Los 16 principios de producto | CPO |
| [07_DECISION_FRAMEWORK.md](07_DECISION_FRAMEWORK.md) | Filtro, puntuación y registro de decisiones | CEO |
| [08_RELEASE_PROCESS.md](08_RELEASE_PROCESS.md) | El pipeline de release con checklists por fase | Lead Engineer |
| [09_WEEKLY_COUNCIL.md](09_WEEKLY_COUNCIL.md) | El Consejo de Dirección semanal y sus actas | CEO |
| [10_NORTH_STAR.md](10_NORTH_STAR.md) | La constitución: misión, visión, cultura, límites | CEO |
| [11_METRICS_PLAYBOOK.md](11_METRICS_PLAYBOOK.md) | Todas las métricas oficiales con fórmula y umbral | CPO + Lead Eng. |
| [12_RISK_REGISTER.md](12_RISK_REGISTER.md) | Registro vivo de riesgos con mitigaciones | CEO + Codex |

**Reglas de esta carpeta:**
- Los documentos son normativos: se cumplen, especialmente cuando estorban.
- Se cambian por commit con motivo, nunca por erosión ([02_OPERATING_SYSTEM.md](02_OPERATING_SYSTEM.md) §13).
- Si dos documentos se contradicen, gana `02_OPERATING_SYSTEM.md` hasta que el Consejo resuelva.
- Cada documento indica su propietario y su cadencia de revisión.
