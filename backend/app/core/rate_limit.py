"""Small in-memory rate limiter for MVP ingestion endpoints."""

from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock
from time import time


@dataclass(frozen=True)
class RateLimitDecision:
    """Result returned by the limiter."""

    allowed: bool
    remaining: int
    retry_after: int = 0


class InMemoryRateLimiter:
    """Sliding-window rate limiter.

    This is intentionally simple for the MVP. It works for a single process/container.
    A distributed deployment should replace it with Redis-backed rate limiting.
    """

    def __init__(self, max_requests: int, period_seconds: int):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, now: float | None = None) -> RateLimitDecision:
        """Check and record one request for a key."""
        current_time = now if now is not None else time()
        window_start = current_time - self.period_seconds

        with self._lock:
            timestamps = self._requests[key]
            while timestamps and timestamps[0] <= window_start:
                timestamps.popleft()

            if len(timestamps) >= self.max_requests:
                retry_after = max(1, int(timestamps[0] + self.period_seconds - current_time))
                return RateLimitDecision(
                    allowed=False,
                    remaining=0,
                    retry_after=retry_after,
                )

            timestamps.append(current_time)
            return RateLimitDecision(
                allowed=True,
                remaining=max(0, self.max_requests - len(timestamps)),
            )
