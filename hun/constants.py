from typing import Final

__all__ = (
    "ENDPOINTS",
    "GAMES",
    "GAME_BIZS",
    "HYP_CN_ENDPOINT",
    "HYP_GLOBAL_ENDPOINT",
    "get_game_icon",
)

GAMES: tuple[str, ...] = (
    "Genshin Impact Global",
    "Genshin Impact China",
    "Honkai Impact 3rd Global",
    "Honkai Impact 3rd China",
    "Honkai Impact 3rd SEA",
    "Honkai: Star Rail Global",
    "Honkai: Star Rail China",
    "Zenless Zone Zero Global",
    "Zenless Zone Zero China",
)

HYP_GLOBAL_ENDPOINT: Final[str] = (
    "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?launcher_id=VYTpXlbWo8"
)
"""HoYoPlay global endpoint, contains GI, HSR, ZZZ version data."""

HYP_CN_ENDPOINT: Final[str] = (
    "https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGamePackages?launcher_id=jGHBHlcOq1"
)
"""HoYoPlay China endpoint, contains GI, HSR, ZZZ, HI3 version data."""

ENDPOINTS: Final[dict[str, str]] = {
    "Genshin Impact Global": HYP_GLOBAL_ENDPOINT,
    "Genshin Impact China": HYP_CN_ENDPOINT,
    "Honkai Impact 3rd Global": "https://sdk-os-static.mihoyo.com/bh3_global/mdk/launcher/api/resource?key=dpz65xJ3&channel_id=1&launcher_id=10&sub_channel_id=1",
    "Honkai Impact 3rd China": HYP_CN_ENDPOINT,
    "Honkai Impact 3rd SEA": "https://sdk-os-static.mihoyo.com/bh3_global/mdk/launcher/api/resource?channel_id=1&key=tEGNtVhN&launcher_id=9&sub_channel_id=1",
    "Honkai: Star Rail Global": HYP_GLOBAL_ENDPOINT,
    "Honkai: Star Rail China": HYP_CN_ENDPOINT,
    "Zenless Zone Zero Global": HYP_GLOBAL_ENDPOINT,
    "Zenless Zone Zero China": HYP_CN_ENDPOINT,
}

GAME_BIZS: Final[dict[str, str]] = {
    "Genshin Impact Global": "hk4e_global",
    "Genshin Impact China": "hk4e_cn",
    "Honkai Impact 3rd Global": "bh3_global",
    "Honkai Impact 3rd China": "bh3_cn",
    "Honkai Impact 3rd SEA": "bh3_sea",
    "Honkai: Star Rail Global": "hkrpg_global",
    "Honkai: Star Rail China": "hkrpg_cn",
    "Zenless Zone Zero Global": "nap_global",
    "Zenless Zone Zero China": "nap_cn",
}

ICONS: Final[dict[str, str]] = {
    "Genshin Impact": "https://iili.io/dKleQ4I.png",
    "Honkai Impact 3rd": "https://iili.io/dKleLEN.png",
    "Honkai: Star Rail": "https://iili.io/dKlesBp.png",
    "Zenless Zone Zero": "https://iili.io/dKlekrP.png",
}


def get_game_icon(game_name: str) -> str:
    for game, icon_url in ICONS.items():
        if game_name.startswith(game):
            return icon_url
    msg = f"Cannot find icon for game: {game_name}"
    raise ValueError(msg)
