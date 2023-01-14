from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.sqlite_db import sql_read_questions
from database import sqlite_db
from database.sqlite_db import delete_all_data
from keyboards import admin_kb

ID = None


async def director_test(message: types.Message):
    """ Check on admin """

    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Hello! What do you want?", reply_markup=admin_kb.button_case_a)
    await message.delete()


async def del_callback_run(callback_query: types.CallbackQuery):
    """ Delete one item in database """

    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} was deleted!', show_alert=True)


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_two()
        for ret in read:
            await bot.send_message(message.from_user.id,
                                   f'Client_id: {ret[0]}\n'
                                   f'Name: {ret[1]}\n'
                                   f'Phone_number: {ret[2]}\n'
                                   f'GMT: {ret[3]}\n'
                                   f'Query: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'DELETE: {ret[0]}, {ret[1]}',
                                                            callback_data=f'del {ret[0]}')))


async def del_callback_run_q(callback_query: types.CallbackQuery):
    """ Delete one item in database """

    await sqlite_db.sql_delete_command_q(callback_query.data.replace('dlt ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("dlt ", "")} was deleted!', show_alert=True)


async def delete_question(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_three()
        for ret in read:
            await bot.send_message(message.from_user.id,
                                   f'ID: {ret[0]}\n'
                                   f'Имя: {ret[2]}\n'
                                   f'Номер телефона: {ret[3]}\n'
                                   f'Вопрос: {ret[1]}\n')
            await bot.send_message(message.from_user.id, text='^^^',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'DELETE: {ret[0]}, {ret[1]}',
                                                            callback_data=f'dlt {ret[0]}')))


async def emergency_delete(message: types.Message):
    if message.from_user.id == ID:
        await delete_all_data()
        await bot.send_message(message.from_user.id, 'Database was successfully deleted!')


async def open_all(message: types.Message):
    if message.from_user.id == ID:
        await sqlite_db.sql_read(message)


async def open_questions_db(message: types.Message):
    if message.from_user.id == ID:
        await sql_read_questions(message)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(director_test, commands=['moderator'], is_chat_admin=True)

    dp.register_message_handler(delete_item, commands='Delete')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))

    dp.register_message_handler(delete_question, commands='Delete_question')
    dp.register_callback_query_handler(del_callback_run_q, lambda x: x.data and x.data.startswith('dlt '))

    dp.register_message_handler(emergency_delete, commands='Emergency_delete')

    dp.register_message_handler(open_all, commands='Open_db')
    dp.register_message_handler(open_questions_db, commands='Open_questions_db')
