from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
async def health(request: Request) -> dict:
    return {"status": "ok", "exchanges": len(await request.app.state.store.snapshot())}


@router.get("/snapshot")
async def snapshot(request: Request) -> dict:
    return await request.app.state.engine.payload()
