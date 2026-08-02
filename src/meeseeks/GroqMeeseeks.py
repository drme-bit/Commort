import os

from dotenv import load_dotenv

from openai import OpenAI

from src.domain.comment import Comment
from src.domain.verdict import MeeseeksVerdict
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.meeseeks.prompt import build_prompt
from src.meeseeks.rate_limit import RateLimiter
from src.meeseeks.verdict_parser import parse_verdict


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
        prompt = build_prompt(comment)
        self._limiter.wait()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return parse_verdict(response.choices[0].message.content)
