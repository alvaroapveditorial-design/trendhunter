type PlausibleProps = Record<string, string | number | boolean>;

declare global {
  interface Window {
    plausible?: (event: string, options?: { props?: PlausibleProps }) => void;
  }
}

/** Fire a Plausible custom event. No-ops server-side or when the script hasn't loaded
 * (no Plausible domain configured, ad blocker, etc.) -- never throws. */
export function track(event: string, props?: PlausibleProps): void {
  if (typeof window === "undefined" || typeof window.plausible !== "function") {
    return;
  }
  try {
    window.plausible(event, props ? { props } : undefined);
  } catch {
    // Analytics must never break the app.
  }
}
