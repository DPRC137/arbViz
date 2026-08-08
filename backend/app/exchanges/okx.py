from typing import Any

import orjson

from .base import ExchangeConnector, top, update


class OKXConnector(ExchangeConnector):
    exchange, url = "okx", "wss://ws.okx.com:8443/ws/v5/public"

    # OKX rejects RFC 6455 latency-probe frames. Its API requires a text
    # "ping" after an idle period shorter than 30 seconds instead.
    ping_interval = None
    ping_timeout = None
    heartbeat_interval = 25

    async def subscribe(self, ws): await ws.send(orjson.dumps({"op": "subscribe", "args": [{"channel": "books5", "instId": "BTC-USDT"}]}))

    async def send_heartbeat(self, ws) -> None:
        await ws.send("ping")

    def is_heartbeat_response(self, raw: str | bytes) -> bool:
        return raw == "pong" or raw == b"pong"

    def parse(self, m: dict[str, Any], received: float):
        if m.get("arg", {}).get("channel") != "books5": return None
        book = m["data"][0]
        return update(self.exchange, top(book["bids"]), top(book["asks"]), received, float(book["ts"]) / 1000)
