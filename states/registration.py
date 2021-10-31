from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    setup_gender = State()
    setup_country = State()
    setup_age = State()
