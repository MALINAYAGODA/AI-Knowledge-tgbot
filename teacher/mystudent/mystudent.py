from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import dp
from db.db_teacher import get_all_data_all_student


@dp.callback_query(lambda c: c.data == "my_students_teacher")
async def searching_next(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    students = await get_all_data_all_student(callback.from_user.id)
    TEACHER_LIST = "Список людей, которых вы хотите собеседовать:\n"
    for student in students:
        TEACHER_LIST += (f"Имя: {student["name"]}\n"
                         f"Уровень: {student['grade']}\n"
                         f"Сфера: {student['sphere']}\n"
                         f"\n\n{student["bio"]}\n"
                         f"Для связи:  @{student['nickname']}\n\n")

    if TEACHER_LIST == "Список людей, которых вы хотите собеседовать:":
        text = "Ваш список пуст"
    else:
        text = TEACHER_LIST
    await callback.message.edit_text(text, reply_markup=keyboard)
