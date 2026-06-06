"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

import { API_URL } from "@/lib/api";

type ActionKind = "demo" | "hackernews" | "rss";

async function runIngestion(kind: ActionKind) {
  const path =
    kind === "demo"
      ? "/api/v1/ingestion/demo"
      : kind === "hackernews"
        ? "/api/v1/ingestion/hackernews?feed=top&limit=10"
        : "/api/v1/ingestion/rss?feed=techcrunch_startups&limit=10";

  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    cache: "no-store",
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail ?? `Ingestion failed with status ${response.status}`);
  }

  return response.json();
}

export function IngestionActions() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [runningAction, setRunningAction] = useState<ActionKind | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function handleRun(kind: ActionKind) {
    setRunningAction(kind);
    setMessage(null);
    setError(null);

    startTransition(async () => {
      try {
        const result = await runIngestion(kind);
        setMessage(
          `${result.processed_signals} signals processed. ${result.created_trends} created, ${result.updated_trends} updated.`
        );
        router.refresh();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Could not run ingestion.");
      } finally {
        setRunningAction(null);
      }
    });
  }

  const disabled = isPending || runningAction !== null;

  return (
    <div className="ingestion-actions">
      <button disabled={disabled} type="button" onClick={() => handleRun("demo")}>
        {runningAction === "demo" ? "Running demo..." : "Run demo ingestion"}
      </button>
      <button
        className="secondary-button"
        disabled={disabled}
        type="button"
        onClick={() => handleRun("hackernews")}
      >
        {runningAction === "hackernews" ? "Pulling..." : "Pull Hacker News"}
      </button>
      <button
        className="secondary-button"
        disabled={disabled}
        type="button"
        onClick={() => handleRun("rss")}
      >
        {runningAction === "rss" ? "Pulling..." : "Pull RSS"}
      </button>
      {message ? <p className="action-message success">{message}</p> : null}
      {error ? <p className="action-message error">{error}</p> : null}
    </div>
  );
}
