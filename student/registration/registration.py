"""
Реализация регистрации 'студента'
"""
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config import dp, bot
from db.db_student import get_all, update_all, insert_all
from student.registration import keyboard as kb


class Registration(StatesGroup):
    name = State()
    grade = State()
    sphere = State()
    bio = State()
    wait = State()


DATA = """
Ваши данные
Имя: {}
Уровень: {}
Сфера: {}
Описание: 
{}
"""

NoneData = ""


async def display_student(state: FSMContext):
    student_data = await state.get_data()

    n = student_data['name']
    g = student_data['grade']
    s = student_data['sphere']
    b = student_data['bio']

    call = student_data['call']
    if n != NoneData and g != NoneData and s != NoneData and b != NoneData:
        await call.message.edit_text(text="Проверьте введенные данные и если все "
                                          "верно нажмите на соответсвующую кнопку \n\n" +
                                          DATA.format(n, g, s, b),
                                     reply_markup=kb.registration_okay_kb())
    else:
        await call.message.edit_text(DATA.format(n, g, s, b),
                                     reply_markup=kb.dynamic_choosing_kb(n, g, s, b))  # kb.registration_kb() - была,
        # но она без галочек, Денчику не кайф((


@dp.callback_query(lambda c: c.data == "registration")
async def cmd_reg(callback: CallbackQuery, state: FSMContext):
    student_data = await get_all(callback.from_user.id)
    if student_data:
        student_data = student_data[0]
        await state.update_data(name=student_data["name"], grade=student_data["grade"], sphere=student_data["sphere"],
                                bio=student_data["bio"], call=callback)
    else:
        await state.update_data(name=NoneData, grade=NoneData, sphere=NoneData, bio=NoneData, call=callback)

    await display_student(state)


@dp.callback_query(lambda c: c.data == "return")
async def return_to_cmd_reg(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.wait)
    await display_student(state)


@dp.callback_query(lambda c: c.data == "name")
async def fill_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите, как к вам обращаться", reply_markup=kb.return_kb())
    await state.set_state(Registration.name)
    await state.update_data(call=callback)


@dp.callback_query(lambda c: c.data == "grade")
async def choose_grade(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите уровень вашей квалификации", reply_markup=kb.choose_grade_kb())
    await state.set_state(Registration.grade)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "grade")
async def choose_grade(callback: CallbackQuery, state: FSMContext):
    tt =  " ".join(callback.data.split("_")[:-1]).capitalize()
    if tt == "No work":
        tt = "Без грейда"
    await state.update_data(grade=tt)
    await display_student(state)
    await state.set_state(Registration.wait)


@dp.callback_query(lambda c: c.data == "sphere")
async def choose_sphere(callback: CallbackQuery, state: FSMContext):
    student_data = await state.get_data()
    s = student_data['sphere']
    if s == NoneData:
        await callback.message.edit_text("Выберите сферы AI, в которых вы специализируетесь", reply_markup=kb.choose_sphere_kb())
    else:
        await callback.message.edit_text("Выбрано: " + s + "\nВыберите дополнительно или нажмите повторно чтобы убрать",
                                         reply_markup=kb.choose_sphere_kb())
    await state.set_state(Registration.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "sphere")
async def choose_sphere(callback: CallbackQuery, state: FSMContext):
    student_data = await state.get_data()
    s = student_data['sphere']
    tt = " ".join(callback.data.split("_")[:-1])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback.message.edit_text(text="Выбрано: " + tt + "\nВыберите дополнительно или нажмите повторно чтобы убрать",
                                     reply_markup=kb.choose_sphere_kb())
    await state.set_state(Registration.wait)


@dp.callback_query(lambda c: c.data == "bio")
async def fill_bio(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Расскажите немного о себе для вашего будущего собеседника", reply_markup=kb.return_kb())
    await state.set_state(Registration.bio)
    await state.update_data(call=callback)


@dp.message(StateFilter(Registration.name))
async def end_fill_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.delete()
    await display_student(state)
    await state.set_state(Registration.wait)


@dp.message(StateFilter(Registration.bio))
async def end_fill_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.delete()
    await display_student(state)
    await state.set_state(Registration.wait)


ALL_OKAY_TEXT = """
Регистрация успешно завершена, все изменения внесены
    
Вот список функций, которые вы можете использовать для поиска собеседований:

⚙️ Регистрация/изменение данных - заполнить или изменить свою информацию.

🔍 Поиск - поиск людей, с которыми можно пройти собеседование

👀 Видимость - показывать ли мою анкету другим людям

📋 Список твоих интервьюеров - список людей, которые взяли тебя на собеседование
"""


@dp.callback_query(lambda c: c.data == "all_is_okay")
async def end_reg(callback: CallbackQuery, state: FSMContext):
    student_id = callback.from_user.id
    student_data = await state.get_data()
    if await get_all(student_id):
        await update_all(student_id, student_data["name"], student_data["grade"], student_data["sphere"],
                         student_data["bio"])
    else:
        await insert_all(student_id, student_data["name"], student_data["grade"], student_data["sphere"],
                         student_data["bio"], callback.from_user.username)

    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=ALL_OKAY_TEXT,
        reply_markup=kb.info_and_continue_kb()
    )
