from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import os
from dotenv import load_dotenv, find_dotenv
from create_bot import bot
from database.sqlite_db import sql_add_command
from keyboards.client_kb import inline_kb, inline_faq_kb, inline_m_kb
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from to_json import read_from_file, read_price, arr_j

load_dotenv(find_dotenv())


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет, я бот для записи к высококлассному психологу Лене Кабаковой! 😎',
                           reply_markup=inline_kb)


async def bio(callback: types.CallbackQuery):
    await callback.message.answer(read_from_file())
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


async def prices(callback: types.CallbackQuery):
    await callback.message.answer(read_price())
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


# REQUEST MENU
async def show_menu(callback: types.CallbackQuery):
    await callback.message.answer('Меню', reply_markup=inline_kb)


""" Заявка на консультацию """

""" Входим в режим машины состояний """


class FSMClient(StatesGroup):
    name = State()
    phone = State()
    gmt = State()
    comment = State()


async def writing_on_consult(callback: types.CallbackQuery):
    await FSMClient.name.set()
    await callback.message.reply('Подача заявки состоит из четырех вопросов. '
                                 '\nЕсли вы передумали, то достаточно написать "Отмена"')
    await callback.message.reply('Шаг1. Напишите ваше имя')


""" CANCEL state """


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK. Ваша заявка отменена.')


""" Catch name and write in table """


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.next()
    await message.reply('Шаг2. Введите ваш номер телефона(Пример:8-912-345-67-89)')


""" Catch a phone number """


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_n'] = message.text
    await FSMClient.next()
    await message.reply('Шаг3. Укажите город в котором вы проживаете')


"""Catch a Timezone """


async def load_gmt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gmt'] = message.text
    await FSMClient.next()
    await message.reply('Шаг4. Напишите ваш запрос с которым вы хотите обратиться')


""" Catch a comment """


async def load_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    await sql_add_command(state)
    await state.finish()
    if await message.answer('Спасибо! Ваша заявка принята, Лена скоро с вами свяжется!'):
        await bot.send_message(chat_id=os.getenv('ID_NUM'),
                               text='You have a new query! Please check the database!')
        await message.delete()
    await message.answer('Вернуться в меню', reply_markup=inline_m_kb)


""" FAQ """


async def faq(callback: types.CallbackQuery):
    await callback.message.reply('Часто задаваемые вопросы', reply_markup=inline_faq_kb)


async def first_query(callback: types.CallbackQuery):
    await callback.message.answer(arr_j[0])
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


async def second_query(callback: types.CallbackQuery):
    await callback.message.answer(arr_j[1])
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


async def third_query(callback: types.CallbackQuery):
    await callback.message.answer(arr_j[2])
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


async def four_query(callback: types.CallbackQuery):
    await callback.message.answer(arr_j[3])
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


async def five_query(callback: types.CallbackQuery):
    await callback.message.answer(arr_j[4])
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


def register_handlers_client(dp: Dispatcher):
    """ Menu buttons handlers """
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(bio, Text(startswith='/bio'))
    dp.register_callback_query_handler(prices, Text(startswith='/price'))
    dp.register_callback_query_handler(show_menu, Text(startswith='/Menu'))

    ''' register handlers for creating values for writing in SQLite table '''
    dp.register_callback_query_handler(writing_on_consult, Text(startswith='/write'), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMClient.name)
    dp.register_message_handler(load_phone, state=FSMClient.phone)
    dp.register_message_handler(load_gmt, state=FSMClient.gmt)
    dp.register_message_handler(load_comment, state=FSMClient.comment)

    ''' FAQ reg_handlers '''
    dp.register_callback_query_handler(faq, Text(startswith='/faq'))
    dp.register_callback_query_handler(first_query, Text(startswith='/first_query'))
    dp.register_callback_query_handler(second_query, Text(startswith='/second_query'))
    dp.register_callback_query_handler(third_query, Text(startswith='/third_query'))
    dp.register_callback_query_handler(four_query, Text(startswith='/four_query'))
    dp.register_callback_query_handler(five_query, Text(startswith='/five_query'))
