"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

/** Instruments the (plain HTML, server-submitted) dashboard filter form
 * without turning it into a controlled React form -- attaches a submit
 * listener the same way LandingInteractions does for the beta form. */
export function DashboardFilterAnalytics() {
  useEffect(() => {
    const form = document.querySelector<HTMLFormElement>("form.filters");
    if (!form) return;

    const onSubmit = () => {
      const data = new FormData(form);
      const q = String(data.get("q") || "").trim();
      const category = String(data.get("category") || "");
      const sourceType = String(data.get("source_type") || "");
      const minScore = String(data.get("min_score") || "");

      if (q) {
        track("Search Used", { query_length: q.length });
      }
      if (category || sourceType || minScore) {
        track("Filter Used", {
          category: category || "none",
          source_type: sourceType || "none",
          min_score: minScore || "none",
        });
      }
    };

    form.addEventListener("submit", onSubmit);
    return () => form.removeEventListener("submit", onSubmit);
  }, []);

  return null;
}
