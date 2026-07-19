export const metadata = {
  title: "Terminos",
  description: "Terminos de servicio de AI Trend Hunter.",
};

export default function TermsPage() {
  return (
    <main className="legal-page">
      <section>
        <a href="/" className="legal-page__back">
          AI Trend Hunter
        </a>
        <h1>Terminos de servicio</h1>
        <p>
          Estos terminos son una base operativa para la beta comercial. Deben revisarse con
          asesoramiento legal antes de venta publica.
        </p>

        <h2>Servicio</h2>
        <p>
          AI Trend Hunter ofrece un dashboard para detectar tendencias SaaS emergentes a
          partir de fuentes publicas como GitHub, Hacker News y RSS.
        </p>

        <h2>Suscripcion y prueba</h2>
        <p>
          El plan Pro incluye 7 dias de prueba. Al terminar la prueba, Stripe cobrara 39
          EUR/mes salvo cancelacion previa.
        </p>

        <h2>Cancelacion</h2>
        <p>
          Puedes cancelar desde el portal de facturacion de Stripe. La cancelacion evita
          renovaciones futuras, salvo que Stripe indique otra cosa durante el proceso.
        </p>

        <h2>Uso aceptable</h2>
        <p>
          No esta permitido intentar eludir controles de acceso, abusar de endpoints,
          revender acceso no autorizado o usar el servicio para actividades ilegales.
        </p>

        <h2>Disponibilidad</h2>
        <p>
          El producto esta en fase MVP/beta. Pueden existir cambios, interrupciones o
          limitaciones mientras evolucionan fuentes, scoring y funcionalidades.
        </p>

        <h2>Limitacion</h2>
        <p>
          Los scores y briefs son informacion de apoyo para investigacion y decision, no
          garantias de exito comercial, financiero o tecnico.
        </p>
      </section>
    </main>
  );
}
