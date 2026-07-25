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
        <p className="eyebrow">Dashboard error</p>
        <h1>Could not load AI Trend Hunter</h1>
        <p>
          Check that the backend is running on `http://localhost:8000`, then retry the
          dashboard.
        </p>
        <pre>{error.message}</pre>
        <button type="button" onClick={reset}>
          Retry
        </button>
      </section>
    </main>
  );
}
