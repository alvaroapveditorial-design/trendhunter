"""Rate limiter tests."""

from app.core.rate_limit import InMemoryRateLimiter


def test_rate_limiter_allows_requests_within_window():
    limiter = InMemoryRateLimiter(max_requests=2, period_seconds=60)

    first = limiter.check("client", now=100)
    second = limiter.check("client", now=101)

    assert first.allowed is True
    assert first.remaining == 1
    assert second.allowed is True
    assert second.remaining == 0


def test_rate_limiter_blocks_when_window_is_full():
    limiter = InMemoryRateLimiter(max_requests=2, period_seconds=60)

    limiter.check("client", now=100)
    limiter.check("client", now=101)
    blocked = limiter.check("client", now=102)

    assert blocked.allowed is False
    assert blocked.remaining == 0
    assert blocked.retry_after == 58


def test_rate_limiter_reopens_after_window_expires():
    limiter = InMemoryRateLimiter(max_requests=1, period_seconds=60)

    limiter.check("client", now=100)
    reopened = limiter.check("client", now=161)

    assert reopened.allowed is True
    assert reopened.remaining == 0
