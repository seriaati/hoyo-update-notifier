import asyncio

import aiohttp
from loguru import logger
from tortoise import Tortoise

from hoyo_update_notifier.constants import ENDPOINTS
from hoyo_update_notifier.models import GameVersionInfo, Webhook
from hoyo_update_notifier.webhook import get_game_webhook_data, send_webhook


async def main() -> None:
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["hoyo_update_notifier.models"]},
    )
    await Tortoise.generate_schemas()

    session = aiohttp.ClientSession()

    for game, endpoint in ENDPOINTS.items():
        logger.info(f"Fetching {game} update data")

        async with session.get(endpoint) as resp:
            if resp.status != 200:
                logger.error(f"Failed to fetch {game} update data")
                continue

            data = await resp.json()
            latest = data["data"]["game"]["latest"]
            version = latest["version"]
            md5 = latest["md5"]

        game_version_info = await GameVersionInfo.get_or_none(game=game)
        if game_version_info is None:
            logger.info(f"Creating {game} game version info")
            game_version_info = await GameVersionInfo.create(
                game=game, version_num=version, md5=md5
            )
        else:
            if game_version_info.md5 != md5:
                webhooks = await Webhook.filter(game=game).all()
                logger.info(f"Sending {game} webhooks, total {len(webhooks)}")
                for webhook in webhooks:
                    await send_webhook(webhook.url, get_game_webhook_data(game, version))

            game_version_info.version_num = version
            game_version_info.md5 = md5
            await game_version_info.save()

    await session.close()
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
