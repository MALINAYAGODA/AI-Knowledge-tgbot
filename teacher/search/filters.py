import random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import db.db_student
from db.db_student import insert_into_ts
from db.db_teacher import get_filter_students, get_all_student, check_id, get_one_student
from start.start import student_info
from teacher.search import keyboard as kb

from config import dp, NoneData, bot


class Filters(StatesGroup):
    grade = State()
    sphere = State()
    wait = State()


FILTER_DATA = """
В данный момент выбраны фильтры:

Уровень:   {}

Сфера:   {}
"""


async def print_filters(state: FSMContext):
    filter_data = await state.get_data()

    g = filter_data['grade']
    s = filter_data['sphere']

    call = filter_data['call']
    await call.message.edit_text(text=FILTER_DATA.format(g, s),
                                 reply_markup=kb.cmd_filters_kb())


@dp.callback_query(lambda c: c.data == "filters_students")
async def cmd_filters(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(grade=NoneData, sphere=NoneData, call=callback)
    await print_filters(state)


@dp.callback_query(lambda c: c.data == "returnf_teacher")
async def choice_returning(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Filters.wait)
    await print_filters(state)


# !!!!!!!! grade choice
@dp.callback_query(lambda c: c.data == "gradef_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Выберите уровень подготовки", reply_markup=kb.fchoose_grade_kb())
    await state.set_state(Filters.grade)


@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["gradef", "teacher"])
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    g = filter_data['grade']
    tt = " ".join(callback_query.data.split("_")[:-2])
    if g == NoneData:
        await state.update_data(grade=tt)
    elif tt in g:
        tt = ", ".join([i for i in "".join(g.split(tt)).split(", ") if i != ""])
        await state.update_data(grade=tt)
    else:
        tt = g + ", " + tt
        await state.update_data(grade=tt)
    await callback_query.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                                  "нажмите повторно чтобы убрать",
                                           reply_markup=kb.fchoose_grade_kb())
    await state.set_state(Filters.wait)

# !!!!!!!!


# ///////////// sphere choice
@dp.callback_query(lambda c: c.data == "spheref_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    if s == NoneData:
        await callback_query.message.edit_text("Выберите ваши сферы деятельности", reply_markup=kb.fchoose_sphere_kb())
    else:
        await callback_query.message.edit_text("Выбрано " + s + "\n\nВыберите дополнительно или "
                                                                "нажмите повторно чтобы убрать",
                                               reply_markup=kb.fchoose_sphere_kb())
    await state.set_state(Filters.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["spheref", "teacher"])
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    tt = " ".join(callback_query.data.split("_")[:-2])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback_query.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                                  "нажмите повторно чтобы убрать",
                                           reply_markup=kb.fchoose_sphere_kb())
    await state.set_state(Filters.wait)


# /////////////


TEACHER_DATAf = """
Имя:    {}
Уровень:    {}
Сфера:    {}
Краткий рассказ:
{}
"""


async def print_teacherf(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(teacher_list):
        teacher = teacher_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATAf.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=kb.fsearching_kb()
        )
    else:
        await state.clear()
        await callback.message.edit_text(
            text="студенты закончились((",
            reply_markup=kb.return_go_kb()
        )


async def get_random_teachersf(grade, sphere, teacher_id) -> list[dict]:
    list_ = await get_filter_students(grade, sphere, teacher_id)
    random.shuffle(list_)
    return list_


@dp.callback_query(lambda c: c.data == "fsearch_teacher")
async def searching(callback: CallbackQuery, state: FSMContext):
    teacher_data = await state.get_data()
    gr = teacher_data["grade"]
    sp = teacher_data["sphere"]
    if "list" not in teacher_data:
        random_list = await get_random_teachersf(gr, sp, callback.from_user.id)
        await state.update_data(list=random_list, index=0)
        await print_teacherf(callback, state)


@dp.callback_query(lambda c: c.data == "fnext_student")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_teacherf(callback, state)


STUDENT_DATA = """
Новая заявка от учителя

Имя:    {}
Уровень:    {}
Сфера:    {}
Краткий рассказ:
{}
"""


@dp.callback_query(lambda c: c.data == "agreef_teacher")
async def agree_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    list_ = data["list"]
    index_ = data["index"]
    user_id = list_[index_]["id"]
    teacher, i = check_id(callback.from_user.id)

    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data=f"{callback.from_user.id}_acceptf_teacher")],
        [InlineKeyboardButton(text="Отказать", callback_data=f"{callback.from_user.id}_denyf_teacher")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(user_id, STUDENT_DATA.format(teacher.name, teacher.grade,
                                                        teacher.sphere, teacher.description), reply_markup=keyboard)
    data = await state.get_data()
    index = data.get("index", 0) + 1
    await callback.answer(text="Заявка отправлена")

    await state.update_data(index=index)
    await print_teacherf(callback, state)

RESPONSE_TEACHER_DATA_ACCEPT = """
Ваша заявка для ученика

Имя:       {}
Уровень:   {}
Сфера:     {}
Краткий рассказ:
{}

была ПРИНЯТА
Никнейм для связи: @{}
"""

RESPONSE_TEACHER_DATA_DENY = """
Ваша заявка для ученика

Имя:       {}
Уровень:   {}
Сфера:     {}
Краткий рассказ:
{}

была ОТКЛОНЕНА
"""

@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["acceptf", "teacher"])
async def deny_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Ок", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    teacher_id = callback.from_user.id
    student_id = int(callback.data.split("_")[0])
    teacher, i = check_id(student_id)
    student_info = (await db.db_student.get_all(teacher_id))[0]
    print(student_info)
    await insert_into_ts(student_id, teacher_id, teacher.nickname, callback.from_user.username)

    await bot.send_message(student_id,
                           RESPONSE_TEACHER_DATA_ACCEPT.format(student_info["name"], student_info["grade"],
                                                               student_info["sphere"], student_info["bio"],
                                                               student_info["nickname"]),
                           reply_markup=keyboard)

    await callback.answer(text="Вы приняли заявку")
    await callback.message.delete()

@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["denyf", "teacher"])
async def deny_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Ок", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    student_id = callback.from_user.id
    teacher_info = (await db.db_student.get_all(student_id))[0]
    await bot.send_message(int(callback.data.split("_")[0]),
                           RESPONSE_TEACHER_DATA_DENY.format(teacher_info["name"], teacher_info["grade"],
                                                             teacher_info["sphere"], teacher_info["bio"]),
                           reply_markup=keyboard)

    await callback.answer(text="Вы отклонили заявку")
    await callback.message.delete()

@dp.callback_query(lambda c: c.data == "ok")
async def deny_request(callback: CallbackQuery):
    await callback.message.delete()

