export const metadata = {
  title: "Terms",
  description: "AI Trend Hunter terms of service.",
};

export default function TermsPage() {
  return (
    <main className="legal-page">
      <section>
        <a href="/" className="legal-page__back">
          AI Trend Hunter
        </a>
        <h1>Terms of service</h1>
        <p>
          These terms are an operational baseline for the commercial beta. They should be
          reviewed with legal counsel before public sale.
        </p>

        <h2>Service</h2>
        <p>
          AI Trend Hunter offers a dashboard to detect emerging SaaS trends from public
          sources such as GitHub, Hacker News, and RSS.
        </p>

        <h2>Subscription and trial</h2>
        <p>
          The Pro plan includes a 7-day trial. After the trial ends, Stripe charges 39
          EUR/month unless you cancel first.
        </p>

        <h2>Cancellation</h2>
        <p>
          You can cancel from the Stripe billing portal. Cancellation prevents future
          renewals, unless Stripe indicates otherwise during the process.
        </p>

        <h2>Acceptable use</h2>
        <p>
          You may not attempt to bypass access controls, abuse endpoints, resell
          unauthorized access, or use the service for illegal activities.
        </p>

        <h2>Availability</h2>
        <p>
          The product is in MVP/beta stage. There may be changes, interruptions, or
          limitations as sources, scoring, and features evolve.
        </p>

        <h2>Limitation</h2>
        <p>
          Scores and briefs are supporting information for research and decision-making,
          not guarantees of commercial, financial, or technical success.
        </p>
      </section>
    </main>
  );
}
