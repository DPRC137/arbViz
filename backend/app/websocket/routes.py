from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws")
async def market_feed(websocket: WebSocket) -> None:
    broadcaster = websocket.app.state.broadcaster
    await broadcaster.connect(websocket)
    try:
        await websocket.send_json(await websocket.app.state.engine.payload())
        while True:
            await websocket.receive_text()  # keeps proxies and browser connection state honest
    except WebSocketDisconnect:
        pass
    finally:
        await broadcaster.disconnect(websocket)
