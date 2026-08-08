from typing import Any
import orjson
from .base import ExchangeConnector, update


class MEXCConnector(ExchangeConnector):
    exchange, url = "mexc", "wss://wbs-api.mexc.com/ws"
    async def subscribe(self, ws): await ws.send(orjson.dumps({"method": "SUBSCRIPTION", "params": ["spot@public.bookTicker.v3.api@BTCUSDT"]}))
    def parse(self, m: dict[str, Any], received: float):
        if m.get("c") != "spot@public.bookTicker.v3.api@BTCUSDT": return None
        x = m["d"]
        return update(self.exchange, (float(x["b"]), float(x["B"])), (float(x["a"]), float(x["A"])), received, float(x.get("t", 0)) / 1000 or None)
