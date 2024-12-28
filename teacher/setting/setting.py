"""Реализация настроек"""

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import db.db_teacher
import teacher.setting.keyboard as kb
from config import dp
from db.db_teacher import check_id

DATA = """
Показывать ли мою анкету - {}
"""


async def do_text(state: FSMContext):
    """
    Функция, отвечающая за вывод всех данных
    :param state: FSMContext
    :return: --, но меняет сообшение
    """
    user_data = await state.get_data()
    show = user_data["show"]
    call = user_data['call']
    db.db_teacher.change_show(call.from_user.id, show)
    show = "Да" if show else "Нет"
    await call.message.edit_text(DATA.format(show),
                                 reply_markup=kb.setting_teacher())


@dp.callback_query(lambda c: c.data == "setting_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    """
    Реагирует на кнопку настроек, обновляет данные состояний
    :param call: CallbackQuery
    :param state: FSMContext
    :return: --, на выходе вызывает do_text
    """
    user, i = check_id(call.from_user.id)
    await state.update_data(show=user.show, call=call)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "show_setting_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    """
    Реагирует на кнопку смены показа учителя
    :param call: CallbackQuery
    :param state: FSMContext
    :return: --, меняет текст для смены показа
    """
    await call.message.edit_text("Выберите, показывать ли вас среди списка учителей",
                                 reply_markup=kb.show_setting_teacher())


@dp.callback_query(lambda c: (c.data.split("_")[0] == "show" and c.data.split("_")[2] == "teacher"))
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Реагирует на кнопки смены показа
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return: --, в конце вызывает do_text
    """
    if callback_query.data.split("_")[1] == "true":
        await state.update_data(show=True)
    elif callback_query.data.split("_")[1] == "false":
        await state.update_data(show=False)
    await do_text(state)
