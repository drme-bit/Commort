import json
import os
import time

from dotenv import load_dotenv

from openai import OpenAI, RateLimitError

from src.fetcher.sources.CommortSourceBase import Comment
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.meeseeks.MeeseeksVerdict import MeeseeksVerdict
from src.meeseeks.rate_limit import RateLimiter


class OpenMeeseeks(MeeseeksModel):
    provider = "openrouter"

    def __init__(
        self,
        model: str = None,
        calls_per_minute: float = 15.0,
    ):
        load_dotenv()
        self.model = model or os.getenv("OPENROUTER_MODEL", "inclusionai/ling-3.0-flash:free")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self._limiter = RateLimiter(calls_per_minute=calls_per_minute)

    def score(self, comment: Comment) -> MeeseeksVerdict:
        prompt = self._build_prompt(comment)
        response = self._create(prompt)
        return self.parse_verdict(response.choices[0].message.content)

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
