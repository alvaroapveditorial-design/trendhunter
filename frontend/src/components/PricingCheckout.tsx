"use client";

import { FormEvent, useState } from "react";

import { track } from "@/lib/analytics";

export function PricingCheckout() {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);
    track("Sign Up Started");
    track("Checkout Started");

    try {
      const response = await fetch("/api/backend/api/v1/billing/checkout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ email }),
      });
      const body = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(body?.detail || "We couldn't start checkout.");
      }
      window.location.href = body.checkout_url;
    } catch (err) {
      setIsSubmitting(false);
      const message = err instanceof Error ? err.message : "We couldn't start checkout.";
      setError(message);
      track("Checkout Failed", { reason: message.slice(0, 120) });
    }
  }

  return (
    <form className="pricing-checkout" onSubmit={onSubmit}>
      <label htmlFor="checkout-email">Billing email</label>
      <div className="pricing-checkout__row">
        <input
          id="checkout-email"
          name="email"
          type="email"
          autoComplete="email"
          placeholder="you@company.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Opening Stripe..." : "Start trial"}
        </button>
      </div>
      <p>
        7 days free. Then 39 EUR/month unless you cancel before the trial ends.
      </p>
      {error ? <p className="pricing-checkout__error">{error}</p> : null}
    </form>
  );
}
