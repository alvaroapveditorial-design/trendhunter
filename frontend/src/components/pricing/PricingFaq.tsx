const FAQ_ITEMS: Array<{ q: string; a: string }> = [
  {
    q: "¿Me cobran hoy?",
    a: "No. El primer cobro se realiza al terminar los siete días de prueba, salvo cancelación previa.",
  },
  {
    q: "¿Necesito introducir tarjeta?",
    a: "Sí. Stripe pide una tarjeta al iniciar el checkout, incluso durante el periodo de prueba, pero no se realiza ningún cargo hasta que termina.",
  },
  {
    q: "¿Puedo cancelar durante el trial?",
    a: "Sí, mediante el portal de facturación, antes del primer cobro.",
  },
  {
    q: "¿Qué fuentes analiza?",
    a: "GitHub, Hacker News y feeds RSS seleccionados.",
  },
  {
    q: "¿Qué ocurre si cancelo?",
    a: "Si cancelas durante el trial, no se te cobra nada y pierdes el acceso al terminar el periodo de prueba. Si cancelas después del primer cobro, mantienes el acceso hasta el final del periodo ya pagado y la suscripción no se renueva.",
  },
  {
    q: "¿Es una recomendación de inversión?",
    a: "No. Es una herramienta de investigación y apoyo a decisiones.",
  },
];

export function PricingFaq() {
  return (
    <section className="section" id="faq">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">FAQ</span>
          <h2 className="h2">Before you start the trial.</h2>
        </div>
        <div style={{ display: "grid", gap: 12, maxWidth: 720 }}>
          {FAQ_ITEMS.map((item) => (
            <details
              key={item.q}
              style={{
                border: "1px solid var(--line)",
                borderRadius: 8,
                padding: "14px 18px",
                background: "var(--surface)",
              }}
            >
              <summary style={{ cursor: "pointer", fontWeight: 600 }}>{item.q}</summary>
              <p style={{ marginTop: 10, color: "var(--ink-soft)", fontSize: 14.5, lineHeight: 1.55 }}>
                {item.a}
              </p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}
