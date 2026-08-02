import asyncio
import json
from dataclasses import asdict, is_dataclass

from fastapi import WebSocket

from src.domain.ports import Broadcaster


class WSManager(Broadcaster):
    def __init__(self):
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)

    async def broadcast(self, event: str, payload: dict) -> None:
        message = json.dumps({"event": event, "data": payload}, default=_default)
        async with self._lock:
            targets = list(self._connections)

        for ws in targets:
            try:
                await ws.send_text(message)
            except Exception:
                await self.disconnect(ws)


def _default(obj):
    if is_dataclass(obj):
        return asdict(obj)
    return str(obj)
