"""
Реализация рандомного поиска с фильтрами
"""
import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from db.db_student import get_filter_teachers, insert_into_ts
from db.db_teacher import check_id, get_all_student
from student.search import keyboard as kb

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


async def display_filters(state: FSMContext):
    filter_data = await state.get_data()

    g = filter_data['grade']
    s = filter_data['sphere']

    call = filter_data['call']
    await call.message.edit_text(text=FILTER_DATA.format(g, s),
                                 reply_markup=kb.cmd_filters_kb())


@dp.callback_query(lambda c: c.data == "filters")
async def cmd_filters(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(grade=NoneData, sphere=NoneData, call=callback)
    await display_filters(state)


@dp.callback_query(lambda c: c.data == "returnf")
async def filter_return(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Filters.wait)
    await display_filters(state)


@dp.callback_query(lambda c: c.data == "gradef")
async def choose_grade(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите уровень подготовки", reply_markup=kb.fchoose_grade_kb())
    await state.set_state(Filters.grade)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "gradef")
async def choose_grade(callback: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    g = filter_data['grade']
    tt = " ".join(callback.data.split("_")[:-1])
    if g == NoneData:
        await state.update_data(grade=tt)
    elif tt in g:
        tt = ", ".join([i for i in "".join(g.split(tt)).split(", ") if i != ""])
        await state.update_data(grade=tt)
    else:
        tt = g + ", " + tt
        await state.update_data(grade=tt)
    await callback.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                            "нажмите повторно чтобы убрать",
                                     reply_markup=kb.fchoose_grade_kb())
    await state.set_state(Filters.wait)


@dp.callback_query(lambda c: c.data == "spheref")
async def choose_sphere(callback: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    if s == NoneData:
        await callback.message.edit_text("Выберите ваши сферы деятельности", reply_markup=kb.fchoose_sphere_kb())
    else:
        await callback.message.edit_text("Выбрано " + s + "\n\nВыберите дополнительно или "
                                                          "нажмите повторно чтобы убрать",
                                         reply_markup=kb.fchoose_sphere_kb())
    await state.set_state(Filters.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "spheref")
async def choose_sphere(callback: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    tt = " ".join(callback.data.split("_")[:-1])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                            "нажмите повторно чтобы убрать",
                                     reply_markup=kb.fchoose_sphere_kb())
    await state.set_state(Filters.wait)


TEACHER_DATAf = """
Имя:    {}
Уровень:    {}
Сфера:    {}
Краткий рассказ:
{}
"""


async def display_filter_teachers(callback: CallbackQuery, state: FSMContext):
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
            text="Учителя закончились((",
            reply_markup=kb.return_go_kb()
        )


async def get_random_teachersf(grade, sphere, id_student) -> list[dict]:
    list_ = await get_filter_teachers(grade, sphere, id_student)
    random.shuffle(list_)
    return list_


@dp.callback_query(lambda c: c.data == "fsearch")
async def searching(callback: CallbackQuery, state: FSMContext):
    teacher_data = await state.get_data()
    gr = teacher_data["grade"]
    sp = teacher_data["sphere"]
    if "list" not in teacher_data:
        random_list = await get_random_teachersf(gr, sp, callback.from_user.id)
        await state.update_data(list=random_list, index=0)
        await display_filter_teachers(callback, state)


@dp.callback_query(lambda c: c.data == "fnext_teacher")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await display_filter_teachers(callback, state)
