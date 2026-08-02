"""Auth and paywall API contract tests."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.v1 import auth
from app.main import app
from app.models.base import Subscription
from app.models.database import SessionLocal


def test_login_code_flow_without_subscription():
    email = f"login-{uuid4()}@example.com"

    with TestClient(app) as client:
        request_response = client.post("/api/v1/auth/request-code", json={"email": email})
        assert request_response.status_code == 200
        code = request_response.json()["code"]

        verify_response = client.post(
            "/api/v1/auth/verify-code",
            json={"email": email, "code": code},
        )
        assert verify_response.status_code == 200
        assert verify_response.json()["email"] == email
        assert verify_response.json()["has_active_subscription"] is False

        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == 200
        assert me_response.json()["email"] == email


def test_login_code_flow_with_active_subscription():
    email = f"paid-login-{uuid4()}@example.com"
    db = SessionLocal()
    try:
        db.add(
            Subscription(
                id=str(uuid4()),
                email=email,
                plan="pro",
                status="trialing",
                stripe_subscription_id=f"sub_{uuid4()}",
            )
        )
        db.commit()
    finally:
        db.close()

    with TestClient(app) as client:
        code = client.post("/api/v1/auth/request-code", json={"email": email}).json()["code"]
        verify_response = client.post(
            "/api/v1/auth/verify-code",
            json={"email": email, "code": code},
        )

    assert verify_response.status_code == 200
    assert verify_response.json()["has_active_subscription"] is True
    assert verify_response.json()["subscription_status"] == "trialing"


def test_login_code_rejects_wrong_code():
    email = f"wrong-code-{uuid4()}@example.com"

    with TestClient(app) as client:
        client.post("/api/v1/auth/request-code", json={"email": email})
        response = client.post(
            "/api/v1/auth/verify-code",
            json={"email": email, "code": "000000"},
        )

    assert response.status_code == 401


def test_request_login_code_sends_email_when_configured(monkeypatch):
    email = f"email-send-{uuid4()}@example.com"
    sent = {}

    def fake_send_login_code_email(target_email: str, code: str) -> bool:
        sent["email"] = target_email
        sent["code"] = code
        return True

    monkeypatch.setattr(auth, "send_login_code_email", fake_send_login_code_email)
    monkeypatch.setattr(auth.settings, "ENVIRONMENT", "production")

    with TestClient(app) as client:
        response = client.post("/api/v1/auth/request-code", json={"email": email})

    assert response.status_code == 200
    assert response.json()["code"] is None
    assert sent["email"] == email
    assert len(sent["code"]) == 6


def test_request_login_code_fires_plausible_event(monkeypatch):
    email = f"email-track-{uuid4()}@example.com"
    monkeypatch.setattr(auth, "send_login_code_email", lambda *a, **k: True)

    calls = []
    monkeypatch.setattr(auth, "send_plausible_event", lambda *a, **k: calls.append(a))

    with TestClient(app) as client:
        response = client.post("/api/v1/auth/request-code", json={"email": email})

    assert response.status_code == 200
    assert len(calls) == 1
    assert calls[0][0] == "Login Code Requested"
