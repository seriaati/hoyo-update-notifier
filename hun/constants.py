from __future__ import annotations

from enum import StrEnum

__all__ = ("HYP_CN_ENDPOINT", "HYP_GLOBAL_ENDPOINT", "Region", "get_region_icon", "get_region_name")


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


HYP_GLOBAL_ENDPOINT = (
    "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?launcher_id=VYTpXlbWo8"
)
HYP_CN_ENDPOINT = (
    "https://hyp-api.mihoyo.com/hyp/hyp-connect/api/getGamePackages?launcher_id=jGHBHlcOq1"
)
MAINT_ENDPOINTS = {
    Region.GI_GLB: "https://sg-cg-api.hoyoverse.com/hk4e_global/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.GI_CN: "https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/getGlobalApplicationMaintenance",
    Region.HSR_GLB: "https://cg-hkrpg-api.mihoyo.com/hkrpg_cn/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.HSR_CN: "https://cg-hkrpg-api.mihoyo.com/hkrpg_cn/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.ZZZ_GLB: "https://cg-nap-api.mihoyo.com/nap_cn/cg/gamer/api/getGlobalApplicationMaintenance",
    Region.ZZZ_CN: "https://cg-nap-api.mihoyo.com/nap_cn/cg/gamer/api/getGlobalApplicationMaintenance",
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
    (Region.GI_CN, Region.GI_GLB): "https://iili.io/dKleQ4I.png",
    (
        Region.HI3_CN,
        Region.HI3_JP,
        Region.HI3_KR,
        Region.HI3_SEA,
        Region.HI3_TW,
        Region.HI3_US_EU,
    ): "https://iili.io/dKleLEN.png",
    (Region.HSR_CN, Region.HSR_GLB): "https://iili.io/dKlesBp.png",
    (Region.ZZZ_CN, Region.ZZZ_GLB): "https://iili.io/dKlekrP.png",
}


def get_region_name(region: Region) -> str:
    return REGION_NAMES.get(region, "Unknown region")


def get_region_icon(region: Region) -> str:
    for regions, icon in ICONS.items():
        if region in regions:
            return icon

    return ""
