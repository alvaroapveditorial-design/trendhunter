"use client";

import { FormEvent, useState } from "react";

import { track } from "@/lib/analytics";

export function ContactForm() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "sent">("idle");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setError("");

    try {
      const response = await fetch("/api/backend/api/v1/support/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ email, message }),
      });
      const body = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(body?.detail || "We couldn't send your message.");
      }
      track("Support Contact Sent");
      setStatus("sent");
    } catch (err) {
      setError(err instanceof Error ? err.message : "We couldn't send your message.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (status === "sent") {
    return (
      <div className="login-card">
        <span className="eyebrow">Message sent</span>
        <h1>We got it.</h1>
        <p>We'll reply to {email} as soon as we can.</p>
        <a className="login-card__link" href="/">
          Back to home
        </a>
      </div>
    );
  }

  return (
    <div className="login-card">
      <span className="eyebrow">Support</span>
      <h1>Tell us what's going on.</h1>
      <p>We read every message and reply by email, usually within a day.</p>

      <form className="login-form" onSubmit={onSubmit}>
        <label htmlFor="contact-email">Email</label>
        <input
          id="contact-email"
          type="email"
          autoComplete="email"
          placeholder="you@company.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <label htmlFor="contact-message">Message</label>
        <textarea
          id="contact-message"
          placeholder="What do you need help with?"
          rows={5}
          minLength={10}
          maxLength={2000}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          required
        />
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Sending..." : "Send message"}
        </button>
      </form>

      {error ? <p className="login-card__message">{error}</p> : null}
    </div>
  );
}
