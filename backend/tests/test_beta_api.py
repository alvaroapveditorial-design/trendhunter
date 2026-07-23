"""Beta signup API contract tests."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


def test_create_beta_signup():
    email = f"founder-{uuid4()}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/beta/signups",
            json={
                "email": f" {email.upper()} ",
                "role": "Founder / cofundador",
                "interests": ["AI infra", "AI infra", "Dev tools"],
            },
        )

    assert response.status_code == 201
    signup = response.json()
    assert signup["email"] == email
    assert signup["role"] == "Founder / cofundador"
    assert signup["interests"] == ["AI infra", "Dev tools"]
    assert signup["status"] == "new"
    assert signup["already_registered"] is False


def test_create_beta_signup_is_idempotent_by_email():
    email = f"repeat-{uuid4()}@example.com"
    payload = {
        "email": email,
        "role": "Product manager",
        "interests": ["Fintech"],
    }

    with TestClient(app) as client:
        first = client.post("/api/v1/beta/signups", json=payload)
        second = client.post(
            "/api/v1/beta/signups",
            json={**payload, "role": "Founder / cofundador", "interests": ["AI infra"]},
        )

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["id"] == first.json()["id"]
    assert second.json()["already_registered"] is True
    assert second.json()["role"] == "Product manager"


def test_create_beta_signup_rejects_invalid_email():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/beta/signups",
            json={"email": "not-an-email", "role": "Founder", "interests": []},
        )

    assert response.status_code == 422


def test_list_beta_signups_requires_admin_key_configured():
    get_settings.cache_clear()

    with TestClient(app) as client:
        response = client.get("/api/v1/beta/signups", headers={"X-Admin-Key": "whatever"})

    get_settings.cache_clear()
    assert response.status_code == 401


def test_list_beta_signups_rejects_wrong_key(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "top-secret")
    get_settings.cache_clear()

    with TestClient(app) as client:
        response = client.get("/api/v1/beta/signups", headers={"X-Admin-Key": "wrong"})

    get_settings.cache_clear()
    assert response.status_code == 401


def test_list_beta_signups_returns_newest_first(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY", "top-secret")
    get_settings.cache_clear()

    email_a = f"list-a-{uuid4()}@example.com"
    email_b = f"list-b-{uuid4()}@example.com"

    with TestClient(app) as client:
        client.post(
            "/api/v1/beta/signups",
            json={"email": email_a, "role": "Founder", "interests": []},
        )
        client.post(
            "/api/v1/beta/signups",
            json={"email": email_b, "role": "Founder", "interests": []},
        )
        response = client.get("/api/v1/beta/signups", headers={"X-Admin-Key": "top-secret"})

    get_settings.cache_clear()
    assert response.status_code == 200
    emails = [signup["email"] for signup in response.json()]
    assert emails.index(email_b) < emails.index(email_a)
