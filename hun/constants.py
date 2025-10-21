from __future__ import annotations

from enum import StrEnum

__all__ = (
    "GAME_PACKAGES_CN_URL",
    "GAME_PACKAGES_GLOBAL_URL",
    "Region",
    "get_region_icon",
    "get_region_name",
)


class Region(StrEnum):
    GI_GLB = "gopR6Cufr3"
    GI_CN = "1Z8W5NHUQb"

    HSR_GLB = "4ziysqXOQ8"
    HSR_CN = "64kMb5iAWu"

    ZZZ_GLB = "U5hbdsT9W7"
    ZZZ_CN = "x6znKlJ0xK"

    HI3_US_EU = "5TIVvvcwtM"
    HI3_SEA = "bxPTXSET5t"
    HI3_JP = "g0mMIvshDb"
    HI3_KR = "uxB4MC7nzC"
    HI3_TW = "wkE5P5WsIf"
    HI3_CN = "osvnlOc0S8"


GAME_PACKAGES_GLOBAL_URL = (
    "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?launcher_id=VYTpXlbWo8"
)
GAME_PACKAGES_CN_URL = (
    "https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGamePackages?launcher_id=jGHBHlcOq1"
)

GAME_BRANCHES_GLOBAL_URL = (
    "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGameBranches?launcher_id=VYTpXlbWo8"
)
GAME_BRANCHES_CN_URL = (
    "https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGameBranches?launcher_id=jGHBHlcOq1"
)

MAINT_ENDPOINTS = {
    Region.GI_GLB: "https://sg-cg-api.hoyoverse.com/hk4e_global/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.GI_CN: "https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/getGlobalApplicationMaintenance",
    Region.HSR_GLB: "https://cg-hkrpg-api.mihoyo.com/hkrpg_cn/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.HSR_CN: "https://cg-hkrpg-api.mihoyo.com/hkrpg_cn/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.ZZZ_GLB: "https://cg-nap-api.mihoyo.com/nap_cn/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.ZZZ_CN: "https://cg-nap-api.mihoyo.com/nap_cn/cg/gamer/api/getGlobalApplicationMaintenance",
}
MAINT_GAME_BIZS = {
    Region.GI_GLB: "hk4e_global",
    Region.GI_CN: "hk4e_cn",
    Region.HSR_GLB: "hkrpg_cn",
    Region.HSR_CN: "hkrpg_cn",
    Region.ZZZ_GLB: "nap_cn",
    Region.ZZZ_CN: "nap_cn",
}

REGION_NAMES = {
    Region.GI_GLB: "Genshin Impact (Global)",
    Region.GI_CN: "Genshin Impact (China)",
    Region.HSR_GLB: "Honkai: Star Rail (Global)",
    Region.HSR_CN: "Honkai: Star Rail (China)",
    Region.ZZZ_GLB: "Zenless Zone Zero (Global)",
    Region.ZZZ_CN: "Zenless Zone Zero (China)",
    Region.HI3_US_EU: "Honkai Impact 3rd (US/EU)",
    Region.HI3_SEA: "Honkai Impact 3rd (SEA)",
    Region.HI3_JP: "Honkai Impact 3rd (Japan)",
    Region.HI3_KR: "Honkai Impact 3rd (Korea)",
    Region.HI3_TW: "Honkai Impact 3rd (Taiwan)",
    Region.HI3_CN: "Honkai Impact 3rd (China)",
}
ICONS = {
    (
        Region.GI_CN,
        Region.GI_GLB,
    ): "https://raw.githubusercontent.com/seriaati/hoyo-update-notifier/refs/heads/main/game_icons/icon_ys.jpg",
    (
        Region.HI3_CN,
        Region.HI3_JP,
        Region.HI3_KR,
        Region.HI3_SEA,
        Region.HI3_TW,
        Region.HI3_US_EU,
    ): "https://raw.githubusercontent.com/seriaati/hoyo-update-notifier/refs/heads/main/game_icons/icon_bh3.jpg",
    (
        Region.HSR_CN,
        Region.HSR_GLB,
    ): "https://raw.githubusercontent.com/seriaati/hoyo-update-notifier/refs/heads/main/game_icons/icon_sr.jpg",
    (
        Region.ZZZ_CN,
        Region.ZZZ_GLB,
    ): "https://raw.githubusercontent.com/seriaati/hoyo-update-notifier/refs/heads/main/game_icons/icon_zzz.jpg",
}

NOTICE = {
    Region.GI_GLB: "https://m.hoyolab.com/toBBS.html?game_id=2",
    Region.GI_CN: "https://bbs.mihoyo.com/ysToBBS.html",
    Region.HSR_GLB: "https://m.hoyolab.com/toBBS.html?game_id=6",
    Region.HSR_CN: "https://bbs.mihoyo.com/srToBBS.html",
    Region.ZZZ_GLB: "https://m.hoyolab.com/toBBS.html?game_id=8",
    Region.ZZZ_CN: "https://bbs.mihoyo.com/zzzToBBS.html",
}


def get_region_name(region: Region) -> str:
    return REGION_NAMES.get(region, "Unknown region")


def get_region_icon(region: Region) -> str:
    for regions, icon in ICONS.items():
        if region in regions:
            return icon

    return ""


def get_notice_url(region: Region) -> str | None:
    return NOTICE.get(region)
