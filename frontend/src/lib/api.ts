import type { AgentExecution, IngestionRun, Trend, TrendDetail } from "@/types/trend";

const SERVER_API_URL =
  process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const API_URL = typeof window === "undefined" ? SERVER_API_URL : PUBLIC_API_URL;

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    next: { revalidate: 30 },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getTrends(params?: {
  q?: string;
  category?: string;
  sourceType?: string;
  minScore?: number;
}): Promise<Trend[]> {
  const search = new URLSearchParams();
  if (params?.q) search.set("q", params.q);
  if (params?.category) search.set("category", params.category);
  if (params?.sourceType) search.set("source_type", params.sourceType);
  if (params?.minScore) search.set("min_score", String(params.minScore));

  const query = search.toString();
  return getJson<Trend[]>(`/api/v1/trends${query ? `?${query}` : ""}`);
}

export function getCategories(): Promise<string[]> {
  return getJson<string[]>("/api/v1/trends/meta/categories");
}

export function getSources(): Promise<string[]> {
  return getJson<string[]>("/api/v1/trends/meta/sources");
}

export function getTrend(slug: string): Promise<TrendDetail> {
  return getJson<TrendDetail>(`/api/v1/trends/${slug}`);
}

export function getIngestionRuns(): Promise<AgentExecution[]> {
  return getJson<AgentExecution[]>("/api/v1/ingestion/runs?limit=8");
}

export function runDemoIngestion(): Promise<IngestionRun> {
  return postJson<IngestionRun>("/api/v1/ingestion/demo");
}

export function runHackerNewsIngestion(): Promise<IngestionRun> {
  return postJson<IngestionRun>("/api/v1/ingestion/hackernews?feed=top&limit=10");
}
