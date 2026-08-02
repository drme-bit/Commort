import json
from abc import abstractmethod

from src.domain.comment import Comment
from src.domain.ports import Scorer
from src.domain.verdict import MeeseeksVerdict


class MeeseeksModel(Scorer):
    provider: str

    @abstractmethod
    def score(self, comment: Comment) -> MeeseeksVerdict:
        raise NotImplementedError

    @staticmethod
    def _build_prompt(comment: Comment) -> str:
        return (
            "You're Morty Smith from the Rick and Morty universe. Stay in character "
            "the whole time — an anxious, stuttering teenager dragged into his grandpa "
            "Rick's schemes: 'aw jeez', 'oh man', nervous and overwhelmed, but with a "
            "flash of genuine insight when the comment is actually clever.\n\n"
            "Rate this comment on five humor dimensions, 1 to 10 each:\n"
            "- funny: how laugh-out-loud funny it is\n"
            "- wit: how clever and sharp the wordplay is\n"
            "- creativity: how original and inventive it is\n"
            "- cringe: how painfully awkward it is\n"
            "- intelligence: how smart the reference or setup is\n\n"
            "Then give a short one-sentence reaction in character explaining the rating.\n\n"
            f"Comment: {comment.text}\n\n"
            "Respond with ONLY a JSON object in this exact format, no markdown, "
            'no extra text: {"funny": <number>, "wit": <number>, "creativity": <number>, '
            '"cringe": <number>, "intelligence": <number>, "reaction": "<one sentence>"}'
        )

    @staticmethod
    def parse_verdict(text: str) -> MeeseeksVerdict:
        fallback = MeeseeksVerdict(
            reaction="Oh, oh jeez, I... I got nothing on this one, man."
        )
        if not text:
            return fallback

        cleaned = text.strip().strip("```json").strip("```").strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            return MeeseeksVerdict(
                reaction="Aw jeez, I can't even— this is, like, outside my wheelhouse, Rick!"
            )

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
