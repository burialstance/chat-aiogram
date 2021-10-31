from aiogram import types
from aiogram.utils.callback_data import CallbackData

from database.enums import SearchOptionsGenderEnum, CountriesEnum
from misc import icon_characters as icons
from misc.country_enum_icons import country_enum_icons
from misc.gender_enum_icons import gender_enum_icons


search_options_section_callback = CallbackData('search_options_section', 'section')

search_options_setup_age_callback = CallbackData('search_options_setup_age', 'from_age', 'to_age')
search_options_setup_country_callback = CallbackData('search_options_setup_country', 'country')
search_options_setup_gender_callback = CallbackData('search_options_setup_gender', 'gender')


def build_search_options_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton(text=f'{icons.underage} Возраст',
                                   callback_data=search_options_section_callback.new(section='setup_age')),
        types.InlineKeyboardButton(text=f'{icons.world} Страна',
                                   callback_data=search_options_section_callback.new(section='setup_country'))
    )
    kb.row(types.InlineKeyboardButton(text=f'{icons.couple} Пол собеседника',
                                      callback_data=search_options_section_callback.new(section='setup_gender'))
           )
    return kb


def build_setup_age_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    ages = {
        'до 12 лет': {'from_age': 0, 'to_age': 12},
        '13-15 лет': {'from_age': 13, 'to_age': 15},
        '16-18 лет': {'from_age': 16, 'to_age': 18},
        '19-23 лет': {'from_age': 19, 'to_age': 23},
        '24-27 лет': {'from_age': 24, 'to_age': 27},
        '28-30+': {'from_age': 28, 'to_age': 30},
    }
    for key, value in ages.items():
        kb.insert(types.InlineKeyboardButton(text=key, callback_data=search_options_setup_age_callback.new(**value)))

    kb.row(types.InlineKeyboardButton(
        text=f'{icons.back} Назад', callback_data=search_options_section_callback.new(section='main')))
    return kb


def build_setup_country_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for country in CountriesEnum:
        flag = country_enum_icons.get(country, country_enum_icons[CountriesEnum.ALL])
        kb.insert(types.InlineKeyboardButton(
            text=f"{flag} {country.value}",
            callback_data=search_options_setup_country_callback.new(country=country.value))
        )

    kb.row(types.InlineKeyboardButton(
        text=f'{icons.back} Назад', callback_data=search_options_section_callback.new(section='main')))
    return kb


def build_setup_gender_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)

    for gender in SearchOptionsGenderEnum:
        icon = gender_enum_icons[gender]
        kb.insert(types.InlineKeyboardButton(
            text=f'{icon} {gender.value}',
            callback_data=search_options_setup_gender_callback.new(gender=gender.value))
        )

    kb.row(types.InlineKeyboardButton(
        text=f'{icons.back} Назад', callback_data=search_options_section_callback.new(section='main')))
    return kb
