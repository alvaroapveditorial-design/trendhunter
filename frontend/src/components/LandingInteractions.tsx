"use client";

import { useEffect } from "react";

import { track } from "@/lib/analytics";

export function LandingInteractions() {
  useEffect(() => {
    track("Landing Viewed");

    const onCtaClick = (event: MouseEvent) => {
      const target = event.target as Element | null;
      const link = target?.closest<HTMLAnchorElement | HTMLButtonElement>(".btn");
      if (!link) return;
      track("CTA Clicked", {
        label: link.textContent?.trim().slice(0, 60) || "unknown",
        href: link instanceof HTMLAnchorElement ? link.getAttribute("href") || "" : "",
      });
    };
    document.addEventListener("click", onCtaClick);

    const nav = document.getElementById("nav");
    const onScroll = () => {
      if (!nav) return;
      nav.classList.toggle("is-stuck", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    const burger = document.getElementById("burger");
    const onBurgerClick = () => {
      window.location.href = "/pricing";
    };
    burger?.addEventListener("click", onBurgerClick);

    const filters = document.getElementById("filters");
    const grid = document.getElementById("sample-grid");
    const onFilterClick = (event: MouseEvent) => {
      const target = event.target as Element | null;
      const button = target?.closest<HTMLButtonElement>(".filter");
      if (!button || !filters || !grid) return;

      filters.querySelectorAll(".filter").forEach((filter) => filter.classList.remove("is-active"));
      button.classList.add("is-active");

      const category = button.getAttribute("data-cat");
      grid.querySelectorAll(".scard").forEach((card) => {
        const show = category === "all" || card.getAttribute("data-cat") === category;
        card.classList.toggle("is-hidden", !show);
      });
    };
    filters?.addEventListener("click", onFilterClick);

    const form = document.getElementById("beta-form") as HTMLFormElement | null;
    const success = document.getElementById("form-success");
    const formMicro = form?.querySelector<HTMLParagraphElement>(".form__micro");
    const chipsWrap = document.getElementById("chips");
    const interestsVal = document.getElementById("interests-val") as HTMLInputElement | null;
    const emailEl = document.getElementById("email") as HTMLInputElement | null;
    const roleEl = document.getElementById("role") as HTMLSelectElement | null;

    const syncInterests = () => {
      if (!chipsWrap || !interestsVal) return;
      const picked = Array.from(chipsWrap.querySelectorAll(".chip.is-on"))
        .map((chip) => chip.getAttribute("data-v"))
        .filter(Boolean);
      interestsVal.value = picked.join(", ");
    };

    const onChipClick = (event: MouseEvent) => {
      const target = event.target as Element | null;
      const chip = target?.closest<HTMLButtonElement>(".chip");
      if (!chip) return;
      chip.classList.toggle("is-on");
      chip.setAttribute("aria-pressed", chip.classList.contains("is-on") ? "true" : "false");
      syncInterests();
    };
    chipsWrap?.addEventListener("click", onChipClick);

    const setError = (fieldId: string, on: boolean) => {
      document.getElementById(fieldId)?.classList.toggle("has-error", on);
    };
    const validEmail = (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());

    const onEmailBlur = () => {
      if (emailEl?.value) setError("f-email", !validEmail(emailEl.value));
    };
    const onEmailInput = () => {
      const field = document.getElementById("f-email");
      if (field?.classList.contains("has-error") && emailEl && validEmail(emailEl.value)) {
        setError("f-email", false);
      }
    };
    const onRoleChange = () => setError("f-role", !roleEl?.value);

    emailEl?.addEventListener("blur", onEmailBlur);
    emailEl?.addEventListener("input", onEmailInput);
    roleEl?.addEventListener("change", onRoleChange);

    const onSubmit = async (event: SubmitEvent) => {
      event.preventDefault();
      if (!form || !emailEl || !roleEl || !success) return;

      const okEmail = validEmail(emailEl.value);
      const okRole = Boolean(roleEl.value);
      setError("f-email", !okEmail);
      setError("f-role", !okRole);
      if (!okEmail) {
        emailEl.focus();
        return;
      }
      if (!okRole) {
        roleEl.focus();
        return;
      }

      const button = document.getElementById("submit-btn") as HTMLButtonElement | null;
      if (button) {
        button.textContent = "Sending...";
        button.disabled = true;
      }
      if (formMicro) {
        formMicro.textContent = "Saving your request...";
      }

      try {
        const interests = interestsVal?.value
          ? interestsVal.value.split(",").map((item) => item.trim()).filter(Boolean)
          : [];
        const response = await fetch("/api/backend/api/v1/beta/signups", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            email: emailEl.value,
            role: roleEl.value,
            interests,
          }),
        });

        if (!response.ok) {
          const error = await response.json().catch(() => null);
          throw new Error(error?.detail || "We couldn't save your request.");
        }

        form.style.display = "none";
        success.classList.add("is-on");
        const line = document.getElementById("success-line");
        const picks = interestsVal?.value || "all categories";
        if (line) line.textContent = "-> " + emailEl.value + "  ·  " + picks;
        track("Beta Signup Completed", { role: roleEl.value });
      } catch (error) {
        if (button) {
          button.textContent = "Keep me posted";
          button.disabled = false;
        }
        if (formMicro) {
          formMicro.textContent =
            error instanceof Error
              ? error.message
              : "We couldn't save your request. Please try again.";
        }
      }
    };
    form?.addEventListener("submit", onSubmit);

    return () => {
      document.removeEventListener("click", onCtaClick);
      window.removeEventListener("scroll", onScroll);
      burger?.removeEventListener("click", onBurgerClick);
      filters?.removeEventListener("click", onFilterClick);
      chipsWrap?.removeEventListener("click", onChipClick);
      emailEl?.removeEventListener("blur", onEmailBlur);
      emailEl?.removeEventListener("input", onEmailInput);
      roleEl?.removeEventListener("change", onRoleChange);
      form?.removeEventListener("submit", onSubmit);
    };
  }, []);

  return null;
}
