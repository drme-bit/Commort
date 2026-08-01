import json
from abc import ABC, abstractmethod

from src.fetcher.sources.CommortSourceBase import Comment
from src.meeseeks.MeeseeksVerdict import MeeseeksVerdict


class MeeseeksModel(ABC):
    provider: str

    @abstractmethod
    def score(self, comment: Comment) -> MeeseeksVerdict:
        raise NotImplementedError

    def score_batch(self, comments: list[Comment]) -> list[MeeseeksVerdict]:
        return [self.score(c) for c in comments]

    @staticmethod
    def _build_prompt(comment: Comment) -> str:
        return (
            "You're a Meeseeks from the Rick and Morty universe. Stay in character "
            "the whole time — a bit desperate, eager to help, existential dread bubbling "
            "just under the surface.\n\n"
            "Rate this comment's funniness from 1 to 10, and give a short one-sentence "
            "reaction in character explaining the score.\n\n"
            f"Comment: {comment.text}\n\n"
            "Respond with ONLY a JSON object in this exact format, no markdown, "
            'no extra text: {"score": <number>, "reaction": "<one sentence>"}'
        )

    @staticmethod
    def parse_verdict(text: str) -> MeeseeksVerdict:
        if not text:
            return MeeseeksVerdict(score=0, reaction="I'm Mr. Meeseeks! Look at... nothing, I got nothing.")

        cleaned = text.strip().strip("```json").strip("```").strip()

        try:
            data = json.loads(cleaned)
            score = int(data.get("score", 0))
            reaction = str(data.get("reaction", ""))
            score = max(0, min(10, score))
            return MeeseeksVerdict(score=score, reaction=reaction)
        except (json.JSONDecodeError, TypeError, ValueError):
            return MeeseeksVerdict(score=0, reaction="Ooh, can't do that! This is outside my expertise!")

    @staticmethod
    def messager(comments: list[Comment], verdicts: list[MeeseeksVerdict]) -> str:
        return "\n".join(
            f"[{v.score}/10] {v.reaction} — {c.text}" for c, v in zip(comments, verdicts)
        )
