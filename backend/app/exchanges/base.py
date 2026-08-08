from __future__ import annotations

import abc
import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

import orjson
import websockets
from websockets.asyncio.client import ClientConnection

from app.models import BookUpdate

UpdateHandler = Callable[[BookUpdate], Awaitable[None]]


class ExchangeConnector(abc.ABC):
    """Isolated resilient public-feed adapter. It never knows about arbitrage."""

    exchange: str
    url: str
    # Most venues support RFC 6455 ping frames. Connectors can opt out when an
    # exchange specifies an application-level heartbeat instead.
    ping_interval: float | None = 20
    ping_timeout: float | None = 10
    heartbeat_interval: float | None = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"arbviz.exchange.{self.exchange}")
        self._ws: ClientConnection | None = None

    async def connect(self) -> ClientConnection:
        self._ws = await websockets.connect(
            self.url,
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout,
            max_size=2**20,
        )
        self._log(logging.INFO, "connected")
        return self._ws

    @abc.abstractmethod
    async def subscribe(self, ws: ClientConnection) -> None: ...

    @abc.abstractmethod
    def parse(self, message: dict[str, Any], received: float) -> BookUpdate | None: ...

    async def receive(self, ws: ClientConnection, handler: UpdateHandler) -> None:
        while True:
            try:
                if self.heartbeat_interval is None:
                    raw = await ws.recv()
                else:
                    raw = await asyncio.wait_for(ws.recv(), timeout=self.heartbeat_interval)
            except TimeoutError:
                await self.send_heartbeat(ws)
                raw = await asyncio.wait_for(ws.recv(), timeout=self.heartbeat_interval)

            if self.is_heartbeat_response(raw):
                continue

            received = time.time()
            try:
                data = orjson.loads(raw)
                update = self.parse(data, received)
                if update:
                    await handler(update)
            except (orjson.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as exc:
                self._log(logging.WARNING, f"malformed_message: {exc}")

    async def send_heartbeat(self, ws: ClientConnection) -> None:
        """Send an exchange-specific heartbeat after an idle receive interval."""
        raise RuntimeError(f"{self.exchange} configured a heartbeat interval without a heartbeat")

    def is_heartbeat_response(self, raw: str | bytes) -> bool:
        return False

    async def reconnect(self, handler: UpdateHandler) -> None:
        delay = 1
        while True:
            try:
                ws = await self.connect()
                await self.subscribe(ws)
                self._log(logging.INFO, "subscribed")
                delay = 1
                await self.receive(ws, handler)
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # network failures are connector-local
                self._log(logging.WARNING, f"disconnected: {type(exc).__name__}: {exc}")
            finally:
                if self._ws:
                    await self._ws.close()
                    self._ws = None
            self._log(logging.INFO, f"reconnect_attempt delay_seconds={delay}")
            await asyncio.sleep(delay)
            delay = min(delay * 2, 16)

    async def run(self, handler: UpdateHandler) -> None:
        await self.reconnect(handler)

    def _log(self, level: int, message: str) -> None:
        self.logger.log(level, message, extra={"event": message.split(" ", 1)[0], "exchange": self.exchange})


def top(values: list[list[str | float]]) -> tuple[float, float]:
    price, quantity = values[0]
    return float(price), float(quantity)


def update(exchange: str, bid: tuple[float, float], ask: tuple[float, float], received: float, timestamp: float | None = None) -> BookUpdate:
    return BookUpdate(exchange, bid[0], bid[1], ask[0], ask[1], timestamp, received)
