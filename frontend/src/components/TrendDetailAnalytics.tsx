"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

export function TrendDetailAnalytics({
  slug,
  category,
  hasOpportunities,
}: {
  slug: string;
  category: string;
  hasOpportunities: boolean;
}) {
  useEffect(() => {
    track("Trend Viewed", { slug, category });
    if (hasOpportunities) {
      track("Opportunity Viewed", { slug, category });
    }
    // Re-fire whenever the selected trend changes (each row click is a full
    // navigation, so this mounts fresh per trend).

    const FIRST_TREND_KEY = "ath_first_trend_opened";
    if (typeof window !== "undefined" && !window.sessionStorage.getItem(FIRST_TREND_KEY)) {
      window.sessionStorage.setItem(FIRST_TREND_KEY, "1");
      track("First Trend Opened", { slug, category });
    }
  }, [slug, category, hasOpportunities]);

  return null;
}
