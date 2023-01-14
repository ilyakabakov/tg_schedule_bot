from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

""" Keyboard_menu_button """
inline_m_kb = InlineKeyboardMarkup(row_width=1)
menu_bttn = InlineKeyboardButton('Меню', callback_data='/Menu')
inline_m_kb.add(menu_bttn)

""" Keyboard FAQ part """
inline_faq_kb = InlineKeyboardMarkup(row_width=1)
faq_b1 = InlineKeyboardButton(text="Как понять, что\n мне нужно к психологу?", callback_data='/first_query')
faq_bttns = [InlineKeyboardButton(text='Как выбрать психолога?👍🏻', callback_data='/second_query'),
             InlineKeyboardButton(text='С какими запросами я могу обратиться?', callback_data='/third_query'),
             InlineKeyboardButton(text='Как проходит сессия?', callback_data='/four_query'),
             InlineKeyboardButton(text='Как часто нужно встречаться?', callback_data='/five_query'),
             InlineKeyboardButton(text='Сколько нужно сессий,\n для результата?', callback_data='/six_query'),
             InlineKeyboardButton(text='Психолог и психиатр - в чем отличия?', callback_data='/seven_query'),
             InlineKeyboardButton(text='Задать свой вопрос', callback_data='/question')
             ]
inline_faq_kb.add(faq_b1).add(*faq_bttns).add(menu_bttn)

""" Inline keyboard part """
inline_kb = InlineKeyboardMarkup(row_width=1)
b1 = InlineKeyboardButton(text=' Часто задаваемые вопросы ⁉️', callback_data='/faq')
b2 = InlineKeyboardButton(text='О специалисте 👩 ', callback_data='/bio')
b3 = InlineKeyboardButton(text='Цены👇🏼', callback_data='/price')
b4 = InlineKeyboardButton(text='Оставить заявку на консультацию 👍', callback_data='/write')

inline_kb.add(b1)
inline_kb.add(b2).add(b3, b4)
