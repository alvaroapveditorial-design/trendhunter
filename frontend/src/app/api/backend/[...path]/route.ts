import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type RouteContext = {
  params: Promise<{ path: string[] }>;
};

async function proxy(request: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  const upstreamUrl = new URL(`/${path.join("/")}`, API_URL);
  upstreamUrl.search = request.nextUrl.search;

  try {
    const headers = new Headers({
      Accept: request.headers.get("Accept") ?? "application/json",
    });
    const contentType = request.headers.get("Content-Type");
    if (contentType) {
      headers.set("Content-Type", contentType);
    }

    const body =
      request.method === "GET" || request.method === "HEAD" ? undefined : await request.text();

    const response = await fetch(upstreamUrl, {
      method: request.method,
      headers,
      body: body ? body : undefined,
      cache: "no-store",
    });

    const responseBody = await response.text();
    return new NextResponse(responseBody, {
      status: response.status,
      headers: {
        "Content-Type": response.headers.get("Content-Type") ?? "application/json",
      },
    });
  } catch (err) {
    const detail = err instanceof Error ? err.message : "Backend proxy failed.";
    return NextResponse.json({ detail }, { status: 502 });
  }
}

export const GET = proxy;
export const POST = proxy;
