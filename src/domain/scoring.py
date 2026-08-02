import math

from src.domain.comment import Comment
from src.domain.verdict import MeeseeksVerdict


def likes_score(likes: int) -> float:
    """Map comment like/score counts to a 1-10 scale (logarithmic)."""
    return min(10.0, 1 + 3 * math.log10(max(likes, 0) + 1))


def normalize_score(value: float) -> float:
    """Round a raw score to one decimal and clamp it to the 0.0-10.0 scale."""
    return round(max(0.0, min(10.0, value)), 1)


def adaptive_score(comment: Comment, verdict: MeeseeksVerdict, alpha: float = 0.7) -> float:
    """Blend the Meeseeks verdict with the platform popularity."""
    return round(alpha * verdict.score + (1 - alpha) * likes_score(comment.score), 1)
