from __future__ import annotations
from typing import Any
import httpx
import orjson
from .base import ExchangeConnector, update


class KuCoinConnector(ExchangeConnector):
    exchange = "kucoin"
    url = ""
    async def connect(self):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post("https://api.kucoin.com/api/v1/bullet-public")
            response.raise_for_status()
            data = response.json()["data"]
        server = data["instanceServers"][0]
        self.url = f'{server["endpoint"]}?token={data["token"]}&connectId=arbviz'
        return await super().connect()
    async def subscribe(self, ws): await ws.send(orjson.dumps({"id": "arbviz", "type": "subscribe", "topic": "/market/ticker:BTC-USDT", "privateChannel": False, "response": True}))
    def parse(self, m: dict[str, Any], received: float):
        if m.get("topic") != "/market/ticker:BTC-USDT" or m.get("type") != "message": return None
        x = m["data"]
        return update(self.exchange, (float(x["bestBid"]), float(x["bestBidSize"])), (float(x["bestAsk"]), float(x["bestAskSize"])), received, float(x["time"]) / 1_000_000_000)
