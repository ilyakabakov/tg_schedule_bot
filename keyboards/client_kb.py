from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

""" Keyboard_menu_button """


def get_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text='Меню',
            callback_data='Menu'
        )
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


menu_bttn = types.InlineKeyboardButton(text='Меню', callback_data='Menu')

""" Keyboard FAQ part """


def get_faq_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    faq_bttns = [
        types.InlineKeyboardButton(
            text="Как понять, что\n мне нужно к психологу?",
            callback_data='first_query'
        ),
        types.InlineKeyboardButton(
            text='Как выбрать психолога?👍🏻',
            callback_data='second_query'
        ),
        types.InlineKeyboardButton(
            text='Что такое КПТ и ACT?',
            callback_data='eight_query'
        ),
        types.InlineKeyboardButton(
            text='С какими запросами я могу обратиться?',
            callback_data='third_query'
        ),
        types.InlineKeyboardButton(
            text='Как проходит терапия?',
            callback_data='four_query'
        ),
        types.InlineKeyboardButton(
            text='Как часто нужно встречаться?',
            callback_data='five_query'
        ),
        types.InlineKeyboardButton(
            text='Сколько нужно сессий,\n для результата?',
            callback_data='six_query'
        ),
        types.InlineKeyboardButton(
            text='Психолог и психиатр - в чем отличия?',
            callback_data='seven_query'
        ),
        types.InlineKeyboardButton(
            text='Задать свой вопрос',
            callback_data='question'
        )
    ]
    kb.add(*faq_bttns)
    kb.add(menu_bttn)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_back_to_faq_list_btn() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        types.InlineKeyboardButton(
            text='Назад к вопросам',
            callback_data='faq'
        )
    )
    kb.add(menu_bttn)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


""" Inline Main keyboard part """


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    bttns = [
        types.InlineKeyboardButton(
            text=' Часто задаваемые вопросы ⁉️',
            callback_data='faq'
        ),
        types.InlineKeyboardButton(
            text='О специалисте 👩 ',
            callback_data='bio'
        ),
        types.InlineKeyboardButton(
            text='Цены👇🏼',
            callback_data='price'
        ),
        types.InlineKeyboardButton(
            text='Оставить заявку на консультацию 👍',
            callback_data='write'
        ),
        types.InlineKeyboardButton(
            text='Мероприятия',
            callback_data='meeting'
        )
    ]
    kb.add(*bttns)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


""" Thematic meetings part """


def get_meetings_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    bttns = [
        types.InlineKeyboardButton(
            text='О наших мероприятиях',
            callback_data='about_meeting'),
        types.InlineKeyboardButton(
            text='Записаться на мероприятие',
            callback_data='thematic_write')
    ]
    kb.add(*bttns)
    kb.add(menu_bttn)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


""" Back to meetings part """


def get_back_to_meetings_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    bttns = [
        types.InlineKeyboardButton
        (text='Назад',
         callback_data='meeting')
    ]
    kb.add(*bttns)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


""" Other keyboards """


def cancel_state_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    bttns = [
        types.InlineKeyboardButton(
            text='отмена',
            callback_data='cancel')
    ]
    kb.add(*bttns)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
