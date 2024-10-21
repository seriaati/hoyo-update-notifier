from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import aiofiles
import aiohttp
from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from tortoise import Tortoise

from .constants import REGION_NAMES
from .models import Webhook, WebhookCreate, WebhookTest
from .webhook import get_test_webhook_data, send_webhook

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

__all__ = ("app",)

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.session = aiohttp.ClientSession()
    await Tortoise.init(db_url="sqlite://hun.db", modules={"models": ["hun.models"]})
    await Tortoise.generate_schemas()
    yield
    await app.state.session.close()
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> HTMLResponse:
    async with aiofiles.open("hun/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=status.HTTP_200_OK)


@app.get("/regions")
async def get_regions() -> JSONResponse:
    return JSONResponse(content={r.value: n for r, n in REGION_NAMES.items()}, status_code=status.HTTP_200_OK)


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
