from __future__ import annotations

import asyncio
import logging

import orjson
from fastapi import WebSocket


class Broadcaster:
    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()
        self._lock = asyncio.Lock()
        self.logger = logging.getLogger("arbviz.broadcaster")

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._clients.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._clients.discard(websocket)

    async def broadcast(self, payload: dict) -> None:
        message = orjson.dumps(payload).decode()
        async with self._lock:
            clients = tuple(self._clients)
        if not clients:
            return
        results = await asyncio.gather(*(client.send_text(message) for client in clients), return_exceptions=True)
        for client, result in zip(clients, results, strict=True):
            if isinstance(result, Exception):
                await self.disconnect(client)
