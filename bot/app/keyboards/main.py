from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Создать опрос"), KeyboardButton(text="📚 Мои опросы")],
        [KeyboardButton(text="✅ Пройти опрос"), KeyboardButton(text="📊 Результаты")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="❌ Отмена")],
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
        [KeyboardButton(text="Один вариант"), KeyboardButton(text="Несколько вариантов")],
        [KeyboardButton(text="Шкала 1-5"), KeyboardButton(text="Свободный текст")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
