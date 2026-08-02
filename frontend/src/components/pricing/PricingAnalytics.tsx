"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

/** Fires "How It Works Click" when the matching nav link is clicked. Uses
 * event delegation (same pattern as LandingInteractions) instead of an
 * onClick prop so the nav markup stays a plain server-rendered link. */
export function PricingAnalytics() {
  useEffect(() => {
    const onClick = (event: MouseEvent) => {
      const target = event.target as Element | null;
      const link = target?.closest<HTMLAnchorElement>('[data-track="how-it-works"]');
      if (!link) return;
      track("How It Works Click");
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  return null;
}
