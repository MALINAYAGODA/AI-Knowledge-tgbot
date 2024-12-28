"""
Этот файл отвечает за создание всех встроенных клавиатур
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import NoneData


def sphere_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура создания типов сфер деятельности учителя
    :return: keyboard
    """
    kb = [
        [
            InlineKeyboardButton(text="NLP", callback_data="NLP_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="CV", callback_data="CV_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="RecSys", callback_data="RecSys_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Audio", callback_data="Audio_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Любая", callback_data="Any_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data="return_reg_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def grade_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура создания уровня работы
    :return: keyboard
    """
    kb = [
        [
            InlineKeyboardButton(text="Без грейда", callback_data="no_work_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Intern", callback_data="intern_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Junior", callback_data="junior_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Middle", callback_data="middle_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Senior", callback_data="senior_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data="return_reg_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def reg_teacher(name, grade, sphere, bio) -> InlineKeyboardMarkup:
    """
    Базовая клавиатура выбора пункта для регистрации
    :return: keyboard
    """

    buttons = []
    button_n = [InlineKeyboardButton(text="Имя", callback_data="name_teacher")]
    button_g = [InlineKeyboardButton(text="Уровень", callback_data="grade_teacher")]
    button_s = [InlineKeyboardButton(text="Сфера", callback_data="sphere_teacher")]
    button_b = [InlineKeyboardButton(text="Краткий рассказ", callback_data="description_teacher")]
    if name != NoneData:
        button_n = [InlineKeyboardButton(text="Имя ✅", callback_data="name_teacher")]
    if grade != NoneData:
        button_g = [InlineKeyboardButton(text="Уровень ✅", callback_data="grade_teacher")]
    if sphere != NoneData:
        button_s = [InlineKeyboardButton(text="Сфера ✅", callback_data="sphere_teacher")]
    if bio != NoneData:
        button_b = [InlineKeyboardButton(text="Краткий рассказ ✅", callback_data="description_teacher")]

    buttons.append(button_n)
    buttons.append(button_g)
    buttons.append(button_s)
    buttons.append(button_b)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def reg_teacher_okay() -> InlineKeyboardMarkup:
    """
    Конечная клавиатура выбора пункта для регистрации
    :return: keyboard
    """
    kb = [
        [
            InlineKeyboardButton(text="Имя ✅", callback_data="name_teacher")
        ],
        [
            InlineKeyboardButton(text="Уровень ✅", callback_data="grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Сфера ✅", callback_data="sphere_teacher")
        ],
        [
            InlineKeyboardButton(text="Краткий рассказ ✅", callback_data="description_teacher"),
        ],
        [
            InlineKeyboardButton(text='Все верно', callback_data="reg_teacher_ok"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def reg_return_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура для возвращения на регистрацию
    :return: keyboard
    """
    kb = [
        [
            InlineKeyboardButton(text="Вернуться", callback_data="return_reg_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
