"""Billing API contract tests."""

import hashlib
import hmac
import json
import time
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.v1 import billing
from app.main import app
from app.models.base import Subscription
from app.models.database import SessionLocal


def _stripe_signature(payload: bytes, secret: str) -> str:
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload.decode('utf-8')}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def test_create_checkout_session(monkeypatch):
    def fake_create_session(email: str) -> dict:
        assert email == "founder@example.com"
        return {
            "id": "cs_test_123",
            "url": "https://checkout.stripe.com/c/pay/cs_test_123",
        }

    monkeypatch.setattr(billing, "create_stripe_checkout_session", fake_create_session)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/billing/checkout",
            json={"email": " Founder@Example.com "},
        )

    assert response.status_code == 200
    assert response.json() == {
        "session_id": "cs_test_123",
        "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_123",
    }


def test_create_checkout_session_requires_valid_email():
    with TestClient(app) as client:
        response = client.post("/api/v1/billing/checkout", json={"email": "nope"})

    assert response.status_code == 422


def test_create_billing_portal(monkeypatch):
    email = f"portal-{uuid4()}@example.com"
    customer_id = f"cus_{uuid4()}"
    db = SessionLocal()
    try:
        db.add(
            Subscription(
                id=str(uuid4()),
                email=email,
                plan="pro",
                status="active",
                stripe_customer_id=customer_id,
                stripe_subscription_id=f"sub_{uuid4()}",
            )
        )
        db.commit()
    finally:
        db.close()

    def fake_portal_session(stripe_customer_id: str) -> dict:
        assert stripe_customer_id == customer_id
        return {"url": "https://billing.stripe.com/session/test"}

    monkeypatch.setattr(billing, "create_stripe_billing_portal_session", fake_portal_session)

    with TestClient(app) as client:
        response = client.post("/api/v1/billing/portal", json={"email": email})

    assert response.status_code == 200
    assert response.json() == {"portal_url": "https://billing.stripe.com/session/test"}


def test_stripe_webhook_creates_subscription(monkeypatch):
    secret = "whsec_test_secret"
    email = f"paid-{uuid4()}@example.com"
    session_id = f"cs_test_{uuid4()}"
    subscription_id = f"sub_{uuid4()}"
    event = {
        "id": f"evt_{uuid4()}",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session_id,
                "customer": f"cus_{uuid4()}",
                "customer_email": email,
                "subscription": subscription_id,
                "subscription_status": "trialing",
            }
        },
    }
    payload = json.dumps(event, separators=(",", ":")).encode("utf-8")
    monkeypatch.setattr(billing.settings, "STRIPE_WEBHOOK_SECRET", secret)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/billing/webhook",
            content=payload,
            headers={
                "Content-Type": "application/json",
                "Stripe-Signature": _stripe_signature(payload, secret),
            },
        )

    assert response.status_code == 200
    assert response.json() == {"received": True}

    db = SessionLocal()
    try:
        subscription = (
            db.query(Subscription)
            .filter(Subscription.stripe_subscription_id == subscription_id)
            .first()
        )
        assert subscription is not None
        assert subscription.email == email
        assert subscription.status == "trialing"
        assert subscription.stripe_checkout_session_id == session_id
    finally:
        db.close()
