"""
Клавиатуры для начального блока
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#
# def starting_kb() -> InlineKeyboardMarkup:
#     buttons = [
#         [InlineKeyboardButton(text="student", callback_data="info")],
#         [InlineKeyboardButton(text="teacher", callback_data="teacher")],
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard


def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Регистрация", callback_data="registration")],
        [InlineKeyboardButton(text="Поиск", callback_data="cmd_go")],
        [InlineKeyboardButton(text="Видимость", callback_data="setting_student")],
        [InlineKeyboardButton(text="Список твоих интервьюеров", callback_data="teacher_list")],
        [InlineKeyboardButton(text="Вернуться к выбору роли", callback_data="return_to_start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

#
# def return_go_kb() -> InlineKeyboardMarkup:
#     buttons = [
#         [InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard
#
#
# def cmd_filters_kb() -> InlineKeyboardMarkup:
#     buttons = [
#         [InlineKeyboardButton(text="Выбрать уровень", callback_data="gradef")],
#         [InlineKeyboardButton(text="Выбрать сферу", callback_data="spheref")],
#         [InlineKeyboardButton(text="Применить и перейти", callback_data="fsearch")],
#         [InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
#
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard
