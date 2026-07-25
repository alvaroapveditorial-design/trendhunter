"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

/** Fires one Plausible custom event when the page/section mounts. Used from
 * server components to log page-level events (e.g. "Pricing Viewed") that
 * Plausible's automatic pageview doesn't tag with our own event taxonomy. */
export function PageViewTracker({
  event,
  props,
}: {
  event: string;
  props?: Record<string, string | number | boolean>;
}) {
  const propsKey = JSON.stringify(props ?? {});
  useEffect(() => {
    track(event, props);
    // propsKey is a stable serialization of props, used instead of the object
    // reference so this doesn't re-fire on every parent re-render.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [event, propsKey]);

  return null;
}
