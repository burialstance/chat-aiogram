from database.types import SearchOptionsSexEnum, UserSexEnum
import misc.icon_characters as icons

sex_type_icons = {
    SearchOptionsSexEnum.MALE: icons.man,
    SearchOptionsSexEnum.FEMALE: icons.woman,
    SearchOptionsSexEnum.ALL: icons.couple,

    UserSexEnum.MALE: icons.man,
    UserSexEnum.FEMALE: icons.woman,
    UserSexEnum.UNKNOWN: icons.eyes
}