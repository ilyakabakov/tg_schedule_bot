from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.sqlite_db import sql_read_only_one
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
                                   f'Client_id: {ret[0]}\nName: {ret[1]}\nPhone_number: {ret[2]}\nGMT: {ret[3]}\nQuery: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(
                InlineKeyboardButton(f'DELETE: {ret[0]}, {ret[1]}', callback_data=f'del {ret[0]}')))


async def emergency_delete(message: types.Message):
    if message.from_user.id == ID:
        await delete_all_data()
        await bot.send_message(message.from_user.id, 'Database was successfully deleted!')


async def open_all(message: types.Message):
    if message.from_user.id == ID:
        await sqlite_db.sql_read(message)


class FSMAdmin(StatesGroup):
    """ Входим в режим машины состояний """
    client_id = State()


# Doesn't work now
@dp.message_handler(commands='Open_one')
async def open_one(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.client_id.set()
        await message.reply(
            'Text me client_ID')  # TODO: catch answer and send for db, and return answer of query from db
        await FSMAdmin.next()


async def open_client(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['client_id'] = message.text
        await sql_read_only_one(state)
        await state.finish()
        for ret in sqlite_db.res:
            await bot.send_message(message.from_user.id,
                                   f'ID: {ret[0]}\nName: {ret[1]}\nPhone number: {ret[2]}\nTimezone: {ret[3]}\nComment: {ret[-1]}')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(director_test, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands='Delete')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(emergency_delete, commands='Emergency_delete')
    dp.register_message_handler(open_all, commands='Open_db')
    # dp.register_callback_query_handler(open_one, Text(startswith='/Open_one'), state=None)
    # dp.register_message_handler(open_one, commands='Open_one')
    dp.register_message_handler(open_client, content_types=['client_id'], state=FSMAdmin.client_id)
