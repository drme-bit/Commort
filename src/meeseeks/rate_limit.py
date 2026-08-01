import threading
import time


class RateLimiter:
    """Spaces calls so we never exceed calls_per_minute on the provider."""

    def __init__(self, calls_per_minute: float = 15.0):
        self.min_interval = 60.0 / calls_per_minute
        self._last = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            delay = self.min_interval - (now - self._last)
            if delay > 0:
                time.sleep(delay)
            self._last = time.monotonic()
