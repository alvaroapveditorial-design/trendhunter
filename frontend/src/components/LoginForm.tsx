"use client";

import { FormEvent, useState } from "react";

import { track } from "@/lib/analytics";

type Step = "email" | "code";

export function LoginForm() {
  const [step, setStep] = useState<Step>("email");
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [devCode, setDevCode] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function requestCode(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setMessage("");
    setDevCode(null);

    try {
      const response = await fetch("/api/backend/api/v1/auth/request-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ email }),
      });
      const body = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(body?.detail || "We couldn't create the code.");
      }
      setDevCode(body.code ?? null);
      setStep("code");
      setMessage("We've sent you an access code.");
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "We couldn't create the code.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function verifyCode(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setMessage("");

    try {
      const response = await fetch("/api/backend/api/v1/auth/verify-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ email, code }),
      });
      const body = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(body?.detail || "Invalid or expired code.");
      }
      track("Login");
      window.location.href = body.has_active_subscription ? "/dashboard" : "/pricing";
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Invalid or expired code.");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="login-card">
      <span className="eyebrow">Private access</span>
      <h1>Sign in with your subscription email.</h1>
      <p>
        Use the same email you used to start your trial or subscription. If you don't have
        one, start on pricing.
      </p>

      {step === "email" ? (
        <form className="login-form" onSubmit={requestCode}>
          <label htmlFor="login-email">Email</label>
          <input
            id="login-email"
            type="email"
            autoComplete="email"
            placeholder="you@company.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Sending..." : "Send code"}
          </button>
        </form>
      ) : (
        <form className="login-form" onSubmit={verifyCode}>
          <label htmlFor="login-code">6-digit code</label>
          <input
            id="login-code"
            inputMode="numeric"
            maxLength={6}
            placeholder="123456"
            value={code}
            onChange={(event) => setCode(event.target.value.replace(/\D/g, "").slice(0, 6))}
            required
          />
          <button type="submit" disabled={isSubmitting || code.length !== 6}>
            {isSubmitting ? "Verifying..." : "Sign in"}
          </button>
          <button
            type="button"
            className="login-form__secondary"
            onClick={() => {
              setStep("email");
              setCode("");
              setDevCode(null);
            }}
          >
            Change email
          </button>
        </form>
      )}

      {devCode ? <p className="login-card__dev">Dev code: {devCode}</p> : null}
      {message ? <p className="login-card__message">{message}</p> : null}
      <a className="login-card__link" href="/pricing">
        Start 7-day trial
      </a>
    </div>
  );
}
