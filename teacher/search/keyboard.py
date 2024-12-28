from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def return_go_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="new_students_teacher")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def search_or_filters_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Искать", callback_data="search_students")],
        [InlineKeyboardButton(text="Фильтры", callback_data="filters_students")],
        [InlineKeyboardButton(text="Назад", callback_data="start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def searching_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data="agree_teacher"),
         InlineKeyboardButton(text="Вперед", callback_data="next_student")
         ],
        [InlineKeyboardButton(text="Назад", callback_data="new_students_teacher")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def fsearching_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data="agreef_teacher"),
         InlineKeyboardButton(text="Вперед", callback_data="fnext_student")],
        [InlineKeyboardButton(text="Назад", callback_data="filters_teacher")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cmd_filters_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Выбрать уровень", callback_data="gradef_teacher")],
        [InlineKeyboardButton(text="Выбрать сферу", callback_data="spheref_teacher")],
        [InlineKeyboardButton(text="Применить и перейти", callback_data="fsearch_teacher")],
        [InlineKeyboardButton(text="Назад", callback_data="new_students_teacher")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def fchoose_sphere_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="NLP", callback_data="NLP_spheref_teacher")],
        [InlineKeyboardButton(text="CV", callback_data="CV_spheref_teacher")],
        [InlineKeyboardButton(text="RecSys", callback_data="RecSys_spheref_teacher")],
        [InlineKeyboardButton(text="Audio", callback_data="Audio_spheref_teacher")],
        [InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_spheref_teacher")],
        [InlineKeyboardButton(text="Любой", callback_data="Any_spheref_teacher")],
        [InlineKeyboardButton(text="Назад", callback_data="returnf_teacher")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# no_work, intern, junior, middle. senior
def fchoose_grade_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Без грейда", callback_data="No_work_gradef_teacher")],
        [InlineKeyboardButton(text="Intern", callback_data="Intern_gradef_teacher")],
        [InlineKeyboardButton(text="Junior", callback_data="Junior_gradef_teacher")],
        [InlineKeyboardButton(text="Middle", callback_data="Middle_gradef_teacher")],
        [InlineKeyboardButton(text="Senior", callback_data="Senior_gradef_teacher")],
        [InlineKeyboardButton(text="Назад", callback_data="returnf_teacher")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
