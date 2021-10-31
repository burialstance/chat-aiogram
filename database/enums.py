from enum import Enum


class UserGenderEnum(Enum):
    MALE = 'мужской'
    FEMALE = 'женский'
    UNKNOWN = 'неизвестный'


class SearchOptionsGenderEnum(Enum):
    MALE = 'мужской'
    FEMALE = 'женский'
    ALL = 'все'


class CountriesEnum(Enum):
    RUSSIA = 'Россия'
    UKRAINE = 'Украина'
    BELARUS = 'Беларусь'
    KAZAKHSTAN = 'Казахстан'
    UZBEKISTAN = 'Узбекистан'
    TAJIKISTAN = 'Таджикистан'
    TURKMENISTAN = 'Туркменистан'
    AZERBAIJAN = 'Азербайджан'
    ARMENIA = 'Армения'
    MOLDOVA = 'Молдова'
    ALL = 'Все'
