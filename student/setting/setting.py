"""Реализация настроек видимости"""

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

import db.db_student


import student.setting.keyboard as kb
from config import dp


class RegistrateTeacher(StatesGroup):
    show = State()
    wait = State()


DATA = """
Показывать ли мою анкету - {}
"""


async def do_text(state: FSMContext):
    user_data = await state.get_data()
    show = user_data["show"]
    call = user_data['call']
    await db.db_student.change_show_student(call.from_user.id, show)
    show = "Да" if show else "Нет"
    await call.message.edit_text(DATA.format(show),
                                 reply_markup=kb.setting_student())


@dp.callback_query(lambda c: c.data == "setting_student")
async def start_registration(call: CallbackQuery, state: FSMContext):
    user_data = await db.db_student.get_all(call.from_user.id)
    await state.update_data(show=user_data[0]["show"], call=call)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "show_setting")
async def start_registration(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите, показывать ли вас среди списка учителей", reply_markup=kb.show_setting_student())
    await state.set_state(RegistrateTeacher.show)


@dp.callback_query(lambda c: (c.data.split("_")[0] == "show" and c.data.split("_")[2] == "student"))
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.split("_")[1] == "true":
        await state.update_data(show=True)
    elif callback_query.data.split("_")[1] == "false":
        await state.update_data(show=False)
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)
