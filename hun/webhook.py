from typing import Any

import aiohttp

from .constants import get_game_icon

__all__ = ("get_game_webhook_data", "get_test_webhook_data", "send_webhook")


def get_game_webhook_data(game: str, version: str) -> dict[str, Any]:
    return {
        "username": "Hoyo Update Notifier",
        "avatar_url": "https://i.imgur.com/tLHYWyR.png",
        "embeds": [
            {
                "author": {
                    "name": "Hoyo Update Notifier",
                    "url": "https://hoyo-update-notifier.seriaati.xyz",
                },
                "title": "A new update is available!",
                "description": f"{game} (v{version})",
                "color": 8688619,
                "thumbnail": {
                    "url": get_game_icon(game),
                },
            }
        ],
    }


def get_test_webhook_data() -> dict[str, Any]:
    return {
        "username": "Hoyo Update Notifier",
        "avatar_url": "https://i.imgur.com/tLHYWyR.png",
        "embeds": [
            {
                "author": {
                    "name": "Hoyo Update Notifier",
                    "url": "https://hoyo-update-notifier.seriaati.xyz",
                },
                "title": "This is a test message",
                "description": "If you see this, then the webhook is working!",
                "color": 8688619,
                "thumbnail": {
                    "url": "https://i.imgur.com/tLHYWyR.png",
                },
                "footer": {
                    "text": "Future game updates will be posted here",
                },
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
