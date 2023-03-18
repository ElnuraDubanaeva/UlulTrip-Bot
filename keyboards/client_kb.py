from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

submit_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("ДА"), KeyboardButton("НЕТ")
)

cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("CANCEL")
)
quantity_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=2
).add(
    KeyboardButton("1"),
    KeyboardButton("2"),
    KeyboardButton("3"),
    KeyboardButton("4"),
    KeyboardButton("5"),
    KeyboardButton("6"),
    KeyboardButton("7"),
    KeyboardButton("8"),
    KeyboardButton("9"),
    KeyboardButton("10"),
)
