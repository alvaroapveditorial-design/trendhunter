"""Beta signup API contract tests."""

from uuid import uuid4

from fastapi.testclient import TestClient

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
