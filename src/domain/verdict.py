from dataclasses import dataclass


@dataclass
class MeeseeksVerdict:
    funny: int = 5
    wit: int = 5
    creativity: int = 5
    cringe: int = 5
    intelligence: int = 5
    reaction: str = ""

    @property
    def humor_score(self) -> int:
        score = (
            0.50 * self.funny
            + 0.20 * self.wit
            + 0.15 * self.creativity
            + 0.15 * self.intelligence
        )
        return max(1, min(10, round(score)))

    def as_dict(self) -> dict:
        return {
            "funny": self.funny,
            "wit": self.wit,
            "creativity": self.creativity,
            "cringe": self.cringe,
            "intelligence": self.intelligence,
            "score": self.humor_score,
            "reaction": self.reaction,
        }
