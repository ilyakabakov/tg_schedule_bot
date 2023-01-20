from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Admin's keyboard """


admins_kb = InlineKeyboardMarkup(row_width=1)
b_open_db = InlineKeyboardButton(text='👀 Все заявки на консультацию', callback_data='/Open_db')
b_delete_db = InlineKeyboardButton(text='❌ Удалить клиента из БД', callback_data='/Delete')
b_open_questions_db = InlineKeyboardButton(text='👀 Открыть все вопросы', callback_data='/Open_questions_db')
b_delete_question = InlineKeyboardButton(text='❌ Удалить вопрос из БД', callback_data='/clear_question')
b_event1 = InlineKeyboardButton(text='✍🏻 Изменить афишу', callback_data='/create_event')
b_meeting_list = InlineKeyboardButton(text='👀 Список участников встречи', callback_data='/show_list')
b_meeting_list_del = InlineKeyboardButton(text='❌ Удалить список участников встречи', callback_data='/delete_list')
admins_kb.add(b_open_db, b_delete_db, b_open_questions_db, b_delete_question, b_event1, b_meeting_list, b_meeting_list_del)

admins_menu_kb = InlineKeyboardMarkup(row_width=1)
b_admn_menu = InlineKeyboardButton(text="😎 Admin's menu", callback_data='/admin_menu')
admins_menu_kb.add(b_admn_menu)
