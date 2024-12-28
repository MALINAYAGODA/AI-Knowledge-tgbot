"""
Этот файл отвечает за создание клавиатур настроек
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def setting_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора настроек
    :return: InlineKeyboardMarkup
    """
    kb = [
        [
            InlineKeyboardButton(text="Изменить статус видимости", callback_data="show_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data="start"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard



def show_setting_teacher() -> InlineKeyboardMarkup:
    """
    клавиатура выбора показывать ли себя
    :return:InlineKeyboardMarkup
    """
    kb = [
        [
            InlineKeyboardButton(text="Да", callback_data="show_true_teacher"),
            InlineKeyboardButton(text="Нет", callback_data="show_false_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
