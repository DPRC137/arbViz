from typing import Any
import orjson
from .base import ExchangeConnector, update


class BitgetConnector(ExchangeConnector):
    exchange, url = "bitget", "wss://ws.bitget.com/v2/ws/public"
    async def subscribe(self, ws): await ws.send(orjson.dumps({"op": "subscribe", "args": [{"instType": "SPOT", "channel": "ticker", "instId": "BTCUSDT"}]}))
    def parse(self, m: dict[str, Any], received: float):
        if m.get("arg", {}).get("channel") != "ticker": return None
        x = m["data"][0]
        return update(self.exchange, (float(x["bidPr"]), float(x["bidSz"])), (float(x["askPr"]), float(x["askSz"])), received, float(x["ts"]) / 1000)
