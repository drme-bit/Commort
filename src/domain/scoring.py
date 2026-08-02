import math

from src.domain.comment import Comment
from src.domain.verdict import MeeseeksVerdict


def likes_score(likes: int) -> float:
    """Map comment like/score counts to a 1-10 scale (logarithmic)."""
    return min(10.0, 1 + 3 * math.log10(max(likes, 0) + 1))


def adaptive_score(comment: Comment, verdict: MeeseeksVerdict, alpha: float = 0.7) -> int:
    """Blend the Meeseeks humor verdict with the platform popularity."""
    return round(alpha * verdict.humor_score + (1 - alpha) * likes_score(comment.score))
