"use client";

import { FormEvent, useState } from "react";

export function PricingCheckout() {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

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
        throw new Error(body?.detail || "No hemos podido iniciar el checkout.");
      }
      window.location.href = body.checkout_url;
    } catch (err) {
      setIsSubmitting(false);
      setError(err instanceof Error ? err.message : "No hemos podido iniciar el checkout.");
    }
  }

  return (
    <form className="pricing-checkout" onSubmit={onSubmit}>
      <label htmlFor="checkout-email">Email de facturación</label>
      <div className="pricing-checkout__row">
        <input
          id="checkout-email"
          name="email"
          type="email"
          autoComplete="email"
          placeholder="tu@empresa.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Abriendo Stripe..." : "Empezar prueba"}
        </button>
      </div>
      <p>
        7 dias gratis. Despues, 39 EUR/mes salvo cancelacion antes de que termine la
        prueba.
      </p>
      {error ? <p className="pricing-checkout__error">{error}</p> : null}
    </form>
  );
}
