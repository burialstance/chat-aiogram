from typing import Union, Optional

from database.models.user import User
from database.models.country import Country
from database.enums import UserGenderEnum, SearchOptionsGenderEnum, CountriesEnum
from loader import bot


async def get_user(user: Union[User, int], *fetch_related) -> Optional[User]:
    if not any([isinstance(user, User), isinstance(user, int)]):
        raise ValueError(f'value "user" must be int or <User> instance')

    if isinstance(user, int) or isinstance(user, str) and user.isdigit():
        telegram_id = user
        user = await User.get(telegram_id=telegram_id)

        if not user:
            return None

    if fetch_related:
        await user.fetch_related(*fetch_related)
    return user


class UserSearchOptionsService:
    @staticmethod
    async def setup_age(user: Union[User, int], from_age: int, to_age: int) -> User:
        user = await get_user(user, 'search_options')
        user.search_options.from_age, user.search_options.to_age = int(from_age), int(to_age)
        await user.search_options.save(update_fields=['from_age', 'to_age'])
        return user

    @staticmethod
    async def setup_gender(user: Union[User, int], gender: SearchOptionsGenderEnum) -> User:
        user = await get_user(user, 'search_options')
        if not isinstance(gender, SearchOptionsGenderEnum):
            gender = SearchOptionsGenderEnum(gender)
        user.search_options.gender = gender
        await user.search_options.save(update_fields=['gender'])
        return user

    @staticmethod
    async def setup_country(user: Union[User, int], country: CountriesEnum) -> User:
        user = await get_user(user, 'search_options__country')
        if not isinstance(country, CountriesEnum):
            country = CountriesEnum(country)
        user.search_options.country, _ = await Country.get_or_create(name=country)
        await user.search_options.save()
        return user


class UserService:
    search_options = UserSearchOptionsService

    @staticmethod
    async def setup_age(user: Union[User, int], age: int) -> User:
        if not isinstance(age, int):
            age = int(age)
        user = await get_user(user)
        user.age = age
        await user.save()
        return user

    @staticmethod
    async def setup_gender(user: Union[User, int], gender: UserGenderEnum) -> User:
        if not isinstance(gender, UserGenderEnum):
            gender = UserGenderEnum(gender)
        user = await get_user(user)
        user.gender = gender
        await user.save()
        return user

    @staticmethod
    async def setup_country(user: Union[User, int], country: CountriesEnum) -> User:
        if not isinstance(country, CountriesEnum):
            country = CountriesEnum(country)
        user = await get_user(user)
        user.country, _ = await Country.get_or_create(name=country)
        await user.save()
        return user

    @staticmethod
    async def user_exists(telegram_id: int):
        return await User.exists(telegram_id=telegram_id)

    @staticmethod
    async def create(telegram_id: int, age: int = None, country_name: str = None,
                     gender: str = None, referred_id: int = None):
        gender = UserGenderEnum(gender) if gender else UserGenderEnum.UNKNOWN
        country_name = CountriesEnum(country_name) if country_name else None
        country_instance, _ = await Country.get_or_create(name=country_name) if country_name else (None, None)

        referred_instance = await User.get_or_none(telegram_id=referred_id) \
            if all([referred_id, referred_id != telegram_id]) else None
        user = await User.create(
            telegram_id=telegram_id,
            age=age,
            country=country_instance,
            gender=gender,
            referred=referred_instance
        )
        if user.referred:
            await bot.send_message(chat_id=user.referred.telegram_id, text='referral bonus + 100')
        return user
