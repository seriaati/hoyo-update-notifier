# pyright: reportAssignmentType=false

from __future__ import annotations

from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model

from .constants import Region

__all__ = ("GameMaint", "GamePackage", "GamePackageModel", "Webhook")


class GamePackage(Model):
    id = fields.IntField(pk=True, generated=True)
    region = fields.CharEnumField(enum_type=Region)
    version = fields.CharField(max_length=8)
    is_preload = fields.BooleanField(default=False)


class GameMaint(Model):
    id = fields.IntField(pk=True, generated=True)
    region = fields.CharEnumField(enum_type=Region)
    version = fields.CharField(max_length=8)
    maint_start_notified = fields.BooleanField(default=False)
    maint_end_notified = fields.BooleanField(default=False)

    class Meta:
        unique_together = ("region", "version")


class Webhook(Model):
    id = fields.IntField(pk=True, generated=True)
    url = fields.CharField(max_length=255)
    region = fields.CharEnumField(enum_type=Region)
    role_ids: fields.Field[list[int]] = fields.JSONField(default="[]")


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
