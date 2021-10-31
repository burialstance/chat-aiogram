from tortoise import fields

from database.mixins import TimestampMixin
from database.models import AbstractBaseModel
from database.enums import SearchOptionsGenderEnum


class SearchOptions(AbstractBaseModel, TimestampMixin):
    user: fields.OneToOneRelation['User']

    sex: SearchOptionsGenderEnum = fields.CharEnumField(enum_type=SearchOptionsGenderEnum, default=SearchOptionsGenderEnum.ALL)
    from_age: int = fields.IntField(null=True)
    to_age: int = fields.IntField(null=True)

    country = fields.ForeignKeyField(
        'models.Country', related_name='search_options', on_delete=fields.CASCADE)
