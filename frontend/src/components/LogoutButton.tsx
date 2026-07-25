"use client";

import { useState } from "react";

import { track } from "@/lib/analytics";

export function LogoutButton() {
  const [isLoading, setIsLoading] = useState(false);

  async function logout() {
    setIsLoading(true);
    track("Logout");
    try {
      await fetch("/api/backend/api/v1/auth/logout", { method: "POST" });
    } finally {
      window.location.href = "/login";
    }
  }

  return (
    <button type="button" className="logout-button" onClick={logout} disabled={isLoading}>
      {isLoading ? "Signing out..." : "Log out"}
    </button>
  );
}
