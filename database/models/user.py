from tortoise import fields

from database.models import AbstractBaseModel
from database.mixins import TimestampMixin
from database.enums import UserGenderEnum


class User(AbstractBaseModel, TimestampMixin):
    telegram_id: int = fields.IntField(unique=True)

    age: int = fields.IntField(null=True)
    gender: UserGenderEnum = fields.CharEnumField(enum_type=UserGenderEnum, default=UserGenderEnum.UNKNOWN)
    country: fields.ForeignKeyNullableRelation['Country'] = fields.ForeignKeyField(
        'models.Country', related_name='users', on_delete=fields.SET_NULL, null=True)

    search_options: fields.OneToOneNullableRelation['SearchOptions'] = fields.OneToOneField(
        'models.SearchOptions', related_name='user', on_delete=fields.SET_NULL, null=True)

    referred: fields.ForeignKeyNullableRelation['User'] = fields.ForeignKeyField(
        'models.User', related_name='referrals', on_delete=fields.SET_NULL, null=True)



