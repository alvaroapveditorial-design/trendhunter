import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type RouteContext = {
  params: Promise<{ path: string[] }>;
};

async function proxy(request: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  const upstreamUrl = new URL(`/${path.join("/")}`, API_URL);
  upstreamUrl.search = request.nextUrl.search;

  const response = await fetch(upstreamUrl, {
    method: request.method,
    headers: {
      "Content-Type": request.headers.get("Content-Type") ?? "application/json",
      Accept: request.headers.get("Accept") ?? "application/json",
    },
    body: request.method === "GET" || request.method === "HEAD" ? undefined : await request.text(),
    cache: "no-store",
  });

  const body = await response.text();
  return new NextResponse(body, {
    status: response.status,
    headers: {
      "Content-Type": response.headers.get("Content-Type") ?? "application/json",
    },
  });
}

export const GET = proxy;
export const POST = proxy;
