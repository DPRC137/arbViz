from __future__ import annotations

import asyncio
import time

from app.models import Book, BookUpdate


class OrderBookStore:
    def __init__(self, stale_after: float) -> None:
        self._books: dict[str, Book] = {}
        self._lock = asyncio.Lock()
        self.stale_after = stale_after

    async def apply(self, event: BookUpdate) -> None:
        if event.bid <= 0 or event.ask <= 0 or event.bid > event.ask * 1.1:
            return
        async with self._lock:
            self._books[event.exchange] = Book(
                exchange=event.exchange, bid=event.bid, bid_qty=event.bid_qty,
                ask=event.ask, ask_qty=event.ask_qty, updated=event.received_timestamp,
                exchange_timestamp=event.exchange_timestamp,
            )

    async def snapshot(self) -> list[Book]:
        now = time.time()
        async with self._lock:
            return [book for book in self._books.values() if now - book.updated <= self.stale_after]

    async def payload(self) -> list[dict]:
        now = time.time()
        async with self._lock:
            return [book.payload(now, self.stale_after) for book in sorted(self._books.values(), key=lambda b: b.exchange)]
