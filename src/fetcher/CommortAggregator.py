from src.fetcher.sources.CommortSourceBase import CommortSource, Comment

class CommortAgregator:
    def __init__(self, sources: list[CommortSource]):
        self.sources = sources

    def fetch_all(self) -> list[Comment]:
        comments = []
        for source in self.sources:
            comments += source.fetch()
        return comments

    def fetch_by_source(self, source: str) -> list[Comment]:
        return [c for c in self.fetch_all() if c.source == source]