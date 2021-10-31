from database.enums import SearchOptionsGenderEnum, UserGenderEnum
import misc.icon_characters as icons

gender_enum_icons = {
    SearchOptionsGenderEnum.MALE: icons.man,
    SearchOptionsGenderEnum.FEMALE: icons.woman,
    SearchOptionsGenderEnum.ALL: icons.couple,

    UserGenderEnum.MALE: icons.man,
    UserGenderEnum.FEMALE: icons.woman,
    UserGenderEnum.UNKNOWN: icons.eyes
}