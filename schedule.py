import asyncio
import logging

import aiohttp
from tortoise import Tortoise

from hoyo_update_notifier.constants import ENDPOINTS
from hoyo_update_notifier.logging import setup_logging
from hoyo_update_notifier.models import GameVersionInfo, Webhook
from hoyo_update_notifier.webhook import get_game_webhook_data, send_webhook

LOGGER_ = logging.getLogger("hoyo_update_notifier.schedule")


async def main() -> None:
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["hoyo_update_notifier.models"]},
    )
    await Tortoise.generate_schemas()

    session = aiohttp.ClientSession()

    for game, endpoint in ENDPOINTS.items():
        LOGGER_.info("Fetching %s update data", game)

        async with session.get(endpoint) as resp:
            if resp.status != 200:
                LOGGER_.error("Failed to fetch %s update data", game)
                continue

            data = await resp.json()
            latest = data["data"]["game"]["latest"]
            version = latest["version"]
            md5 = latest["md5"]

        game_version_info = await GameVersionInfo.get_or_none(game=game)
        if game_version_info is None:
            LOGGER_.info("Creating %s game version info", game)
            game_version_info = await GameVersionInfo.create(
                game=game, version_num=version, md5=md5
            )
        else:
            if game_version_info.md5 != md5:
                webhooks = await Webhook.filter(game=game).all()
                LOGGER_.info("Sending %s webhooks, total %s", game, len(webhooks))
                for webhook in webhooks:
                    await send_webhook(webhook.url, get_game_webhook_data(game, version))

            game_version_info.version_num = version
            game_version_info.md5 = md5
            await game_version_info.save()

    await session.close()
    await Tortoise.close_connections()


with setup_logging():
    asyncio.run(main())
