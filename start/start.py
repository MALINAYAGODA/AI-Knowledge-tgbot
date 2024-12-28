"""
Начальный блок
"""
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import dp, bot
from db.db_student import get_teacher_list
from db.db_teacher import check_id
import start.keyboard as kb


@dp.callback_query(lambda c: c.data == "start")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user, i = check_id(callback_query.from_user.id)
    if i == 0:
        kb = [
            [
                InlineKeyboardButton(text="Регистрация", callback_data="teacher"),
            ]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback_query.message.edit_text("Здраствуйте, сначала пройдите регистрацию", reply_markup=keyboard)
    else:
        kb = [
            [
                InlineKeyboardButton(text="Изменить анкету", callback_data="teacher"),
            ],
            [
                InlineKeyboardButton(text="⚙️ Настройки", callback_data="setting_teacher"),
            ],
            [
                InlineKeyboardButton(text="🔍 Поиск собеседника", callback_data="new_students_teacher"),
            ],
            [
                InlineKeyboardButton(text="Люди которых вы хотите собеседовать", callback_data="my_students_teacher"),
            ],
            [InlineKeyboardButton(text="Вернуться", callback_data="return_to_start")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        DATA = """
                Привет! Твоя анкета:

Имя: {}
Уровень: {}
Сфера: {}
Описание: 
{}
"""
        await callback_query.message.edit_text(
            DATA.format(user.name, user.grade, user.sphere, user.description),
            reply_markup=keyboard)

start_message = """Привет! Это бот от AI Knowledge Club для поиска собеседований и мок-интервью⚡️

Выберите свою роль:
"""

@dp.callback_query(lambda c: c.data == "return_to_start")
async def cmd_start(callback_query: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="Хочу пройти собеседование", callback_data="info")],
        [InlineKeyboardButton(text="Хочу провести собеседование", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await callback_query.message.edit_text(start_message, reply_markup=keyboard)


INFO_TEXT = """
Вот список функций, которые вы можете использовать для поиска собеседований:

⚙️ Регистрация/изменение данных - заполнить или изменить свою информацию.

🔍 Поиск - поиск людей, с которыми можно пройти собеседование

👀 Видимость - показывать ли мою анкету другим людям

📋 Список твоих интервьюеров - список людей, которые взяли тебя на собеседование
"""


@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [InlineKeyboardButton(text="Хочу пройти собеседование", callback_data="info")],
        [InlineKeyboardButton(text="Хочу провести собеседование", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(start_message, reply_markup=keyboard)



@dp.callback_query(lambda query: query.data == "info")
async def student_info(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=INFO_TEXT,
        reply_markup=kb.info_and_continue_kb()
    )

