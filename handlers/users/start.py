from typing import Optional

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode

from loader import dp, bot
from database.models.user import User
from database.services import UserService
from middlewares.userdata import userdata_required
from misc.messages import START_COMMAND_TEXT
from states.registration import RegistrationState
from keyboards.default.registration import build_registration_setup_country_keyboard, build_registration_setup_gender
from database.enums import CountriesEnum, UserGenderEnum



# @userdata_required
@dp.message_handler(CommandStart())
async def process_start_command(message: types.Message, state: FSMContext):
    user_exists = await UserService.user_exists(telegram_id=message.from_user.id)
    if not user_exists:
        await registration_new_user(telegram_id=message.from_user.id, state=state, referred_id=message.get_args())


async def registration_new_user(telegram_id, state: FSMContext, referred_id: Optional[int] = None):
    referred_id = referred_id if any([isinstance(referred_id, str) and referred_id.isdigit(),
                                      isinstance(referred_id, int)]) else None
    await state.update_data({'telegram_id': telegram_id, 'referred_id': referred_id})

    await RegistrationState.setup_country.set()
    await bot.send_message(
        chat_id=telegram_id, text='Укажи страну',
        reply_markup=build_registration_setup_country_keyboard()
    )


@dp.message_handler(state=RegistrationState.setup_country)
async def process_registration_setup_country(message: types.Message, state: FSMContext):
    country = message.text.split()[-1]
    if country not in [c.value for c in CountriesEnum if c != CountriesEnum.ALL]:
        return await message.answer('Выберите страну из предлагаемых на клавиатуре снизу')
    await state.update_data({'country_name': country})

    await RegistrationState.setup_gender.set()
    await message.answer(
        'Страна указана, теперь скажи, какого ты пола?',
        reply_markup=build_registration_setup_gender()
    )


@dp.message_handler(state=RegistrationState.setup_gender)
async def process_registration_setup_gender(message: types.Message, state: FSMContext):
    gender = message.text.split()[-1]
    if gender not in [UserGenderEnum.MALE.value, UserGenderEnum.FEMALE.value]:
        return await message.answer('Выбери пол из клавиатуры снизу')
    await state.update_data({'gender': gender})

    await RegistrationState.setup_age.set()
    await message.answer(
        'Отлично, осталось самое последнее, сколько тебе лет?',
        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=RegistrationState.setup_age)
async def process_registration_setup_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        return await message.answer('Возраст отправляем цифрами')
    is_child = lambda user_age: 0 <= int(user_age) < 6
    if is_child(age):
        return await message.answer('делай уроки')

    await state.update_data({'age': int(age)})
    async with state.proxy() as data:
        user_kwargs = data.as_dict()
        print(user_kwargs)
    user = await UserService.create(**user_kwargs)
    await state.reset_state(with_data=True)
    print(user)
