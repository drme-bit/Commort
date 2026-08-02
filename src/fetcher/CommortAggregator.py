from src.domain.comment import Comment
from src.domain.ports import CommentFetcher


class CommortAggregator:
    def __init__(self, sources: list[CommentFetcher]):
        self.sources = sources

    def fetch(self, limit: int = 20) -> list[Comment]:
        comments: list[Comment] = []
        for source in self.sources:
            comments += source.fetch(limit)
        return comments
