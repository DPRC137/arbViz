from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.config import settings
from app.engine.arbitrage import ArbitrageEngine
from app.engine.broadcaster import Broadcaster
from app.engine.orderbooks import OrderBookStore
from app.exchanges import connectors
from app.logging import configure_logging
from app.websocket.routes import router as websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    app.state.broadcaster = Broadcaster()
    app.state.store = OrderBookStore(settings.stale_after_seconds)
    app.state.engine = ArbitrageEngine(app.state.store, app.state.broadcaster)
    tasks = [asyncio.create_task(connector.run(app.state.engine.on_update), name=connector.exchange) for connector in connectors()]
    yield
    for task in tasks:
        task.cancel()
    for task in tasks:
        with suppress(asyncio.CancelledError):
            await task


app = FastAPI(title="arbViz", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=False, allow_methods=["GET"], allow_headers=["*"])
app.include_router(api_router, prefix="/api")
app.include_router(websocket_router)
