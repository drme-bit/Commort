import json

from src.domain.verdict import MeeseeksVerdict

_FALLBACK = MeeseeksVerdict(
    reaction="Oh, oh jeez, I... I got nothing on this one, man."
)
_UNPARSEABLE = MeeseeksVerdict(
    reaction="Aw jeez, I can't even— this is, like, outside my wheelhouse, Rick!"
)


def parse_verdict(text: str) -> MeeseeksVerdict:
    if not text:
        return _FALLBACK

    cleaned = text.strip().strip("```json").strip("```").strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return _UNPARSEABLE

    def num(key: str, default: int) -> int:
        try:
            value = int(data.get(key, default))
            return max(1, min(10, value))
        except (TypeError, ValueError):
            return default

    reaction = str(data.get("reaction", ""))
    if "funny" in data:
        return MeeseeksVerdict(
            funny=num("funny", 5),
            wit=num("wit", 5),
            creativity=num("creativity", 5),
            cringe=num("cringe", 5),
            intelligence=num("intelligence", 5),
            reaction=reaction,
        )

    # backward-compatible: single "score"
    score = num("score", 5)
    return MeeseeksVerdict(funny=score, wit=score, creativity=score, intelligence=score, reaction=reaction)
