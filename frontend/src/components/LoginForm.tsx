"use client";

import { FormEvent, useState } from "react";

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
        throw new Error(body?.detail || "No hemos podido crear el codigo.");
      }
      setDevCode(body.code ?? null);
      setStep("code");
      setMessage("Te hemos enviado un codigo de acceso.");
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "No hemos podido crear el codigo.");
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
        throw new Error(body?.detail || "Codigo invalido o caducado.");
      }
      window.location.href = body.has_active_subscription ? "/dashboard" : "/pricing";
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Codigo invalido o caducado.");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="login-card">
      <span className="eyebrow">Acceso privado</span>
      <h1>Entra con tu email de suscripcion.</h1>
      <p>
        Usa el mismo email con el que iniciaste la prueba o suscripcion. Si no tienes una,
        empieza en pricing.
      </p>

      {step === "email" ? (
        <form className="login-form" onSubmit={requestCode}>
          <label htmlFor="login-email">Email</label>
          <input
            id="login-email"
            type="email"
            autoComplete="email"
            placeholder="tu@empresa.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Enviando..." : "Enviar codigo"}
          </button>
        </form>
      ) : (
        <form className="login-form" onSubmit={verifyCode}>
          <label htmlFor="login-code">Codigo de 6 digitos</label>
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
            {isSubmitting ? "Verificando..." : "Entrar"}
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
            Cambiar email
          </button>
        </form>
      )}

      {devCode ? <p className="login-card__dev">Codigo dev: {devCode}</p> : null}
      {message ? <p className="login-card__message">{message}</p> : null}
      <a className="login-card__link" href="/pricing">
        Empezar prueba de 7 dias
      </a>
    </div>
  );
}
