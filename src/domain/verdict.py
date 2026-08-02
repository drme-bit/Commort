from dataclasses import dataclass


@dataclass
class MeeseeksVerdict:
    score: int = 4
    assessment: str = ""

    def as_dict(self) -> dict:
        return {
            "score": self.score,
            "assessment": self.assessment,
        }
