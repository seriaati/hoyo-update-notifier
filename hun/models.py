from __future__ import annotations

from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model

from .constants import Region

__all__ = ("GamePackage", "GamePackageModel", "Webhook")


class GamePackage(Model):
    id = fields.IntField(pk=True, generated=True)
    region = fields.CharEnumField(enum_type=Region)
    version = fields.CharField(max_length=8)
    is_preload = fields.BooleanField(default=False)


class Webhook(Model):
    id = fields.IntField(pk=True, generated=True)
    url = fields.CharField(max_length=255)
    region = fields.CharEnumField(enum_type=Region)


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
