"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

/** Reports uncaught frontend errors as a Plausible custom event so failures
 * are visible without a dedicated error-tracking SDK on the client. Backend
 * exceptions are already captured by Sentry (see app/main.py). */
export function ErrorTracking() {
  useEffect(() => {
    const onError = (event: ErrorEvent) => {
      track("Frontend Error", {
        message: event.message.slice(0, 200),
        path: window.location.pathname,
      });
    };
    const onRejection = (event: PromiseRejectionEvent) => {
      const reason = event.reason instanceof Error ? event.reason.message : String(event.reason);
      track("Frontend Error", {
        message: `unhandled rejection: ${reason}`.slice(0, 200),
        path: window.location.pathname,
      });
    };

    window.addEventListener("error", onError);
    window.addEventListener("unhandledrejection", onRejection);
    return () => {
      window.removeEventListener("error", onError);
      window.removeEventListener("unhandledrejection", onRejection);
    };
  }, []);

  return null;
}
