from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp
from database.models.user import User
from middlewares.userdata import userdata_required
from database.services import UserService
from misc.messages import build_user_profile_text
from states.user_profile import UserProfileState
from keyboards.inline.user_profile import (
    build_user_profile_keyboard, user_profile_section_callback,
    build_user_profile_setup_country_keyboard, user_profile_setup_country_callback,
    build_user_profile_setup_gender_keyboard, user_profile_setup_gender_callback
)


async def show_user_profile(message: types.Message, user: User, edit_message=False):
    text, parse_mode = await build_user_profile_text(user)
    keyboard = build_user_profile_keyboard()

    if edit_message:
        return await message.edit_text(text=text, parse_mode=parse_mode, reply_markup=keyboard)
    return await message.answer(text=text, parse_mode=parse_mode, reply_markup=keyboard)


@userdata_required
@dp.message_handler(Text(equals=['/user_profile']))
async def process_show_user_profile(message: types.Message, user: User):
    await show_user_profile(message, user)


# BACK BUTTON
@dp.callback_query_handler(user_profile_section_callback.filter(section='main'))
async def process_user_profile_section_back_callback(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=build_user_profile_keyboard())
    await call.answer()


# SETUP USER AGE
@dp.callback_query_handler(user_profile_section_callback.filter(section='setup_age'), state='*')
async def process_user_profile_setup_age_callback(call: types.CallbackQuery):
    await UserProfileState.setup_age.set()
    await call.message.answer(text='Сколько вам полных лет?')
    await call.answer()


@dp.message_handler(state=UserProfileState.setup_age)
async def process_user_profile_setup_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer('Возраст должен быть числом')

    user = await UserService.setup_age(message.from_user.id, message.text)
    await state.reset_state()
    await message.answer(text=f'Возраст изменен на {user.age}')
    await show_user_profile(message, user)


# SETUP USER COUNTRY
@dp.callback_query_handler(user_profile_section_callback.filter(section='setup_country'))
async def process_user_profile_setup_callback(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=build_user_profile_setup_country_keyboard())
    await call.answer()


@dp.callback_query_handler(user_profile_setup_country_callback.filter())
async def process_user_profile_setup_country(call: types.CallbackQuery, callback_data: dict):
    country = callback_data.get('country')
    user = await UserService.setup_country(call.from_user.id, country)
    await show_user_profile(call.message, user, edit_message=True)
    await call.answer(f'Страна изменена на {user.country.name.value}')


# SETUP USER GENDER
@dp.callback_query_handler(user_profile_section_callback.filter(section='setup_gender'))
async def process_user_profile_setup_gender_callback(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=build_user_profile_setup_gender_keyboard())
    await call.answer()


@dp.callback_query_handler(user_profile_setup_gender_callback.filter())
async def process_user_profile_setup_gender(call: types.CallbackQuery, callback_data: dict):
    gender = callback_data.get('gender')
    print(gender)
    user = await UserService.setup_gender(user=call.from_user.id, gender=gender)
    await show_user_profile(message=call.message, user=user, edit_message=True)
    await call.answer()
