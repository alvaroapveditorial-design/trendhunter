"""Support contact-form API contract tests."""

from fastapi.testclient import TestClient

from app.api.v1 import support
from app.main import app


def test_create_support_contact_relays_email(monkeypatch):
    captured = {}

    def fake_send(email: str, message: str) -> bool:
        captured["email"] = email
        captured["message"] = message
        return True

    monkeypatch.setattr(support, "send_support_contact_email", fake_send)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/support/contact",
            json={"email": "user@example.com", "message": "I can't log in, please help."},
        )

    assert response.status_code == 202
    assert response.json() == {"received": True}
    assert captured == {"email": "user@example.com", "message": "I can't log in, please help."}


def test_create_support_contact_requires_valid_email(monkeypatch):
    monkeypatch.setattr(support, "send_support_contact_email", lambda *a, **k: True)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/support/contact",
            json={"email": "nope", "message": "I can't log in, please help."},
        )

    assert response.status_code == 422


def test_create_support_contact_requires_nonempty_message(monkeypatch):
    monkeypatch.setattr(support, "send_support_contact_email", lambda *a, **k: True)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/support/contact",
            json={"email": "user@example.com", "message": "too short"},
        )

    assert response.status_code == 422


def test_create_support_contact_does_not_fail_when_relay_fails(monkeypatch):
    """Matches the rest of the app's email endpoints: a Resend failure never
    surfaces as an HTTP error, since the client has no way to retry a lost
    message anyway."""
    monkeypatch.setattr(support, "send_support_contact_email", lambda *a, **k: False)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/support/contact",
            json={"email": "user@example.com", "message": "I can't log in, please help."},
        )

    assert response.status_code == 202
