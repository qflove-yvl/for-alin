from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/create_poll"), KeyboardButton(text="/my_polls")],
        [KeyboardButton(text="/take_poll"), KeyboardButton(text="/results")],
        [KeyboardButton(text="/help")],
    ],
    resize_keyboard=True,
)

yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

question_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="single_choice"), KeyboardButton(text="multi_choice")],
        [KeyboardButton(text="scale_1_5"), KeyboardButton(text="open_text")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
