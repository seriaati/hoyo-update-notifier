from __future__ import annotations

import aiohttp
from loguru import logger
from tortoise import Tortoise, run_async

import hun


async def save_and_send_webhooks(
    existing_package: hun.GamePackage | None, *, version: str, region: hun.Region, is_preload: bool
) -> None:
    if existing_package is not None:
        if existing_package.version != version:
            webhooks = await hun.Webhook.filter(region=region).all()
            logger.info(f"Sending {region!r} webhooks, total {len(webhooks)}")

            for webhook in webhooks:
                success = await hun.send_webhook(
                    webhook.url, hun.get_game_webhook_data(region, version=version, is_preload=is_preload)
                )
                if not success:
                    logger.error(f"Failed to send webhook to {webhook.url!r}")
                    await webhook.delete()

        existing_package.version = version
        await existing_package.save()
    else:
        await hun.GamePackage.create(region=region, version=version, is_preload=is_preload)


async def main() -> None:
    await Tortoise.init(db_url="sqlite://hun.db", modules={"models": ["hun.models"]})
    await Tortoise.generate_schemas()

    packages: list[hun.GamePackageModel] = []

    async with aiohttp.ClientSession() as session:
        async with session.get(hun.HYP_CN_ENDPOINT) as resp:
            logger.info("Fetching CN game package data")
            resp.raise_for_status()
            packages.extend([hun.GamePackageModel(**data) for data in (await resp.json())["data"]["game_packages"]])

        async with session.get(hun.HYP_GLOBAL_ENDPOINT) as resp:
            logger.info("Fetching Global game package data")
            resp.raise_for_status()
            packages.extend([hun.GamePackageModel(**data) for data in (await resp.json())["data"]["game_packages"]])

        for region in hun.Region:
            package = next((p for p in packages if p.game.id == region.value), None)
            if package is None:
                logger.error(f"Cannot find game package for {region.name!r}")
                continue

            main_package = package.main
            existing_main_package = await hun.GamePackage.get_or_none(region=region, is_preload=False)
            await save_and_send_webhooks(
                existing_main_package, version=main_package.major.version, region=region, is_preload=False
            )

            preload_package = package.pre_download
            if preload_package is None or preload_package.major is None:
                continue

            existing_preload_package = await hun.GamePackage.get_or_none(region=region, is_preload=True)
            await save_and_send_webhooks(
                existing_preload_package, version=preload_package.major.version, region=region, is_preload=True
            )


if __name__ == "__main__":
    run_async(main())
