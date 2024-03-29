import asyncio
import sys

import flet as ft
from tortoise import Tortoise

from hoyo_update_notifier.logging import setup_logging
from hoyo_update_notifier.web_app import HoyoUpdateNotifierWebApp


async def main(page: ft.Page) -> None:
    page.title = "Hoyo Update Notifier"
    page.scroll = ft.ScrollMode.ADAPTIVE
    web_app = HoyoUpdateNotifierWebApp(page)
    await web_app.start()


with setup_logging():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        Tortoise.init(
            db_url="sqlite://db.sqlite3",
            modules={"models": ["hoyo_update_notifier.models"]},
        )
    )
    loop.run_until_complete(Tortoise.generate_schemas())

    ft.app(
        target=main,
        view=None if sys.platform == "linux" else ft.AppView.WEB_BROWSER,
        port=8092,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise.close_connections())
    loop.close()
