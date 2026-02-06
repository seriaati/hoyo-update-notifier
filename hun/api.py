from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import aiofiles
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from tortoise import Tortoise

from .constants import REGION_NAMES, Region
from .models import GamePackage, Webhook
from .scheduler import check_game_updates
from .schemas import WebhookCreate, WebhookTest
from .webhook import get_test_webhook_data, send_webhook

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

__all__ = ("app",)

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.session = aiohttp.ClientSession()
    await Tortoise.init(db_url="sqlite://data/hun.db", modules={"models": ["hun.models"]})
    await Tortoise.generate_schemas()

    # Initialize and start APScheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_game_updates,
        "interval",
        minutes=10,
        args=[app.state.session],
        id="check_game_updates",
    )
    scheduler.start()

    yield

    # Shutdown scheduler
    scheduler.shutdown()

    await app.state.session.close()
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> HTMLResponse:
    async with aiofiles.open("hun/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=status.HTTP_200_OK)


@app.get("/regions")
async def get_regions() -> JSONResponse:
    return JSONResponse(
        content={r.value: n for r, n in REGION_NAMES.items()}, status_code=status.HTTP_200_OK
    )


@app.post("/webhooks")
async def create_webhook(data: WebhookCreate) -> Response:
    existing = await Webhook.filter(**data.model_dump()).first()
    if existing is not None:
        return Response(status_code=status.HTTP_409_CONFLICT)

    await Webhook.create(**data.model_dump())
    return Response(status_code=status.HTTP_201_CREATED)


@app.post("/webhooks/test")
async def test_webhook(data: WebhookTest) -> Response:
    await send_webhook(data.url, get_test_webhook_data())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/games/{region}/version")
async def get_game_version(region: Region) -> JSONResponse:
    """Get the current latest stable version for a game region."""
    latest_version = (
        await GamePackage.filter(region=region, is_preload=False).order_by("-id").first()
    )

    if latest_version is None:
        return JSONResponse(
            content={"error": "No version found for this region"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(
        content={"region": region.value, "version": latest_version.version},
        status_code=status.HTTP_200_OK,
    )
