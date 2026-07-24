export const metadata = {
  title: "Privacy",
  description: "AI Trend Hunter privacy policy.",
};

export default function PrivacyPage() {
  return (
    <main className="legal-page">
      <section>
        <a href="/" className="legal-page__back">
          AI Trend Hunter
        </a>
        <h1>Privacy policy</h1>
        <p>
          This page summarizes how we handle the data needed to operate AI Trend Hunter.
          Before publishing, replace the controller details with the real legal entity.
        </p>

        <h2>Data controller</h2>
        <p>
          Controller details pending: legal name, tax ID, address, and contact email.
        </p>

        <h2>Data we process</h2>
        <ul>
          <li>Login and billing email.</li>
          <li>Role and interests if you request beta access.</li>
          <li>Subscription status synced from Stripe.</li>
          <li>Technical data required for security and operation.</li>
        </ul>

        <h2>Purposes</h2>
        <ul>
          <li>Managing access requests, login, and subscriptions.</li>
          <li>Granting dashboard access to users with an active trial or subscription.</li>
          <li>Sending access codes and transactional communications.</li>
        </ul>

        <h2>Legal basis</h2>
        <p>
          Performance of a contract or pre-contractual steps for subscription/access, and
          consent when you request information or beta access.
        </p>

        <h2>Payments</h2>
        <p>
          Payments are processed through Stripe. AI Trend Hunter does not store full card
          data.
        </p>

        <h2>Retention</h2>
        <p>
          We retain data while a contractual relationship or legal obligation exists, or
          until you request deletion where applicable.
        </p>

        <h2>Your rights</h2>
        <p>
          You can request access, rectification, erasure, objection, restriction, or
          portability by writing to the contact email, which must be completed before
          launch.
        </p>
      </section>
    </main>
  );
}
