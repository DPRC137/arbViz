from __future__ import annotations

import time
from dataclasses import asdict, dataclass

from app.engine.orderbooks import OrderBookStore
from app.models import Book, BookUpdate


@dataclass(frozen=True, slots=True)
class Opportunity:
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread: float
    spread_percent: float


class ArbitrageEngine:
    def __init__(self, store: OrderBookStore, broadcaster) -> None:
        self.store = store
        self.broadcaster = broadcaster

    async def on_update(self, event: BookUpdate) -> None:
        await self.store.apply(event)
        await self.broadcaster.broadcast(await self.payload())

    async def payload(self) -> dict:
        books = await self.store.snapshot()
        opportunities = self._opportunities(books)
        summary = asdict(opportunities[0]) if opportunities else {
            "buy_exchange": None, "buy_price": None, "sell_exchange": None,
            "sell_price": None, "spread": 0, "spread_percent": 0,
        }
        return {
            "summary": summary,
            "books": await self.store.payload(),
            "opportunities": [asdict(item) for item in opportunities],
            "updated_at": time.time(),
        }

    @staticmethod
    def _opportunities(books: list[Book]) -> list[Opportunity]:
        opportunities = []
        for buy in books:
            for sell in books:
                if buy.exchange == sell.exchange:
                    continue
                spread = sell.bid - buy.ask
                if spread > 0:
                    opportunities.append(Opportunity(
                        buy_exchange=buy.exchange, sell_exchange=sell.exchange,
                        buy_price=buy.ask, sell_price=sell.bid, spread=spread,
                        spread_percent=(spread / buy.ask) * 100,
                    ))
        return sorted(opportunities, key=lambda item: item.spread, reverse=True)
