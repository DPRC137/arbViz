from typing import Any
import time
import orjson
from .base import ExchangeConnector, update


class GateIOConnector(ExchangeConnector):
    exchange, url = "gateio", "wss://api.gateio.ws/ws/v4/"
    async def subscribe(self, ws): await ws.send(orjson.dumps({"time": int(time.time()), "channel": "spot.book_ticker", "event": "subscribe", "payload": ["BTC_USDT"]}))
    def parse(self, m: dict[str, Any], received: float):
        if m.get("channel") != "spot.book_ticker" or m.get("event") != "update": return None
        x = m["result"]
        return update(self.exchange, (float(x["b"]), float(x["B"])), (float(x["a"]), float(x["A"])), received, float(x.get("t", 0)) / 1000 or None)
