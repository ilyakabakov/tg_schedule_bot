from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from database.db_queries import new_meeting, get_clients_data, get_event_clients_data, delete_meeting_client_data, \
    get_questions_data, delete_question_data, delete_client_data, get_client_data
from database.json_queries import array_json

from keyboards import admin_kb
from keyboards.admin_kb import admins_kb, admins_menu_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.client_kb import inline_m_kb, meeting_kb, cancel_state_kb

ID = None


async def director_test(message: types.Message):
    """ Check on admin """

    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, await array_json(user="admin_content", query="hello_page"), reply_markup=admin_kb.admins_kb)
    await message.delete()


"""CLIENT DB PART"""


async def del_callback_run(callback_query: types.CallbackQuery):
    """ Delete one item in clients database """
    if callback_query.from_user.id == ID:
        await delete_client_data(callback_query.data.replace('del ', ''))
        # await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} was deleted!', show_alert=True)
        await callback_query.message.edit_text(text=f'ID: {callback_query.data.replace("del ", "")} был удален!',
                                               reply_markup=admins_menu_kb)


async def delete_item(callback: types.CallbackQuery):
    """ Get choice for deleting from clients db"""

    if callback.from_user.id == ID:
        if admins_menu_kb or admins_kb:
            await callback.message.delete()
        try:
            arr = await get_clients_data()
            for row in arr:
                await callback.message.answer(
                    f'Client_id: {row.client_id}\n'
                    f'Name: {row.name}\n'
                    f'Phone_number: {row.phone_number}\n'
                    f'GMT: {row.gmt}\n'
                    f'Query: {row.comment}', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton(f'УДАЛИТЬ: {row.name}',
                                             callback_data=f'del {row.client_id}'),
                        InlineKeyboardButton(text='Вернуться в меню',
                                             callback_data='/admin_menu')))
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


async def admns_menu(callback: types.CallbackQuery):
    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        await callback.message.answer(await array_json(user="admin_content", query="admins_menu"),
                                      reply_markup=admin_kb.admins_kb)


async def open_all(callback: types.CallbackQuery):
    """ Open clients table """

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        try:
            arr = await get_clients_data()
            for row in arr:
                await callback.message.answer(f"ID: {row.client_id}\n"
                                              f"Имя: {row.name}\n"
                                              f"Номер телефона: {row.phone_number}\n"
                                              f"Город/Часовой пояс:{row.gmt}\n"
                                              f"Запрос: {row.comment}")
            await callback.message.answer("Clients", reply_markup=admins_menu_kb)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


async def open_last_client(callback: types.CallbackQuery):
    """ Open last client from clients table"""
    if callback.from_user.id == ID:
        try:
            arr = await get_client_data()
            await callback.message.answer(f"ID: {arr.client_id}\n"
                                          f"Имя: {arr.name}\n"
                                          f"Номер телефона: {arr.phone_number}\n"
                                          f"Город/Часовой пояс:{arr.gmt}\n"
                                          f"Запрос: {arr.comment}\n"
                                          f"МЕНЮ:", reply_markup=admins_menu_kb)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


""" QUESTIONS DB PART """

"""DELETE FROM questions HANDLERS """


async def del_callback_run_q(callback_query: types.CallbackQuery):
    """ Delete one item from questions database """
    if callback_query.from_user.id == ID:
        await delete_question_data(callback_query.data.replace('dlt ', ''))
        # await callback_query.answer(text=f'{callback_query.data.replace("dlt ", "")} was deleted!', show_alert=True)
        await callback_query.message.edit_text(text=f'ID: {callback_query.data.replace("dlt ", "")} был удален!',
                                               reply_markup=admins_menu_kb)


async def delete_question(callback: types.CallbackQuery):
    """ Get choice for deleting from questions db"""

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        try:
            arr = await get_questions_data()
            for row in arr:
                await callback.message.answer(
                    f'ID: {row.question_id}\n'
                    f'Имя: {row.name}\n'
                    f'Номер телефона: {row.phone_number}\n'
                    f'Вопрос: {row.question}\n',
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton(f'УДАЛИТЬ: {row.name}',
                                             callback_data=f'dlt {row.question_id}'),
                        InlineKeyboardButton(text='Вернуться в меню',
                                             callback_data='/admin_menu')))
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


""" GET FROM questions HANDLERS"""


async def open_questions_db(callback: types.CallbackQuery):
    """ Get all questions from questions table """

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        try:
            arr = await get_questions_data()
            for row in arr:
                await callback.message.answer(f"ID: {row.question_id}\n"
                                              f"Вопрос: <b>{row.question}</b>\n"
                                              f"Имя: <b>{row.name}</b>\n"
                                              f"Номер телефона:\n "
                                              f"<b>{row.phone_number}</b>",
                                              parse_mode=ParseMode.HTML)
            await callback.message.answer("Questions", reply_markup=admins_menu_kb)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


