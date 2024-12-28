"""
Вывод списка учителей для 'студента'
"""
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import dp, bot
from db.db_student import get_teacher_list


@dp.callback_query(lambda query: query.data == "teacher_list")
async def student_info(callback: CallbackQuery):
    list_ = await get_teacher_list(callback.from_user.id)

    TEACHER_LIST = "Список людей, которые согласились тебя пособесить:\n"
    if list_:
        for tch in list_:
            TEACHER_LIST += (f"Имя: {tch["name"]}\n"
                             f"Уровень: {tch['grade']}\n"
                             f"Сфера: {tch['sphere']}\n"
                             f"\n\n{tch['description']}\n"
                             f"Для связи: @{tch['nickname']}\n\n")
    else:
        TEACHER_LIST = "Ваш список пуст"

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="info")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=TEACHER_LIST,
        reply_markup=keyboard
    )