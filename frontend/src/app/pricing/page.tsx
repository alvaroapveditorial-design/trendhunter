import { PricingCheckout } from "@/components/PricingCheckout";

export const metadata = {
  title: "Pricing",
  description: "Prueba AI Trend Hunter durante 7 dias y continua con el plan Pro.",
};

export default function PricingPage() {
  return (
    <main className="landing-page pricing-page">
      <header className="nav">
        <div className="container nav__in">
          <a className="brand" href="/">
            <span className="brand__mark">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M3 17.5 9.2 11l3.6 3.3L21 6.5"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2.1"
                />
              </svg>
            </span>
            AI Trend Hunter
          </a>
          <div className="nav__cta">
            <a href="/dashboard" className="btn btn--ghost">
              Ver dashboard
            </a>
          </div>
        </div>
      </header>

      <section className="section pricing-hero">
        <div className="container pricing-hero__grid">
          <div className="pricing-copy">
            <span className="eyebrow">Plan Pro</span>
            <h1 className="display">Prueba AI Trend Hunter durante 7 dias.</h1>
            <p className="lead">
              Detecta oportunidades SaaS emergentes con senales publicas, scoring de
              tendencias y briefs accionables. Sin plan gratis abierto: una prueba corta
              para validar valor real.
            </p>
            <div className="hero__meta">
              <span>
                <b>39 EUR</b> / mes
              </span>
              <span>
                <b>7 dias</b> de prueba
              </span>
              <span>Cancela antes del primer cobro</span>
            </div>
          </div>

          <aside className="pricing-card">
            <div className="pricing-card__top">
              <span className="tag tag--accent">Pro</span>
              <strong>
                39 EUR <small>/mes</small>
              </strong>
              <p>Primer cobro despues de los 7 dias de prueba.</p>
            </div>
            <ul>
              <li>Dashboard de tendencias emergentes</li>
              <li>GitHub, Hacker News y RSS como fuentes iniciales</li>
              <li>Scores de oportunidad, momentum y saturacion</li>
              <li>Briefs accionables para ideas SaaS</li>
              <li>Historial de ejecuciones del pipeline</li>
            </ul>
            <PricingCheckout />
            <p className="pricing-card__fineprint">
              El checkout se procesa con Stripe. El cobro automatico empieza al terminar la
              prueba si no cancelas antes. Al continuar aceptas los{" "}
              <a href="/terms">terminos</a> y la <a href="/privacy">politica de privacidad</a>.
            </p>
          </aside>
        </div>
      </section>
    </main>
  );
}
