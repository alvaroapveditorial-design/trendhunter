"""Tests for transactional email helpers."""

from app.services import email_service


class _FakeResponse:
    status_code = 200
    text = ""


class _FakeClient:
    def __init__(self, *args, **kwargs):
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def post(self, url, headers=None, json=None):
        _FakeClient.last_payload = json
        return _FakeResponse()


def test_login_code_email_sets_reply_to_when_support_email_configured(monkeypatch):
    monkeypatch.setattr(email_service.settings, "RESEND_API_KEY", "re_test")
    monkeypatch.setattr(email_service.settings, "SUPPORT_EMAIL", "support@example.com")
    monkeypatch.setattr(email_service.httpx, "Client", _FakeClient)

    result = email_service.send_login_code_email("user@example.com", "123456")

    assert result is True
    assert _FakeClient.last_payload["reply_to"] == ["support@example.com"]


def test_login_code_email_omits_reply_to_when_support_email_unset(monkeypatch):
    monkeypatch.setattr(email_service.settings, "RESEND_API_KEY", "re_test")
    monkeypatch.setattr(email_service.settings, "SUPPORT_EMAIL", "")
    monkeypatch.setattr(email_service.httpx, "Client", _FakeClient)

    result = email_service.send_login_code_email("user@example.com", "123456")

    assert result is True
    assert "reply_to" not in _FakeClient.last_payload
