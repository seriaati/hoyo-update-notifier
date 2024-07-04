from tortoise import fields
from tortoise.models import Model


class GameVersionInfo(Model):
    id = fields.IntField(pk=True, generated=True)
    game = fields.CharField(max_length=255)
    md5 = fields.CharField(max_length=32)
    version_num = fields.CharField(max_length=5)


class Webhook(Model):
    uuid = fields.UUIDField()
    url = fields.CharField(max_length=255)
    game = fields.CharField(max_length=255)

    class Meta:
        unique_together = ("uuid", "game")
