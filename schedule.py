from __future__ import annotations

import contextlib

import aiohttp
from loguru import logger
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError

import hun


async def save_package_and_notify(
    existing_package: hun.GamePackage | None, *, version: str, region: hun.Region, is_preload: bool
) -> None:
    if existing_package is not None:
        if existing_package.version != version:
            if not is_preload:
                with contextlib.suppress(IntegrityError):
                    await hun.GameMaint.create(region=region, version=version)

            webhooks = await hun.Webhook.filter(region=region).all()
            logger.info(f"Sending {region} webhooks, total {len(webhooks)}")

            for webhook in webhooks:
                success = await hun.send_webhook(
                    webhook.url,
                    hun.get_game_webhook_data(
                        region, version=version, is_preload=is_preload, role_ids=webhook.role_ids
                    ),
                )
                if not success:
                    logger.error(f"Failed to send webhook to {webhook.url!r}")
                    await webhook.delete()

        existing_package.version = version
        await existing_package.save()
    else:
        await hun.GamePackage.create(region=region, version=version, is_preload=is_preload)


async def handle_packages(packages: list[hun.GamePackageModel]) -> None:
    for region in hun.Region:
        package = next((p for p in packages if p.game.id == region.value), None)
        if package is None:
            logger.error(f"Cannot find game package for {region}")
            continue

        main_package = package.main
        existing_main_package = await hun.GamePackage.get_or_none(region=region, is_preload=False)
        await save_package_and_notify(
            existing_main_package,
            version=main_package.major.version,
            region=region,
            is_preload=False,
        )

        preload_package = package.pre_download
        if preload_package is None or preload_package.major is None:
            continue

        existing_preload_package = await hun.GamePackage.get_or_none(region=region, is_preload=True)
        await save_package_and_notify(
            existing_preload_package,
            version=preload_package.major.version,
            region=region,
            is_preload=True,
        )


async def notify_game_maint(maint: hun.GameMaint, *, is_maint: bool) -> None:
    webhooks = await hun.Webhook.filter(region=maint.region).all()
    logger.info(f"Sending {maint.region} maintenance webhooks, total {len(webhooks)}")

    for webhook in webhooks:
        success = await hun.send_webhook(
            webhook.url,
            hun.get_game_maint_webhook_data(
                maint.region, version=maint.version, is_maint=is_maint, role_ids=webhook.role_ids
            ),
        )
        if not success:
            logger.error(f"Failed to send webhook to {webhook.url!r}")
            await webhook.delete()


async def handle_game_maint(session: aiohttp.ClientSession) -> None:
    packages = await hun.GamePackage.all()

    for package in packages:
        maint = await hun.GameMaint.get_or_none(region=package.region, version=package.version)
        if maint is None:
            continue

        if maint.maint_start_notified and maint.maint_end_notified:
            continue

        is_maint = await hun.get_maint_status(session, region=maint.region, version=maint.version)
        if is_maint is None:
            continue

        if is_maint and not maint.maint_start_notified:
            await notify_game_maint(maint, is_maint=True)
            maint.maint_start_notified = True
            await maint.save(update_fields=("maint_start_notified",))

        elif not is_maint and maint.maint_start_notified and not maint.maint_end_notified:
            await notify_game_maint(maint, is_maint=False)
            maint.maint_end_notified = True
            await maint.save(update_fields=("maint_end_notified",))


async def main() -> None:
    await Tortoise.init(db_url="sqlite://hun.db", modules={"models": ["hun.models"]})
    await Tortoise.generate_schemas()

    packages: list[hun.GamePackageModel] = []

    async with aiohttp.ClientSession() as session:
        async with session.get(hun.HYP_CN_ENDPOINT) as resp:
            logger.info("Fetching CN game package data")
            resp.raise_for_status()
            packages.extend(
                [
                    hun.GamePackageModel(**data)
                    for data in (await resp.json())["data"]["game_packages"]
                ]
            )

        async with session.get(hun.HYP_GLOBAL_ENDPOINT) as resp:
            logger.info("Fetching Global game package data")
            resp.raise_for_status()
            packages.extend(
                [
                    hun.GamePackageModel(**data)
                    for data in (await resp.json())["data"]["game_packages"]
                ]
            )

        await handle_packages(packages)
        await handle_game_maint(session)


if __name__ == "__main__":
    run_async(main())
