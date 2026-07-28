import { ContactForm } from "@/components/ContactForm";

export const metadata = {
  title: "Contact",
  description: "Get in touch with AI Trend Hunter support.",
};

export default function ContactPage() {
  return (
    <main className="landing-page login-page">
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
            <a href="/pricing" className="btn btn--primary">
              Try 7 days
            </a>
          </div>
        </div>
      </header>
      <section className="section login-section">
        <div className="container">
          <ContactForm />
        </div>
      </section>
    </main>
  );
}
