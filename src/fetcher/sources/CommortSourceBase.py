from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Comment:
    id: str
    source: str
    text: str
    score: int
    author: str
    author_id: str = ""
    post_title: str = ""
    post_url: str = ""


class CommortSource(ABC):
    source: str  # "reddit" | "youtube"

    @abstractmethod
    def fetch(self, limit: int = 20) -> list[Comment]:
        """fetch comments from the source."""
        raise NotImplementedError