import json

from src.domain.scoring import calibrate_score
from src.domain.verdict import MeeseeksVerdict

_FALLBACK = MeeseeksVerdict(
    score=2,
    assessment="Aw jeez, I... I got nothing on this one, man.",
)
_UNPARSEABLE = MeeseeksVerdict(
    score=2,
    assessment="Aw jeez, I can't even read that, Rick, it's all, like, garbled.",
)


def parse_verdict(text: str) -> MeeseeksVerdict:
    if not text:
        return _FALLBACK

    cleaned = text.strip().strip("```json").strip("```").strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return _UNPARSEABLE

    raw = _number(data.get("score"), 4)
    assessment = str(data.get("assessment") or data.get("reaction") or "")
    return MeeseeksVerdict(score=calibrate_score(raw), assessment=assessment)


def _number(value, default: int) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default
