from typing import Any
import orjson
from .base import ExchangeConnector, update


class KrakenConnector(ExchangeConnector):
    exchange, url = "kraken", "wss://ws.kraken.com/v2"
    async def subscribe(self, ws): await ws.send(orjson.dumps({"method": "subscribe", "params": {"channel": "ticker", "symbol": ["BTC/USDT"]}}))
    def parse(self, m: dict[str, Any], received: float):
        if m.get("channel") != "ticker": return None
        x = m["data"][0]
        return update(self.exchange, (float(x["bid"]), float(x["bid_qty"])), (float(x["ask"]), float(x["ask_qty"])), received, None)
