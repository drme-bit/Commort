import time
from dataclasses import dataclass, field

from src.domain.comment import Comment
from src.domain.ports import CommentStore
from src.domain.verdict import MeeseeksVerdict
from src.service.views import comment_view, user_view


@dataclass
class StoredComment:
    comment: Comment
    verdict: MeeseeksVerdict | None = None
    fetched_at: float = field(default_factory=time.time)
    scored_at: float | None = None


class MemoryStore(CommentStore):
    def __init__(self):
        self._comments: dict[str, StoredComment] = {}

    async def connect(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def upsert_comments(self, comments: list[Comment]) -> list[Comment]:
        new = []
        for c in comments:
            stored = self._comments.get(c.id)
            if stored is None:
                self._comments[c.id] = StoredComment(comment=c)
                new.append(c)
            else:
                stored.comment.score = c.score
        return new

    async def list_unscored(self, limit: int = 20) -> list[Comment]:
        return [
            sc.comment for sc in self._comments.values() if sc.verdict is None
        ][:limit]

    async def mark_scored(self, comment: Comment, verdict: MeeseeksVerdict) -> None:
        stored = self._comments.get(comment.id)
        if stored is None:
            return
        stored.verdict = verdict
        stored.scored_at = time.time()

    async def list_comments(self, limit: int = 20, scored_only: bool = False) -> list[dict]:
        items = [sc for sc in self._comments.values() if not scored_only or sc.verdict]
        items.sort(key=lambda sc: sc.scored_at or sc.fetched_at, reverse=True)
        return [comment_view(sc.comment, sc.verdict, sc.fetched_at, sc.scored_at) for sc in items[:limit]]

    async def leaderboard(self, limit: int = 10) -> list[dict]:
        rated = [u for u in self._aggregate_users().values() if u["comments_count"] > 0]
        rated.sort(key=lambda u: (u["total_score"], u["best_score"]), reverse=True)
        return [user_view(u) for u in rated[:limit]]

    async def get_user(self, key: str) -> dict | None:
        for u in self._aggregate_users().values():
            if u["author_id"] == key or u["username"] == key:
                return user_view(u)
        return None

    def _aggregate_users(self) -> dict[str, dict]:
        users: dict[str, dict] = {}
        for sc in self._comments.values():
            if sc.verdict is None:
                continue
            c = sc.comment
            key = c.author_id or c.author
            u = users.setdefault(key, {
                "author_id": c.author_id,
                "username": c.author,
                "author_avatar": c.author_avatar,
                "total_score": 0,
                "comments_count": 0,
                "best_score": 0,
                "best_assessment": "",
                "last_seen": None,
            })
            u["author_avatar"] = c.author_avatar or u["author_avatar"]
            u["total_score"] += sc.verdict.score
            u["comments_count"] += 1
            u["last_seen"] = sc.scored_at
            if sc.verdict.score >= u["best_score"]:
                u["best_score"] = sc.verdict.score
                u["best_assessment"] = sc.verdict.assessment
        for u in users.values():
            if u["comments_count"]:
                u["avg_score"] = u["total_score"] / u["comments_count"]
        return users
