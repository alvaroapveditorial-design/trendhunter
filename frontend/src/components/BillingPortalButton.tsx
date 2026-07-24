"use client";

import { useState } from "react";

export function BillingPortalButton({ email }: { email: string }) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function openPortal() {
    setIsLoading(true);
    setError("");
    try {
      const response = await fetch("/api/backend/api/v1/billing/portal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ email }),
      });
      const body = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(body?.detail || "We couldn't open billing.");
      }
      window.location.href = body.portal_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "We couldn't open billing.");
      setIsLoading(false);
    }
  }

  return (
    <div className="billing-widget">
      <button type="button" onClick={openPortal} disabled={isLoading}>
        {isLoading ? "Opening..." : "Manage billing"}
      </button>
      {error ? <span>{error}</span> : null}
    </div>
  );
}
