from dataclasses import dataclass


@dataclass
class MeeseeksVerdict:
    score: float = 0.0
    assessment: str = ""

    def as_dict(self) -> dict:
        return {
            "score": self.score,
            "assessment": self.assessment,
        }
