from aiogram import types
from database.enums import CountriesEnum, UserGenderEnum
from misc.country_enum_icons import country_enum_icons
from misc.gender_enum_icons import gender_enum_icons


def build_registration_setup_country_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for country in CountriesEnum:
        if country == CountriesEnum.ALL:
            continue
        icon = country_enum_icons[country]
        kb.add(f'{icon} {country.value}')
    return kb


def build_registration_setup_gender():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for gender in UserGenderEnum:
        if gender == UserGenderEnum.UNKNOWN:
            continue
        icon = gender_enum_icons[gender]
        kb.add(f'{icon} {gender.value}')
    return kb
