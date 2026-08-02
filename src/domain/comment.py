from dataclasses import asdict, dataclass


@dataclass
class Comment:
    id: str
    source: str
    text: str
    score: int
    author: str
    author_id: str = ""
    author_avatar: str = ""
    post_title: str = ""
    post_url: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
