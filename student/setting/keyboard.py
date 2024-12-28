"""
Создание клавиатур для блока настроек видимости
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def setting_student() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора настроек
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="Изменить статус видимости", callback_data="show_setting"),
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data="info"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard



def show_setting_student() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора показывать ли себя
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="Да", callback_data="show_true_student"),
            InlineKeyboardButton(text="Нет", callback_data="show_false_student"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
