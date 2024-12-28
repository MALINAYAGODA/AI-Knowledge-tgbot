"""
Реализация рандомного поиска
"""
import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db.db_student import get_all_teachers, get_teacher_by_id, insert_into_ts, get_all
from config import bot, dp
from student.search import keyboard as kb


@dp.callback_query(lambda c: c.data == "cmd_go")
async def cmd_go(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="""
            Ты можешь выставить определенные фильтры \nили искать по всем подряд
            """,
        reply_markup=kb.search_or_filters_kb()
    )


async def get_random_teachers(id_student) -> list[dict]:
    list_ = await get_all_teachers(id_student)
    random.shuffle(list_)
    return list_


TEACHER_DATA = """
Анкета

Имя: {}
Уровень: {}
Сфера: {}

{}
"""


async def display_teachers(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(teacher_list):
        teacher = teacher_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=kb.searching_kb()
        )
    else:
        await callback.message.edit_text(
            text="Новых заявок нет",
            reply_markup=kb.return_go_kb()
        )


@dp.callback_query(lambda c: c.data == "search")
async def searching(callback: CallbackQuery, state: FSMContext):
    # бесполезные строки, но могут помочь при развитии функционала (state чистится в cmd_go)
    # teacher_data = await state.get_data()
    # if "list" not in teacher_data:
    random_list = await get_random_teachers(callback.from_user.id)
    await state.update_data(list=random_list, index=0)
    await display_teachers(callback, state)


@dp.callback_query(lambda c: c.data == "next_teacher")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await display_teachers(callback, state)


STUDENT_DATA = """
Новая заявка! Этот человек хочет пройти с тобой собеседование:

Имя:    {}
Уровень:    {}
Сфера:    {}

{}
"""


@dp.callback_query(lambda c: c.data == "agree")
async def agree_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    list_ = data["list"]
    index_ = data["index"]

    user_id = list_[index_]["id"]
    user_info = (await get_all(callback.from_user.id))[0]

    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data=f"{callback.from_user.id}_accept")],
        [InlineKeyboardButton(text="Отказать", callback_data=f"{callback.from_user.id}_deny")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(user_id, STUDENT_DATA.format(user_info["name"], user_info["grade"],
                                                        user_info["sphere"], user_info["bio"]), reply_markup=keyboard)
    data = await state.get_data()
    index = data.get("index", 0) + 1
    await callback.answer(text="Заявка отправлена")

    await state.update_data(index=index)
    await display_teachers(callback, state)


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

@dp.callback_query(lambda c: c.data.split("_")[-1] == "accept")
async def accept_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Ок", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    teacher_id = callback.from_user.id
    student_id = int(callback.data.split("_")[0])

    teacher_info = (await get_teacher_by_id(teacher_id))[0]
    student_info = (await get_all(student_id))[0]

    await insert_into_ts(teacher_id, student_id, callback.from_user.username,
                         student_info["nickname"]) # тут происходит какая-то магия почему запрос ломается никто не знает

    await bot.send_message(student_id,
                           RESPONSE_TEACHER_DATA_ACCEPT.format(teacher_info["name"], teacher_info["grade"],
                                                               teacher_info["sphere"], teacher_info["bio"],
                                                               teacher_info["nickname"]),
                           reply_markup=keyboard)

    await callback.answer(text="Вы приняли заявку")
    await callback.message.delete()

@dp.callback_query(lambda c: c.data.split("_")[-1] == "deny")
async def deny_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Ок", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    teacher_id = callback.from_user.id
    teacher_info = (await get_teacher_by_id(teacher_id))[0]
    await bot.send_message(int(callback.data.split("_")[0]),
                           RESPONSE_TEACHER_DATA_DENY.format(teacher_info["name"], teacher_info["grade"],
                                                             teacher_info["sphere"], teacher_info["bio"]),
                           reply_markup=keyboard)

    await callback.answer(text="Вы отклонили заявку")
    await callback.message.delete()

@dp.callback_query(lambda c: c.data == "ok")
async def deny_request(callback: CallbackQuery):
    await callback.message.delete()
