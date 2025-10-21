from __future__ import annotations

from typing import Any

import aiohttp

from .constants import REGION_NAMES, Region, get_notice_url, get_region_icon

__all__ = (
    "get_game_maint_webhook_data",
    "get_game_webhook_data",
    "get_test_webhook_data",
    "send_webhook",
)


def get_game_webhook_data(
    region: Region, *, version: str, is_preload: bool, role_ids: list[int]
) -> dict[str, Any]:
    # Base description always includes region and version
    description = f"{REGION_NAMES[region]}: v{version}"

    # Only add the patch notes link if it's NOT a preload
    if not is_preload and (notice_url := get_notice_url(region)):
        description += f"\n[Read what's new here!]({notice_url})"

    return {
        "username": "Hoyo Update Notifier",
        "avatar_url": "https://i.imgur.com/tLHYWyR.png",
        "embeds": [
            {
                "author": {
                    "name": "Hoyo Update Notifier",
                    "url": "https://hoyo-update-notifier.seria.moe",
                },
                "title": (
                    "A new preload is available!" if is_preload else "A new update is available!"
                ),
                "description": description,
                "color": 8688619,
                "thumbnail": {"url": get_region_icon(region)},
            }
        ],
        "content": " ".join(f"<@&{role_id}>" for role_id in role_ids),
    }


def get_game_maint_webhook_data(
    region: Region, *, version: str, is_maint: bool, role_ids: list[int]
) -> dict[str, Any]:
    return {
        "username": "Hoyo Update Notifier",
        "avatar_url": "https://i.imgur.com/tLHYWyR.png",
        "embeds": [
            {
                "author": {
                    "name": "Hoyo Update Notifier",
                    "url": "https://hoyo-update-notifier.seria.moe",
                },
                "title": "Maintenance has started!" if is_maint else "Maintenance is over!",
                "description": f"{REGION_NAMES[region]}: v{version}",
                "color": 8688619,
                "thumbnail": {"url": get_region_icon(region)},
            }
        ],
        "content": " ".join(f"<@&{role_id}>" for role_id in role_ids),
    }


def get_test_webhook_data() -> dict[str, Any]:
    return {
        "username": "Hoyo Update Notifier",
        "avatar_url": "https://i.imgur.com/tLHYWyR.png",
        "embeds": [
            {
                "author": {
                    "name": "Hoyo Update Notifier",
                    "url": "https://hoyo-update-notifier.seria.moe",
                },
                "title": "This is a test message",
                "description": "If you see this, then the webhook is working!",
                "color": 8688619,
                "thumbnail": {"url": "https://i.imgur.com/tLHYWyR.png"},
                "footer": {"text": "Future game updates and preloads will be posted here"},
            }
        ],
    }


async def send_webhook(webhook_url: str, json_: dict[str, Any]) -> bool:
    try:
        async with (
            aiohttp.ClientSession() as session,
            session.post(webhook_url, json=json_) as resp,
        ):
            return resp.status == 204
    except Exception:
        return False
