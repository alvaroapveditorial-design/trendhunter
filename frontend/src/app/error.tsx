"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    track("Frontend Error", {
      message: error.message.slice(0, 200),
      path: window.location.pathname,
      boundary: "app-error",
    });
  }, [error]);

  return (
    <main className="shell">
      <section className="app-error">
        <p className="eyebrow">Something went wrong</p>
        <h1>We couldn&apos;t load this page</h1>
        <p>
          This is usually temporary. Retry in a few seconds — if it keeps happening,
          <a href="/contact"> contact support</a> and we&apos;ll take a look.
        </p>
        <button type="button" onClick={reset}>
          Retry
        </button>
      </section>
    </main>
  );
}
