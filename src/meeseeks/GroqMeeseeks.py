import os

from dotenv import load_dotenv

from openai import OpenAI

from src.fetcher.sources.CommortSourceBase import Comment
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.meeseeks.MeeseeksVerdict import MeeseeksVerdict
from src.meeseeks.rate_limit import RateLimiter


class GroqMeeseeks(MeeseeksModel):
    provider = "groq"

    def __init__(
        self,
        model: str = None,
        calls_per_minute: float = 15.0,
    ):
        load_dotenv()
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
        )
        self._limiter = RateLimiter(calls_per_minute=calls_per_minute)

    def score(self, comment: Comment) -> MeeseeksVerdict:
        prompt = self._build_prompt(comment)
        self._limiter.wait()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return self.parse_verdict(response.choices[0].message.content)
