import time

from openai import OpenAI, RateLimitError

from src.domain.comment import Comment
from src.domain.verdict import MeeseeksVerdict
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.meeseeks.prompt import build_prompt
from src.meeseeks.rate_limit import RateLimiter
from src.meeseeks.verdict_parser import parse_verdict


class OpenMeeseeks(MeeseeksModel):
    provider = "openrouter"

    def __init__(
        self,
        api_key: str,
        model: str = None,
        calls_per_minute: float = 15.0,
    ):
        self.model = model or "inclusionai/ling-3.0-flash:free"
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self._limiter = RateLimiter(calls_per_minute=calls_per_minute)

    def score(self, comment: Comment) -> MeeseeksVerdict:
        prompt = build_prompt(comment)
        response = self._create(prompt)
        return parse_verdict(response.choices[0].message.content)

    def _create(self, prompt: str):
        self._limiter.wait()
        for attempt in range(5):
            try:
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                )
            except RateLimitError as exc:
                if self._is_daily_limit(exc) or attempt == 4:
                    raise
                time.sleep(self._reset_delay(exc))
        raise RuntimeError("unreachable")

    @staticmethod
    def _is_daily_limit(exc: RateLimitError) -> bool:
        try:
            source = exc.body["error"]["metadata"]["limit_source"]
            return "daily" in source or "per_day" in source
        except (KeyError, TypeError):
            return False

    @staticmethod
    def _reset_delay(exc: RateLimitError) -> float:
        try:
            headers = exc.body["error"]["metadata"]["headers"]
            reset_ms = int(headers["X-RateLimit-Reset"])
            delay = (reset_ms / 1000.0) - time.time()
            return min(max(delay + 1.0, 2.0), 30.0)
        except (KeyError, TypeError, ValueError):
            return 10.0
