import asyncio
import logging

from src.domain.ports import CommentFetcher, CommentStore
from src.meeseeks.MeeseeksModel import MeeseeksModel
from src.api.ws import WSManager

logger = logging.getLogger("commort.poll")


class PollService:
    def __init__(
        self,
        store: CommentStore,
        source: CommentFetcher,
        meeseeks: MeeseeksModel,
        ws: WSManager,
        interval_sec: int = 300,
        fetch_limit: int = 5,
        score_batch: int = 10,
    ):
        self._store = store
        self._source = source
        self._meeseeks = meeseeks
        self._ws = ws
        self._interval = interval_sec
        self._fetch_limit = fetch_limit
        self._score_batch = score_batch

    async def run_once(self, score_batch: int | None = None) -> int:
        comments = await asyncio.to_thread(self._source.fetch, self._fetch_limit)
        new = await self._store.upsert_comments(comments)
        logger.info("fetched %s comments, %s new", len(comments), len(new))

        batch = score_batch or self._score_batch
        unscored = await self._store.list_unscored(limit=batch)
        scored = 0
        for comment in unscored:
            verdict = await asyncio.to_thread(self._meeseeks.score, comment)
            await self._store.mark_scored(comment, verdict)
            await self._ws.broadcast("comment_scored", {
                "comment": comment.to_dict(),
                "verdict": verdict.as_dict(),
            })
            scored += 1

        logger.info("scored %s comments", scored)
        return scored

    async def run_forever(self) -> None:
        while True:
            try:
                await self.run_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("poll cycle failed")
            await asyncio.sleep(self._interval)
