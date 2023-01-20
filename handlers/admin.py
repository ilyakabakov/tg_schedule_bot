from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from database.sqlite_db import sql_read_questions, sql_add_command_events, sql_read_meeting
from database import sqlite_db
from database.sqlite_db import delete_all_data
from keyboards import admin_kb
from keyboards.admin_kb import admins_kb, admins_menu_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.client_kb import inline_m_kb, meeting_kb

ID = None


async def director_test(message: types.Message):
    """ Check on admin """

    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Hello!😎 What do you want?", reply_markup=admin_kb.admins_kb)
    await message.delete()


"""CLIENT DB PART"""


async def del_callback_run(callback_query: types.CallbackQuery):
    """ Delete one item in clients database """
    if callback_query.from_user.id == ID:
        await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
        await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} was deleted!', show_alert=True)


async def delete_item(callback: types.CallbackQuery):
    """ Get choice for deleting from clients db"""

    if callback.from_user.id == ID:
        if admins_menu_kb or admins_kb:
            await callback.message.delete()
        try:
            read = await sqlite_db.sql_read_two()
            for ret in read:
                await callback.message.answer(
                    f'Client_id: {ret[0]}\n'
                    f'Name: {ret[1]}\n'
                    f'Phone_number: {ret[2]}\n'
                    f'GMT: {ret[3]}\n'
                    f'Query: {ret[-1]}', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton(f'DELETE: {ret[0]}, {ret[1]}',
                                             callback_data=f'del {ret[0]}'),
                        InlineKeyboardButton(text='Вернуться в меню',
                                             callback_data='/admin_menu')))
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


async def admns_menu(callback: types.CallbackQuery):
    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        await callback.message.answer("Admins menu", reply_markup=admin_kb.admins_kb)


async def open_all(callback: types.CallbackQuery):
    """ Open clients db """

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        try:
            await sqlite_db.sql_read(callback)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


""" QUESTIONS DB PART """


async def del_callback_run_q(callback_query: types.CallbackQuery):
    """ Delete one item from questions database """
    if callback_query.from_user.id == ID:
        await sqlite_db.sql_delete_command_q(callback_query.data.replace('dlt ', ''))
        await callback_query.answer(text=f'{callback_query.data.replace("dlt ", "")} was deleted!', show_alert=True)


async def delete_question(callback: types.CallbackQuery):
    """ Get choice for deleting from questions db"""

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        try:
            read = await sqlite_db.sql_read_three()
            for ret in read:
                await callback.message.answer(
                    f'ID: {ret[0]}\n'
                    f'Имя: {ret[2]}\n'
                    f'Номер телефона: {ret[3]}\n'
                    f'Вопрос: {ret[1]}\n', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton(f'DELETE: {ret[0]}, {ret[1]}',
                                             callback_data=f'dlt {ret[0]}'),
                        InlineKeyboardButton(text='Вернуться в меню',
                                             callback_data='/admin_menu')))
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


async def open_questions_db(callback: types.CallbackQuery):
    """ Open questions db """

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        try:
            await sql_read_questions(callback)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


""" CREATE EVENT ON EVENT DB """


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
        await callback.message.answer("Укажите название мероприятия:")


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
        await message.answer('Укажите место проведения:')


async def catch_place(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['place'] = message.text
        await FormEvent.next()
        await message.answer('Укажите дату проведения:')


async def catch_date(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['date'] = message.text
        await FormEvent.next()
        await message.answer('Укажите время начала:')


async def catch_time(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['time'] = message.text
        await FormEvent.next()
        await message.answer('Укажите цену:')


async def catch_price(message: types.Message, state: FSMContext):
    await message.delete()
    if message.from_user.id == ID:
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        async with state.proxy() as data:
            data['price'] = message.text
        await sql_add_command_events(state)
        await state.finish()
        await message.answer(f'Мероприятие зарегистрировано!', reply_markup=inline_m_kb)


"""EVENT CLIENTS DB"""


async def del_callback_run_meet(callback_query: types.CallbackQuery):
    """ Delete one item from meeting database """
    if callback_query.from_user.id == ID:
        await sqlite_db.sql_delete_command_meet(callback_query.data.replace('clr ', ''))
        await callback_query.answer(text=f'{callback_query.data.replace("clr ", "")} was deleted!', show_alert=True)


async def delete_meeting_clients(callback: types.CallbackQuery):
    """ Get choice for deleting from meetings db"""

    if callback.from_user.id == ID:
        if callback.from_user.id >= 1:
            await callback.message.delete()
        read = await sqlite_db.sql_read_meeting()
        for ret in read:
            await callback.message.answer(
                f'ID: {ret[0]}\n'
                f'Имя и Фамилия: {ret[1]}\n'
                f'Номер телефона: {ret[2]}\n',
                reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton(f'DELETE: {ret[0]}, {ret[1]}',
                                         callback_data=f'clr {ret[0]}'),
                    InlineKeyboardButton(text='Вернуться в меню',
                                         callback_data='/admin_menu')))


async def meeting(callback: types.CallbackQuery):
    if callback.from_user.id == ID:
        if admins_kb:
            await callback.message.delete()
        try:
            read = await sql_read_meeting()
            for row in read:
                await callback.message.answer(f'ID: <b>{row[0]}</b>\n\n'
                                              f'Full name: <b>{row[1]}</b>\n'
                                              f'номер телефона: <b>{row[2]}</b>\n',
                                              reply_markup=admins_menu_kb, parse_mode=ParseMode.HTML)
        except Exception as ex:
            print(f'Invalid answer from DB: {ex}')


async def emergency_delete(message: types.Message):
    """Drop tables"""
    if message.from_user.id == ID:
        await delete_all_data()
        await bot.send_message(message.from_user.id, 'Database was successfully deleted!')


def register_handlers_admin(dp: Dispatcher):
    """Starting page handlers """
    dp.register_message_handler(director_test, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(admns_menu, Text(startswith='/admin_menu'))

    """ Client db handlers """

    dp.register_callback_query_handler(delete_item, Text(equals='/Delete'))
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(open_all, Text(equals='/Open_db'))

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

    """ Other handlers"""
    dp.register_message_handler(emergency_delete, commands='Emergency_delete')
