import asyncio
from typing import Any

import aiohttp
from loguru import logger
from tortoise import Tortoise

import hun


async def main() -> None:
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["hun.models"]},
    )
    await Tortoise.generate_schemas()

    session = aiohttp.ClientSession()

    for game, endpoint in hun.ENDPOINTS.items():
        logger.info(f"Fetching {game!r} update data")

        async with session.get(endpoint) as resp:
            if resp.status != 200:
                logger.error(f"Failed to fetch {game!r} update data")
                continue

            data = await resp.json()
            if not hun.is_hoyoplay(endpoint):
                latest: dict[str, Any] = data["data"]["game"]["latest"]
                version: str = latest["version"]
                md5: str = latest["md5"]
            else:
                game_packages = data["data"]["game_packages"]
                game_package: dict[str, Any] | None = next(
                    (p for p in game_packages if p["game"]["biz"] == hun.GAME_BIZS[game]), None
                )
                if game_package is None:
                    logger.error(f"Failed to find {game!r} game package")
                    continue
                version: str = game_package["main"]["major"]["version"]
                md5 = ""  # We no longer rely on md5 to distinguish new game versions

        game_version_info = await hun.GameVersionInfo.get_or_none(game=game)
        if game_version_info is None:
            logger.info(f"Creating {game!r} game version info")
            game_version_info = await hun.GameVersionInfo.create(
                game=game, version_num=version, md5=md5
            )
        else:
            if game_version_info.version_num != version:
                webhooks = await hun.Webhook.filter(game=game).all()
                logger.info(f"Sending {game!r} webhooks, total {len(webhooks)}")
                for webhook in webhooks:
                    await hun.send_webhook(webhook.url, hun.get_game_webhook_data(game, version))

            game_version_info.version_num = version
            game_version_info.md5 = md5
            await game_version_info.save()

    await session.close()
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
