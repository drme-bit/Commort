from abc import ABC, abstractmethod

from src.domain.comment import Comment
from src.domain.verdict import MeeseeksVerdict


class CommentFetcher(ABC):
    source: str

    @abstractmethod
    def fetch(self, limit: int = 20) -> list[Comment]:
        """Fetch comments from a platform."""
        raise NotImplementedError


class Scorer(ABC):
    provider: str

    @abstractmethod
    def score(self, comment: Comment) -> MeeseeksVerdict:
        raise NotImplementedError


class CommentStore(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def upsert_comments(self, comments: list[Comment]) -> list[Comment]:
        """Persist comments; return the ones that are new."""
        raise NotImplementedError

    @abstractmethod
    async def list_unscored(self, limit: int = 20) -> list[Comment]:
        raise NotImplementedError

    @abstractmethod
    async def mark_scored(self, comment: Comment, verdict: MeeseeksVerdict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_comments(self, limit: int = 20, scored_only: bool = False) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def leaderboard(self, limit: int = 10) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, key: str) -> dict | None:
        raise NotImplementedError


class Broadcaster(ABC):
    @abstractmethod
    async def broadcast(self, event: str, payload: dict) -> None:
        raise NotImplementedError
