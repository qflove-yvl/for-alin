from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/create_poll"), KeyboardButton(text="/my_polls")],
        [KeyboardButton(text="/take_poll"), KeyboardButton(text="/results")],
        [KeyboardButton(text="/help")],
    ],
    resize_keyboard=True,
)
