import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    youtube_api_key: str = ""
    openrouter_api_key: str = ""
    openrouter_model: str = "inclusionai/ling-3.0-flash:free"
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    meeseeks_provider: str = "groq"
    database_url: str = ""
    poll_interval_sec: int = 300
    fetch_limit: int = 5
    score_batch: int = 10

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            youtube_api_key=os.getenv("YOUTUBE_API_KEY", ""),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
            openrouter_model=os.getenv("OPENROUTER_MODEL", "inclusionai/ling-3.0-flash:free"),
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            groq_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            meeseeks_provider=os.getenv("MEESEEKS_PROVIDER", "groq"),
            database_url=os.getenv("DATABASE_URL", ""),
            poll_interval_sec=int(os.getenv("COMMORT_POLL_INTERVAL_SEC", "300")),
            fetch_limit=int(os.getenv("COMMORT_FETCH_LIMIT", "5")),
            score_batch=int(os.getenv("COMMORT_SCORE_BATCH", "10")),
        )
