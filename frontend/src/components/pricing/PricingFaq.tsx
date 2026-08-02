const FAQ_ITEMS: Array<{ q: string; a: string }> = [
  {
    q: "Am I charged today?",
    a: "No. Your first charge happens when the 7-day trial ends, unless you cancel before then.",
  },
  {
    q: "Do I need to enter a card?",
    a: "Yes. Stripe asks for a card when you start checkout, even during the trial, but you're not charged until the trial ends.",
  },
  {
    q: "Can I cancel during the trial?",
    a: "Yes, through the billing portal, before the first charge.",
  },
  {
    q: "What sources does it analyze?",
    a: "GitHub, Hacker News, and selected RSS feeds.",
  },
  {
    q: "What happens if I cancel?",
    a: "If you cancel during the trial, you're not charged anything and lose access when the trial ends. If you cancel after the first charge, you keep access until the end of the period you already paid for, and the subscription won't renew.",
  },
  {
    q: "Is this investment advice?",
    a: "No. It's a research and decision-support tool.",
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