""" CREATE EVENT ON events TABLE """


class FormEvent(StatesGroup):
    """ Start the States Machine """

    naming = State()
    place = State()
    date = State()
    time = State()
    price = State()


async def create_event(callback: types.CallbackQuery):
    if callback.from_user.id == ID:
        if admins_kb or meeting_kb:
            await callback.message.delete()
        await FormEvent.naming.set()
        await callback.message.answer(await array_json(user='admin_content', query="meeting_naming"), reply_markup=cancel_state_kb)


async def event_cancel_handler(message: types.Message, state: FSMContext):
    """ CANCEL state """
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('👍🏻 Отменено.', reply_markup=admins_menu_kb)


async def catch_naming(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['naming'] = message.text

        await FormEvent.next()
        await message.answer(await array_json(user='admin_content', query="meeting_place"), reply_markup=cancel_state_kb)


async def catch_place(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['place'] = message.text
        await FormEvent.next()
        await message.answer(await array_json(user='admin_content', query="meeting_date"), reply_markup=cancel_state_kb)


async def catch_date(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['date'] = message.text
        await FormEvent.next()
        await message.answer(await array_json(user='admin_content', query="meeting_time"), reply_markup=cancel_state_kb)


async def catch_time(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['time'] = message.text
        await FormEvent.next()
        await message.answer(f"{await array_json(user='admin_content', query='meeting_price')}\n"
                             f"{await array_json(user='other_content', query='currency_gel')}", reply_markup=cancel_state_kb)


async def catch_price(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['price'] = message.text
        await new_meeting(state)
        await state.finish()
        await message.answer(await array_json(user='admin_content', query="meeting_complete"), reply_markup=inline_m_kb)


"""EVENT CLIENTS DB"""


async def del_callback_run_meet(callback_query: types.CallbackQuery):
    """ Delete one item from meeting database """
    if callback_query.from_user.id == ID:
        await delete_meeting_client_data(callback_query.data.replace('clr ', ''))
        # await callback_query.answer(text=f'{callback_query.data.replace("clr ", "")} was deleted!', show_alert=True)
        await callback_query.message.edit_text(text=f'{callback_query.data.replace("clr ", "")} was deleted!',
                                               reply_markup=admins_menu_kb)


async def delete_meeting_clients(callback: types.CallbackQuery):
    """ Get choice for deleting from meetings db"""

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        read = await get_event_clients_data()
        for row in read:
            await callback.message.answer(
                f'ID: {row.client_id}\n'
                f'Имя и Фамилия: {row.full_name}\n'
                f'Номер телефона: {row.phone_number}\n',
                reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton(f'УДАЛИТЬ: {row.full_name}',
                                         callback_data=f'clr {row.client_id}'),
                    InlineKeyboardButton(text='Вернуться в меню',
                                         callback_data='/admin_menu')))


async def meeting(callback: types.CallbackQuery):
    if callback.from_user.id == ID:
        if admins_kb:
            await callback.message.delete()
        try:
            read = await get_event_clients_data()
            for row in read:
                await callback.message.answer(f'ID: <b>{row.client_id}</b>\n\n'
                                              f'Full name: <b>{row.full_name}</b>\n'
                                              f'номер телефона: <b>{row.phone_number}</b>\n',
                                              reply_markup=admins_menu_kb, parse_mode=ParseMode.HTML)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


def register_handlers_admin(dp: Dispatcher):
    """Starting page handlers """
    dp.register_message_handler(director_test, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(admns_menu, Text(startswith='/admin_menu'))

    """ Client db handlers """

    dp.register_callback_query_handler(delete_item, Text(equals='/Delete'))
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(open_all, Text(equals='/Open_db'))
    dp.register_callback_query_handler(open_last_client, Text(equals='/Open_last_client'))

    """ Questions db handlers """

    dp.register_callback_query_handler(delete_question, Text(startswith='/clear_question'))
    dp.register_callback_query_handler(del_callback_run_q, lambda x: x.data and x.data.startswith('dlt '))
    dp.register_callback_query_handler(open_questions_db, Text(startswith='/Open_questions_db'))

    """ Create event handlers """

    dp.register_callback_query_handler(create_event, Text(startswith="/create_event"), state=None)
    dp.register_message_handler(event_cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(catch_naming, state=FormEvent.naming)
    dp.register_message_handler(catch_place, state=FormEvent.place)
    dp.register_message_handler(catch_date, state=FormEvent.date)
    dp.register_message_handler(catch_time, state=FormEvent.time)
    dp.register_message_handler(catch_price, state=FormEvent.price)
    """ Meetings db handlers """

    dp.register_callback_query_handler(delete_meeting_clients, Text(startswith='/delete_list'))
    dp.register_callback_query_handler(del_callback_run_meet, lambda x: x.data and x.data.startswith('clr '))
    dp.register_callback_query_handler(meeting, Text(equals='/show_list'))
