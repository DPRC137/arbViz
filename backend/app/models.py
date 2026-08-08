from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BookUpdate:
    """The exchange-agnostic, top-of-book event consumed by the engine."""

    exchange: str
    bid: float
    bid_qty: float
    ask: float
    ask_qty: float
    exchange_timestamp: float | None
    received_timestamp: float


@dataclass(frozen=True, slots=True)
class Book:
    exchange: str
    bid: float
    bid_qty: float
    ask: float
    ask_qty: float
    updated: float
    exchange_timestamp: float | None

    def payload(self, now: float, stale_after: float) -> dict[str, Any]:
        result = asdict(self)
        result["status"] = "live" if now - self.updated <= stale_after else "stale"
        result["latency_ms"] = round(max(0, (self.updated - (self.exchange_timestamp or self.updated)) * 1000), 1)
        return result
