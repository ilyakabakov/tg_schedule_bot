from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

"""Admin's keyboard """


def admin_keyboard() -> InlineKeyboardMarkup:
    buttons_list = [
        types.InlineKeyboardButton(text='👀 Все заявки на консультацию',
                                   callback_data='Open_db'),
        types.InlineKeyboardButton(text='👀 Последний запрос',
                                   callback_data='Open_last_client'),
        types.InlineKeyboardButton(text='❌ Удалить клиента',
                                   callback_data='Delete'),
        types.InlineKeyboardButton(text='👀 Открыть все вопросы',
                                   callback_data='Open_questions_db'),
        types.InlineKeyboardButton(text='❌ Удалить вопрос',
                                   callback_data='Clear_question'),
        types.InlineKeyboardButton(text='✍🏻 Изменить афишу',
                                   callback_data='Create_event'),
        types.InlineKeyboardButton(text='👀 Список участников встречи',
                                   callback_data='Show_list'),
        types.InlineKeyboardButton(text='❌ Удалить список участников встречи',
                                   callback_data='Delete_list'),
        types.InlineKeyboardButton(text='Вернуться в меню',
                                   callback_data='Menu')
    ]
    keyboard = InlineKeyboardBuilder()
    keyboard.add(*buttons_list)
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def back_to_admin_menu() -> InlineKeyboardMarkup:
    buttons_list = [
        types.InlineKeyboardButton(text="😎 Admin's menu",
                                   callback_data='admin_menu')
    ]
    keyboard = InlineKeyboardBuilder()
    keyboard.add(*buttons_list)
    keyboard.adjust(1)
    return keyboard.as_markup()
