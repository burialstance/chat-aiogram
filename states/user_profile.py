from aiogram.dispatcher.filters.state import StatesGroup, State


class UserProfileState(StatesGroup):
    setup_sex = State()
    setup_age = State()
    setup_country = State()

class RegistrationState(StatesGroup):
    setup_sex = State()
    setup_country = State()
    setup_age = State()
