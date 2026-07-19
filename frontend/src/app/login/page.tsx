import { LoginForm } from "@/components/LoginForm";

export const metadata = {
  title: "Login",
  description: "Accede a AI Trend Hunter con tu email de suscripcion.",
};

export default function LoginPage() {
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
              Probar 7 dias
            </a>
          </div>
        </div>
      </header>
      <section className="section login-section">
        <div className="container">
          <LoginForm />
        </div>
      </section>
    </main>
  );
}
