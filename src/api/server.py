import asyncio
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.api.routes import build_router
from src.api.ws import WSManager
from src.fetcher.CommortAggregator import CommortAggregator
from src.fetcher.sources.YoutubeSource import YoutubeSource
from src.meeseeks import make_meeseeks
from src.service.PollService import PollService
from src.storage import make_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("commort")


def create_app() -> FastAPI:
    load_dotenv()

    store = make_store()
    source = CommortAggregator([YoutubeSource()])
    meeseeks = make_meeseeks()

    ws = WSManager()
    poll = PollService(
        store=store,
        source=source,
        meeseeks=meeseeks,
        ws=ws,
        interval_sec=int(os.getenv("COMMORT_POLL_INTERVAL_SEC", "300")),
        fetch_limit=int(os.getenv("COMMORT_FETCH_LIMIT", "5")),
        score_batch=int(os.getenv("COMMORT_SCORE_BATCH", "10")),
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await store.connect()
        task = asyncio.create_task(poll.run_forever())
        app.state.poll_task = task
        logger.info("commort started, poller every %ss", poll._interval)
        yield
        task.cancel()
        await store.close()

    app = FastAPI(title="Commort API", lifespan=lifespan)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await ws.connect(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await ws.disconnect(websocket)

    app.include_router(build_router(store, poll, ws))
    return app


app = create_app()
