import math

from src.domain.comment import Comment
from src.domain.verdict import MeeseeksVerdict


def likes_score(likes: int) -> float:
    """Map comment like/score counts to a 1-10 scale (logarithmic)."""
    return min(10.0, 1 + 3 * math.log10(max(likes, 0) + 1))


def calibrate_score(raw: int) -> int:
    """Compress a raw 1-10 into a stingy final grade.

    A power curve squeezes everything below near-perfection down, so an 8-9
    is a genuinely rare score and a 10 is essentially unreachable.
    """
    return max(1, min(10, round(1 + 9 * ((raw - 1) / 9) ** 1.6)))


def adaptive_score(comment: Comment, verdict: MeeseeksVerdict, alpha: float = 0.7) -> int:
    """Blend the Meeseeks verdict with the platform popularity."""
    return round(alpha * verdict.score + (1 - alpha) * likes_score(comment.score))
