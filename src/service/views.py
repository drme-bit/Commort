from datetime import datetime, timezone

from src.domain.comment import Comment
from src.domain.scoring import adaptive_score
from src.domain.verdict import MeeseeksVerdict


def iso(value: float | datetime | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    return value.astimezone().isoformat() if value.tzinfo else value.isoformat()


def comment_view(
    comment: Comment,
    verdict: MeeseeksVerdict | None,
    fetched_at: float | datetime | None,
    scored_at: float | datetime | None,
) -> dict:
    verdict_data = None
    if verdict is not None:
        verdict_data = verdict.as_dict()
        verdict_data["adaptive_score"] = adaptive_score(comment, verdict)
    return {
        "comment": comment.to_dict(),
        "verdict": verdict_data,
        "fetched_at": iso(fetched_at),
        "scored_at": iso(scored_at),
    }


def user_view(user: dict) -> dict:
    return {
        "author_id": user["author_id"],
        "username": user["username"],
        "author_avatar": user["author_avatar"],
        "total_score": int(user["total_score"]),
        "comments_count": int(user["comments_count"]),
        "avg_score": round(float(user["avg_score"]), 2),
        "best_score": int(user["best_score"]),
        "best_assessment": user["best_assessment"],
        "last_seen": user.get("last_seen"),
    }
