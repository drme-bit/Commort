import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.api.routes import build_router
from src.api.ws import WSManager
from src.config import Settings
from src.fetcher.CommortAggregator import CommortAggregator
from src.fetcher.sources.YoutubeSource import YoutubeSource
from src.meeseeks import make_meeseeks
from src.service.PollService import PollService
from src.storage import make_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("commort")


def create_app() -> FastAPI:
    settings = Settings.from_env()

    store = make_store(settings.database_url)
    source = CommortAggregator([YoutubeSource(api_key=settings.youtube_api_key)])
    meeseeks = make_meeseeks(settings)

    ws = WSManager()
    poll = PollService(
        store=store,
        source=source,
        meeseeks=meeseeks,
        ws=ws,
        interval_sec=settings.poll_interval_sec,
        fetch_limit=settings.fetch_limit,
        score_batch=settings.score_batch,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await store.connect()
        task = asyncio.create_task(poll.run_forever())
        app.state.poll_task = task
        logger.info("commort started, poller every %ss", settings.poll_interval_sec)
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
