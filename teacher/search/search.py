"""Поиск без фильтра"""

import random

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import bot, dp
from db.db_student import insert_into_ts, get_all
from db.db_teacher import get_all_student, check_id, get_one_student
from teacher.search import keyboard as kb


@dp.callback_query(lambda c: c.data == "new_students_teacher")
async def cmd_go(callback: CallbackQuery, state: FSMContext):
    """
    Обработка основного окна поиска
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: --, меняет сообщение
    """
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="""
            Ты можешь выставить определенные фильтры \nили искать по всем подряд
            """,
        reply_markup=kb.search_or_filters_kb()
    )


async def get_random_student(usr_id: int) -> list[dict]:
    """
    Создает массив студентов для прохода по ним
    :param usr_id:
    :return: list[dict]
    """
    list_ = await get_all_student(usr_id)
    random.shuffle(list_)
    return list_


TEACHER_DATA = """
Анкета

Имя: {}
Уровень: {}
Сфера: {}

{}
"""


async def print_search(callback: CallbackQuery, state: FSMContext):
    """
    Меняет сообщение на нового студента
    :param callback:
    :param state:
    :return:
    """
    data = await state.get_data()
    students_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(students_list):
        teacher = students_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=kb.searching_kb()
        )
    else:
        await callback.message.edit_text(
            text="Новых анкет нет",
            reply_markup=kb.return_go_kb()
        )


@dp.callback_query(lambda c: c.data == "search_students")
async def searching(callback: CallbackQuery, state: FSMContext):
    # бесполезные строки, но могут помочь при развитии функционала (state чистится в cmd_go)
    # teacher_data = await state.get_data()
    # if "list" not in teacher_data:
    random_list = await get_random_student(callback.from_user.id)
    await state.update_data(list=random_list, index=0)
    await print_search(callback, state)


@dp.callback_query(lambda c: c.data == "next_student")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_search(callback, state)


STUDENT_DATA = """
Новая заявка! Этот человек хочет провести с вами собеседование:

Имя:    {}
Уровень:    {}
Сфера:    {}

{}
"""


@dp.callback_query(lambda c: c.data == "agree_teacher")
async def agree_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    list_ = data["list"]
    index_ = data["index"]
    user_id = list_[index_]["id"]
    teacher, i = check_id(callback.from_user.id)

    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data=f"{callback.from_user.id}_accept_teacher")],
        [InlineKeyboardButton(text="Отказать", callback_data=f"{callback.from_user.id}_deny_teacher")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(user_id, STUDENT_DATA.format(teacher.name, teacher.grade,
                                                        teacher.sphere, teacher.description), reply_markup=keyboard)
    await callback.answer(text="Заявка отправлена")
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_search(callback, state)


RESPONSE_TEACHER_DATA_ACCEPT = """
Ваша заявка на интервью от

Имя: {}
Уровень: {}
Сфера: {}

{}

была ПРИНЯТА
Никнейм для связи: @{}
"""

RESPONSE_TEACHER_DATA_DENY = """
Ваша заявка на интервью от

Имя:       {}
Уровень:   {}
Сфера:     {}

{}

была ОТКЛОНЕНА
"""

@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["accept", "teacher"])
async def deny_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Ок", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    teacher_id = callback.from_user.id
    student_id = int(callback.data.split("_")[0])
    teacher, i = check_id(student_id)
    student_info = (await get_all(teacher_id))[0]
    await insert_into_ts(student_id, teacher_id, teacher.nickname, callback.from_user.username)

    await bot.send_message(student_id,
                           RESPONSE_TEACHER_DATA_ACCEPT.format(student_info["name"], student_info["grade"],
                                                               student_info["sphere"], student_info["bio"],
                                                               student_info["nickname"]),
                           reply_markup=keyboard)

    await callback.answer(text="Вы приняли заявку")
    await callback.message.delete()

@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["deny", "teacher"])
async def deny_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Ок", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    student_id = callback.from_user.id
    teacher_info = (await get_all(student_id))[0]
    await bot.send_message(int(callback.data.split("_")[0]),
                           RESPONSE_TEACHER_DATA_DENY.format(teacher_info["name"], teacher_info["grade"],
                                                             teacher_info["sphere"], teacher_info["bio"]),
                           reply_markup=keyboard)

    await callback.answer(text="Вы отклонили заявку")
    await callback.message.delete()

@dp.callback_query(lambda c: c.data == "ok")
async def deny_request(callback: CallbackQuery):
    await callback.message.delete()
