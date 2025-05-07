from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from loguru import logger

from hun.constants import (
    GAME_BRANCHES_CN_URL,
    GAME_BRANCHES_GLOBAL_URL,
    GAME_PACKAGES_CN_URL,
    GAME_PACKAGES_GLOBAL_URL,
    MAINT_ENDPOINTS,
    MAINT_GAME_BIZS,
    Region,
)
from hun.schemas import GameBranch, GamePackageModel

if TYPE_CHECKING:
    import aiohttp

__all__ = ("get_game_branches", "get_game_packages", "get_maint_status")


async def get_maint_status(
    session: aiohttp.ClientSession, *, region: Region, version: str
) -> bool | None:
    """Get the maintenance status for the given region.

    Returns:
        None if the region doesn't have a maintenance endpoint.
        True if the region is in maintenance.
        False if the maintenance has ended.
    """
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
        logger.error(f"Failed to get maintenance status for {region.name}: {e}")
        return False


async def get_game_branches(
    session: aiohttp.ClientSession, *, api_region: Literal["global", "cn"]
) -> list[GameBranch]:
    logger.info(f"Fetching game branches for {api_region!r}")

    url = GAME_BRANCHES_GLOBAL_URL if api_region == "global" else GAME_BRANCHES_CN_URL
    async with session.get(url) as resp:
        data = await resp.json()
        return [GameBranch(**b) for b in data["data"]["game_branches"]]


async def get_game_packages(
    session: aiohttp.ClientSession, *, api_region: Literal["global", "cn"]
) -> list[GamePackageModel]:
    logger.info(f"Fetching game packages for {api_region!r}")

    url = GAME_PACKAGES_GLOBAL_URL if api_region == "global" else GAME_PACKAGES_CN_URL
    async with session.get(url) as resp:
        data = await resp.json()
        return [GamePackageModel(**p) for p in data["data"]["game_packages"]]
