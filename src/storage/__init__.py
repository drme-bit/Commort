import os

from dotenv import load_dotenv

from src.storage.MemoryStore import MemoryStore
from src.storage.PostgresStore import PostgresStore


def make_store():
    load_dotenv()
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return PostgresStore(dsn)
    return MemoryStore()
