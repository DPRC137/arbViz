from typing import Any
from .base import ExchangeConnector, top, update


class BinanceConnector(ExchangeConnector):
    exchange, url = "binance", "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"
    async def subscribe(self, ws): pass
    def parse(self, m: dict[str, Any], received: float):
        # `E` (event time) is not present on every bookTicker payload Binance
        # sends.  The local receive time is still recorded by `update`, so use
        # it when the exchange timestamp is omitted instead of rejecting an
        # otherwise valid quote.
        event_time = m.get("E")
        return update(
            self.exchange,
            (float(m["b"]), float(m["B"])),
            (float(m["a"]), float(m["A"])),
            received,
            float(event_time) / 1000 if event_time is not None else None,
        )
