from abc import abstractmethod

from src.domain.comment import Comment
from src.domain.ports import Scorer
from src.domain.verdict import MeeseeksVerdict


class MeeseeksModel(Scorer):
    provider: str

    @abstractmethod
    def score(self, comment: Comment) -> MeeseeksVerdict:
        raise NotImplementedError
