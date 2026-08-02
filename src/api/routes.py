from fastapi import APIRouter, HTTPException, Query

from src.api.ws import WSManager
from src.domain.ports import CommentStore
from src.service.PollService import PollService


def build_router(store: CommentStore, poll: PollService, ws: WSManager) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/health")
    async def health():
        return {"status": "ok"}

    @router.get("/comments")
    async def comments(
        limit: int = Query(20, ge=1, le=100),
        scored_only: bool = Query(False),
    ):
        return await store.list_comments(limit=limit, scored_only=scored_only)

    @router.post("/comments/score")
    async def score_now(
        limit: int = Query(10, ge=1, le=50),
    ):
        scored = await poll.run_once(score_batch=limit)
        return {"scored": scored, "items": await store.list_comments(limit=limit, scored_only=True)}

    @router.get("/users")
    async def leaderboard(limit: int = Query(10, ge=1, le=100)):
        return await store.leaderboard(limit=limit)

    @router.get("/users/{key}")
    async def user_stats(key: str):
        user = await store.get_user(key)
        if user is None:
            raise HTTPException(status_code=404, detail="user not found")
        return user

    @router.get("/history")
    async def history(limit: int = Query(20, ge=1, le=100)):
        return await store.list_comments(limit=limit, scored_only=True)

    return router
