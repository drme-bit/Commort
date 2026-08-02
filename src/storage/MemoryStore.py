import time
from dataclasses import dataclass, field

from src.domain.comment import Comment
from src.domain.scoring import adaptive_score
from src.domain.verdict import MeeseeksVerdict


@dataclass
class StoredComment:
    comment: Comment
    verdict: MeeseeksVerdict | None = None
    fetched_at: float = field(default_factory=time.time)
    scored_at: float | None = None


class MemoryStore:
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
        return [self._view(sc) for sc in items[:limit]]

    async def leaderboard(self, limit: int = 10) -> list[dict]:
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
                "avg_score": 0.0,
                "best_score": 0,
                "best_reaction": "",
                "last_seen": None,
            })
            u["author_avatar"] = c.author_avatar or u["author_avatar"]
            u["total_score"] += sc.verdict.humor_score
            u["comments_count"] += 1
            u["last_seen"] = sc.scored_at
            if sc.verdict.humor_score >= u["best_score"]:
                u["best_score"] = sc.verdict.humor_score
                u["best_reaction"] = sc.verdict.reaction

        rated = [u for u in users.values() if u["comments_count"] > 0]
        for u in rated:
            u["avg_score"] = round(u["total_score"] / u["comments_count"], 2)
        rated.sort(key=lambda u: (u["total_score"], u["best_score"]), reverse=True)
        return rated[:limit]

    async def get_user(self, key: str) -> dict | None:
        for u in await self.leaderboard(limit=10**6):
            if u["author_id"] == key or u["username"] == key:
                return u
        return None

    @staticmethod
    def _view(sc: StoredComment) -> dict:
        verdict = None
        if sc.verdict:
            d = sc.verdict.as_dict()
            d["adaptive_score"] = adaptive_score(sc.comment, sc.verdict)
            verdict = d
        return {
            "comment": sc.comment.to_dict(),
            "verdict": verdict,
            "fetched_at": _iso(sc.fetched_at),
            "scored_at": _iso(sc.scored_at),
        }


def _iso(timestamp: float | None) -> str | None:
    if timestamp is None:
        return None
    from datetime import datetime, timezone

    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
