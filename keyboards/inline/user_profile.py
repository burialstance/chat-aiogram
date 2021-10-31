from aiogram import types
from aiogram.utils.callback_data import CallbackData

from database.enums import UserGenderEnum, CountriesEnum
from misc import icon_characters as icons
from misc.country_enum_icons import country_enum_icons
from misc.gender_enum_icons import gender_enum_icons

user_profile_section_callback = CallbackData('user_profile', 'section')
user_profile_setup_country_callback = CallbackData('user_profile_setup_country', 'country')
user_profile_setup_gender_callback = CallbackData('user_profile_setup_gender', 'gender')


def build_user_profile_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(text=f'{icons.underage} Изменить Возраст',
                                   callback_data=user_profile_section_callback.new(section='setup_age')),
        types.InlineKeyboardButton(text=f'{icons.world} Изменить страну',
                                   callback_data=user_profile_section_callback.new(section='setup_country')),
        types.InlineKeyboardButton(text=f'{icons.couple} Изменить Пол',
                                   callback_data=user_profile_section_callback.new(section='setup_gender'))
    )

    return kb


def build_user_profile_setup_country_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for country in CountriesEnum:
        if country == CountriesEnum.ALL:
            continue
        country_icon = country_enum_icons.get(country, country_enum_icons[CountriesEnum.ALL])
        kb.insert(types.InlineKeyboardButton(
            text=f"{country_icon} {country.value}",
            callback_data=user_profile_setup_country_callback.new(country=country.value))
        )

    kb.row(types.InlineKeyboardButton(
        text=f'{icons.back} Назад', callback_data=user_profile_section_callback.new(section='main')))
    return kb


def build_user_profile_setup_gender_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for gender in UserGenderEnum:
        if gender == UserGenderEnum.UNKNOWN:
            continue
        gender_icon = gender_enum_icons[gender]
        kb.insert(types.InlineKeyboardButton(
            text=f"{gender_icon} {gender.value}",
            callback_data=user_profile_setup_gender_callback.new(gender=gender.value))
        )
    kb.row(types.InlineKeyboardButton(
        text=f'{icons.back} Назад', callback_data=user_profile_section_callback.new(section='main')))
    return kb
