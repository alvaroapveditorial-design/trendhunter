"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

type ActionKind = "demo" | "hackernews" | "rss" | "github";

async function runIngestion(kind: ActionKind) {
  const path =
    kind === "demo"
      ? "/api/v1/ingestion/demo"
      : kind === "hackernews"
        ? "/api/v1/ingestion/hackernews?feed=top&limit=10"
        : kind === "rss"
          ? "/api/v1/ingestion/rss?feed=techcrunch_startups&limit=10"
          : "/api/v1/ingestion/github?limit=10";

  const response = await fetch(`/api/backend${path}`, {
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
  const [runningAction, setRunningAction] = useState<ActionKind | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleRun(kind: ActionKind) {
    setRunningAction(kind);
    setMessage(null);
    setError(null);

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
  }

  const disabled = runningAction !== null;

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
      <button
        className="secondary-button"
        disabled={disabled}
        type="button"
        onClick={() => handleRun("github")}
      >
        {runningAction === "github" ? "Pulling..." : "Pull GitHub"}
      </button>
      {message ? <p className="action-message success">{message}</p> : null}
      {error ? <p className="action-message error">{error}</p> : null}
    </div>
  );
}
