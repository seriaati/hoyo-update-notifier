from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .constants import Region

__all__ = (
    "Game",
    "GameBranch",
    "GameBranchPackage",
    "GamePackageModel",
    "MainPackage",
    "MajorPackage",
    "PreDownloadPackage",
    "WebhookCreate",
    "WebhookTest",
)


class WebhookCreate(BaseModel):
    url: str
    region: Region


class WebhookTest(BaseModel):
    url: str


class Game(BaseModel):
    id: str
    biz: str


class MajorPackage(BaseModel):
    version: str


class MainPackage(BaseModel):
    major: MajorPackage


class PreDownloadPackage(BaseModel):
    major: MajorPackage | None = None


class GamePackageModel(BaseModel):
    game: Game
    main: MainPackage
    pre_download: PreDownloadPackage | None = None


class GameBranchPackage(BaseModel):
    package_id: str
    branch: Literal["main", "predownload"]
    password: str
    version: str = Field(alias="tag")


class GameBranch(BaseModel):
    game: Game
    main: GameBranchPackage
    pre_download: GameBranchPackage | None = None
