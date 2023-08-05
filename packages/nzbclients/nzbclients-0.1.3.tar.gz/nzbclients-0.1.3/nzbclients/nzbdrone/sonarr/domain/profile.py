from typing import List

from marshmallow import Schema, fields


class Quality(object):
    def __init__(self, name: str = None, id: int = None):
        self.name = name
        self.id = id


class Item(object):
    def __init__(self, quality: Quality = None, allowed: bool = None):
        self.quality = quality
        self.allowed = allowed


class Profile(object):
    def __init__(
        self,
        name: str = None,
        cutoff: Quality = None,
        items: List[Item] = None,
        id: int = None,
    ):
        self.name = name
        self.cutoff = cutoff
        self.items = items
        self.id = id


class QualitySchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    name = fields.Str()
    id = fields.Int()

    def load(self, data, many=None, partial=None, unknown=None) -> Quality:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return Quality(**obj)


class ItemSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    quality = fields.Nested(QualitySchema)
    allowed = fields.Bool()

    def load(self, data, many=None, partial=None, unknown=None) -> Item:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return Item(**obj)


class ProfileSchema(Schema):
    class Meta:
        unknown = "EXCLUDE"
        allow_none = False

    name = fields.Str()
    cutoff = fields.Nested(QualitySchema)
    items = fields.List(fields.Nested(ItemSchema))
    id = fields.Int()

    def load(self, data, many=None, partial=None, unknown=None) -> Profile:
        obj = super(Schema, self).load(data, many, partial, unknown)

        return Profile(**obj)
