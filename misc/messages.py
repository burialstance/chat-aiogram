from aiogram.types import ParseMode

from database.models.user import User
from misc import icon_characters as icons
from misc.gender_enum_icons import gender_enum_icons
from misc.country_enum_icons import country_enum_icons

START_COMMAND_TEXT = """
start command text
user: {user}
"""



async def build_search_options_text(user):
    await user.fetch_related('search_options', 'search_options__country')
    search_from_age = user.search_options.from_age
    search_to_age = user.search_options.to_age
    search_sex = user.search_options.gender.value
    search_country = user.search_options.country.name.value
    search_country_icon = country_enum_icons[user.search_options.country.name]

    message = f"""{icons.settings}<b>Опции поиска собеседника</b>
    Возраст: {search_from_age}-{search_to_age}
    Страна: {search_country_icon} {search_country}
    Пол: {search_sex}    
    """

    return message, ParseMode.HTML


async def build_user_profile_text(user: User):
    await user.fetch_related('country', 'search_options', 'search_options__country')
    telegram_id = user.telegram_id
    user_sex = user.gender.value
    icon_user_sex = gender_enum_icons[user.gender]
    user_age = user.age
    user_country = user.country.name.value
    icon_user_country = country_enum_icons[user.country.name]

    message = f"""
{icons.person} <b>Профиль</b><code> {telegram_id}</code>
    Ваш пол: {icon_user_sex} {user_sex}
    Ваш возраст: {user_age}
    Ваша страна: {icon_user_country} {user_country}

"""

    return message, ParseMode.HTML
