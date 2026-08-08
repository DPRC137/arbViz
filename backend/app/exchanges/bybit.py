from typing import Any
import orjson
from .base import ExchangeConnector, top, update


class BybitConnector(ExchangeConnector):
    exchange, url = "bybit", "wss://stream.bybit.com/v5/public/spot"
    async def subscribe(self, ws): await ws.send(orjson.dumps({"op": "subscribe", "args": ["orderbook.1.BTCUSDT"]}))
    def parse(self, m: dict[str, Any], received: float):
        if m.get("topic") != "orderbook.1.BTCUSDT": return None
        data = m["data"]
        return update(self.exchange, top(data["b"]), top(data["a"]), received, float(m["ts"]) / 1000)
