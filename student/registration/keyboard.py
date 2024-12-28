"""
Создание всех встроенных клавиатур для 'студента'
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from student.search.filters import NoneData


def registration_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Имя", callback_data="name")],
        [InlineKeyboardButton(text="Уровень", callback_data="grade")],
        [InlineKeyboardButton(text="Сфера", callback_data="sphere")],
        [InlineKeyboardButton(text="Краткий рассказ", callback_data="bio")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def dynamic_choosing_kb(name, grade, sphere, bio) -> InlineKeyboardMarkup:
    buttons = []
    button_n = [InlineKeyboardButton(text="Имя", callback_data="name")]
    button_g = [InlineKeyboardButton(text="Уровень", callback_data="grade")]
    button_s = [InlineKeyboardButton(text="Сфера", callback_data="sphere")]
    button_b = [InlineKeyboardButton(text="Краткий рассказ", callback_data="bio")]
    if name != NoneData:
        button_n = [InlineKeyboardButton(text="Имя ✅", callback_data="name")]
    if grade != NoneData:
        button_g = [InlineKeyboardButton(text="Уровень ✅", callback_data="grade")]
    if sphere != NoneData:
        button_s = [InlineKeyboardButton(text="Сфера ✅", callback_data="sphere")]
    if bio != NoneData:
        button_b = [InlineKeyboardButton(text="Краткий рассказ ✅", callback_data="bio")]

    buttons.append(button_n)
    buttons.append(button_g)
    buttons.append(button_s)
    buttons.append(button_b)

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def registration_okay_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Имя ✅", callback_data="name")],
        [InlineKeyboardButton(text="Уровень ✅", callback_data="grade")],
        [InlineKeyboardButton(text="Сфера ✅", callback_data="sphere")],
        [InlineKeyboardButton(text="Краткий рассказ ✅", callback_data="bio")],
        [InlineKeyboardButton(text="Выйти", callback_data="info"),
         InlineKeyboardButton(text="Сохранить", callback_data="all_is_okay")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# NLP, CV,RecSys, Audio, Classic ML, любой
def choose_sphere_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="NLP", callback_data="NLP_sphere")],
        [InlineKeyboardButton(text="CV", callback_data="CV_sphere")],
        [InlineKeyboardButton(text="RecSys", callback_data="RecSys_sphere")],
        [InlineKeyboardButton(text="Audio", callback_data="Audio_sphere")],
        [InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_sphere")],
        [InlineKeyboardButton(text="Любой", callback_data="Any_sphere")],
        [InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# no_work, intern, junior, middle. senior
def choose_grade_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Без грейда", callback_data="no_work_grade")],
        [InlineKeyboardButton(text="Intern", callback_data="intern_grade")],
        [InlineKeyboardButton(text="Junior", callback_data="junior_grade")],
        [InlineKeyboardButton(text="Middle", callback_data="middle_grade")],
        [InlineKeyboardButton(text="Senior", callback_data="senior_grade")],
        [InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Регистрация", callback_data="registration")],
        [InlineKeyboardButton(text="Поиск", callback_data="cmd_go")],
        [InlineKeyboardButton(text="Видимость", callback_data="setting_student")],
        [InlineKeyboardButton(text="Список людей, которые хотят вас пособесить", callback_data="teacher_list")],
        [InlineKeyboardButton(text="Назад", callback_data="return_to_start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
