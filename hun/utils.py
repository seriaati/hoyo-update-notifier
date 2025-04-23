from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from hun.constants import MAINT_ENDPOINTS, MAINT_GAME_BIZS, Region

if TYPE_CHECKING:
    import aiohttp


async def get_maint_status(
    session: aiohttp.ClientSession, *, region: Region, version: str
) -> bool | None:
    """Get the maintenance status for the given region.

    Returns:
        None if the region doesn't have a maintenance endpoint.
        True if the region is in maintenance.
        False if the maintenance has ended.
    """
    logger.info(f"Checking maintenance status for {region}")

    if (game_biz := MAINT_GAME_BIZS.get(region)) is None:
        return None

    if (endpoint := MAINT_ENDPOINTS.get(region)) is None:
        return None

    headers = {
        "x-rpc-app_version": version,
        "x-rpc-client_type": "1",
        "x-rpc-cg_game_biz": game_biz,
    }

    try:
        async with session.get(endpoint, headers=headers) as resp:
            data = await resp.json()
            return data["data"]["application_maintenance"] is not None
    except Exception as e:
        logger.error(f"Failed to get maintenance status for {region}: {e}")
        return False
