export const metadata = {
  title: "Privacidad",
  description: "Politica de privacidad de AI Trend Hunter.",
};

export default function PrivacyPage() {
  return (
    <main className="legal-page">
      <section>
        <a href="/" className="legal-page__back">
          AI Trend Hunter
        </a>
        <h1>Politica de privacidad</h1>
        <p>
          Esta pagina resume como tratamos los datos necesarios para operar AI Trend
          Hunter. Antes de publicar, sustituye los datos del responsable por la entidad
          legal real.
        </p>

        <h2>Responsable</h2>
        <p>
          Responsable pendiente de completar: nombre legal, NIF/CIF, domicilio y email de
          contacto.
        </p>

        <h2>Datos tratados</h2>
        <ul>
          <li>Email de acceso y facturacion.</li>
          <li>Rol e intereses si solicitas acceso a beta.</li>
          <li>Estado de suscripcion sincronizado desde Stripe.</li>
          <li>Datos tecnicos imprescindibles para seguridad y funcionamiento.</li>
        </ul>

        <h2>Finalidades</h2>
        <ul>
          <li>Gestionar solicitudes de acceso, login y suscripciones.</li>
          <li>Permitir acceso al dashboard a usuarios con prueba o suscripcion activa.</li>
          <li>Enviar codigos de acceso y comunicaciones transaccionales.</li>
        </ul>

        <h2>Base legal</h2>
        <p>
          Ejecucion de contrato o medidas precontractuales para suscripcion/acceso, y
          consentimiento cuando solicites informacion o acceso a beta.
        </p>

        <h2>Pagos</h2>
        <p>
          Los pagos se procesan mediante Stripe. AI Trend Hunter no almacena datos completos
          de tarjeta.
        </p>

        <h2>Conservacion</h2>
        <p>
          Conservaremos los datos mientras exista relacion contractual, obligacion legal o
          hasta que solicites su supresion cuando proceda.
        </p>

        <h2>Derechos</h2>
        <p>
          Puedes solicitar acceso, rectificacion, supresion, oposicion, limitacion o
          portabilidad escribiendo al email de contacto que debe completarse antes del
          lanzamiento.
        </p>
      </section>
    </main>
  );
}
