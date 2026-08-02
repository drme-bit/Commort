from src.domain.ports import CommentStore
from src.storage.MemoryStore import MemoryStore
from src.storage.PostgresStore import PostgresStore


def make_store(dsn: str | None) -> CommentStore:
    if dsn:
        return PostgresStore(dsn)
    return MemoryStore()
