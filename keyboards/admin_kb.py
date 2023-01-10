from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

"""Admin's buttons"""

button_open_db = KeyboardButton('/Open_db')
button_delete = KeyboardButton('/Delete')
button_open_one = KeyboardButton('/Open_one')

button_case_a = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_open_db)\
    .add(button_delete).add(button_open_one)
