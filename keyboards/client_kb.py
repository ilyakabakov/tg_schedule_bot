from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


""" Keyboard_menu_button """
inline_m_kb = InlineKeyboardMarkup(row_width=1)
menu_bttn = InlineKeyboardButton('Меню', callback_data='/Menu')
inline_m_kb.add(menu_bttn)

""" Keyboard FAQ part """
inline_faq_kb = InlineKeyboardMarkup(row_width=1)
faq_b1 = InlineKeyboardButton(text="Почему обращаться к психологу необходимо?", callback_data='/first_query')
faq_bttns = [InlineKeyboardButton(text='Что делать если у меня депрессия?', callback_data='/second_query'),
             InlineKeyboardButton(text='Как распознать депрессию?', callback_data='/third_query'),
             InlineKeyboardButton(text='Как бороться с тревогой?', callback_data='/four_query'),
             InlineKeyboardButton(text='Что такое психологическая травма?', callback_data='/five_query')]
inline_faq_kb.add(faq_b1).add(*faq_bttns)

""" Inline keyboard part """
inline_kb = InlineKeyboardMarkup(row_width=1)
b1 = InlineKeyboardButton(text=' Часто задаваемые вопросы ⁉️', callback_data='/faq')
b2 = InlineKeyboardButton(text='О специалисте 👩 ', callback_data='/bio')
b3 = InlineKeyboardButton(text='Услуги👇🏼', callback_data='/price')
b4 = InlineKeyboardButton(text='Оставить заявку на консультацию 👍', callback_data='/write')

inline_kb.add(b1)
inline_kb.add(b2).add(b3, b4)
