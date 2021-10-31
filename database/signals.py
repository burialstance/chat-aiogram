from typing import Type, List
from tortoise.signals import pre_save, post_save
from loguru import logger

from database.models.user import User
from database.models.search_options import SearchOptions
from database.models.country import Country
from database.enums import CountriesEnum


@pre_save(User)
async def signal_create_search_options_for_user(sender: "Type[User]", instance: User, using_db, update_fields) -> None:
    if not instance.search_options:
        instance.search_options = await SearchOptions.create()
        logger.debug(f'for {instance}: created default {instance.search_options}')

    if not instance.country:
        instance.country, _ = await Country.get_or_create(name=CountriesEnum.RUSSIA)
        logger.debug(f'for {instance}: created default {instance.country}')


@pre_save(SearchOptions)
async def signal_create_search_options_country(sender: "Type[SearchOptions]", instance: SearchOptions, using_db,
                                               update_fields) -> None:
    if not await instance.country:
        instance.country, _ = await Country.get_or_create(name=CountriesEnum.RUSSIA)
        logger.debug(f'for {instance}: created default {instance.country}')


@post_save(User)
async def signal_post_save_user(sender: "Type[User]", instance: User, created: bool,
                                using_db: "Optional[BaseDBAsyncClient]",
                                update_fields: List[str]) -> None:
    if created and instance.referred:
        print(f'created new {instance} with referred {await instance.referred}')
