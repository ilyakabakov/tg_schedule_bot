import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from create_bot import bot
from contextlib import suppress
from dotenv import load_dotenv, find_dotenv
from database.sqlite_db import sql_add_command, sql_add_command2, sql_read_events, sql_add_command_meeting
from keyboards.client_kb import inline_kb, inline_faq_kb, inline_m_kb, meeting_kb
from converter_from_json import array_json

load_dotenv(find_dotenv())


async def command_start(message: types.Message):
    try:
        if message.from_user.id >= 1:
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        await bot.send_message(
            message.from_user.id,
            array_json('hello'),
            reply_markup=inline_kb,
            parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(ex)


async def delete_message(message):
    """ Anti-flood func. This function for deleting previous message. """
    if inline_m_kb or inline_kb:
        await message.delete()


async def bio(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_message_with_parse_mode(
        callback.message,
        f"{array_json('bio')}\n\n"
        f"<b>Вернуться в меню:</b>",
        reply_markup=inline_m_kb)


async def prices(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_message_with_parse_mode(
        callback.message,
        f"{array_json('prices')}\n\n"
        f"<b>Вернуться в меню:</b>",
        reply_markup=inline_m_kb)


""" REQUEST MENU """


async def show_menu(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_message_with_parse_mode(
        callback.message,
        '<B>Меню</b>', reply_markup=inline_kb)


def sanitize_text(text: str) -> str:
    """ Remove invalid characters for the writing in db"""
    return text.replace("<", "").replace(">", "").replace("%", "")


async def send_message_with_parse_mode(message: types.Message, text: str, reply_markup=None, parse_mode=ParseMode.HTML):
    """ Send a message with specified text, reply markup and parse mode """

    await message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)


""" APPLY FOR A CONSULTATION PART. """
""" Uses FSM to write data in database. """


class FSMClient(StatesGroup):
    """ Start the StatesMachine"""

    name = State()
    phone = State()
    gmt = State()
    comment = State()


async def writing_on_consult(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await FSMClient.name.set()
    await send_message_with_parse_mode(
        callback.message,
        array_json('writing_on_consultation'))


async def cancel_handler(message: types.Message, state: FSMContext):
    """ CANCEL state. One Cancel state working for all state machines! """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(
        array_json('cancel_state'),
        reply_markup=inline_m_kb)


async def load_name(message: types.Message, state: FSMContext):
    """ Catch name and write in table """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)

    async with state.proxy() as data:
        data['name'] = sanitize_text(message.text)
    await FSMClient.next()
    await send_message_with_parse_mode(
        message,
        array_json('phone_number_query'))


async def load_phone(message: types.Message, state: FSMContext):
    """ Catch a phone number """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = sanitize_text(message.text)
    await FSMClient.next()
    await send_message_with_parse_mode(
        message,
        array_json('gmt_query'))


async def load_gmt(message: types.Message, state: FSMContext):
    """Catch a Timezone """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['gmt'] = sanitize_text(message.text)
    await FSMClient.next()
    await send_message_with_parse_mode(
        message,
        array_json('query_for_query'))


async def load_comment(message: types.Message, state: FSMContext):
    """ Catch a comment """
    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['comment'] = sanitize_text(message.text)
    await sql_add_command(state)
    await state.finish()
    if await send_message_with_parse_mode(
            message,
            array_json('thanks_answer'),
            reply_markup=inline_m_kb):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text=array_json('send_message_to_owner'))
        await message.delete()


""" FAQ PART """


async def faq(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_message_with_parse_mode(
        callback.message,
        array_json('faq_header1'),
        reply_markup=inline_faq_kb)


async def first_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_1'),
        array_json('faq_header2'))


async def second_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_2'),
        array_json('faq_header3'))


async def eight_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_9'),
        array_json('faq_header4'))


async def third_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_3'),
        array_json('faq_header5'))


async def four_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_4'),
        array_json('faq_header6'))


async def five_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_5'),
        array_json('faq_header7'))


async def six_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_6'),
        array_json('faq_header8'))


async def seven_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message,
        array_json('query_7'),
        array_json('faq_header9'))


async def send_faq_response(message, response_text, header_text):
    await message.answer(f'<b>{header_text}</b>\n\n'
                         f'{response_text}\n\n'
                         f'<b>Еще вопросы:</b>',
                         parse_mode=ParseMode.HTML,
                         reply_markup=inline_faq_kb)


""" SEND YOUR QUESTION PART """


class FormQuestion(StatesGroup):
    """ Start the State Machine """
    question = State()
    name = State()
    phone_n = State()


async def send_question(callback: types.CallbackQuery):
    """ Start the form by asking the user to enter their question """
    await delete_message(callback.message)

    await FormQuestion.question.set()

    await send_message_with_parse_mode(
        callback.message,
        array_json('send_question'))


async def load_question(message: types.Message, state: FSMContext):
    """ Load the user's question and move to the next state """

    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['question'] = sanitize_text(message.text)

    await FormQuestion.next()
    await send_message_with_parse_mode(
        message,
        array_json('name_query'))


async def load_name2(message: types.Message, state: FSMContext):
    """ Load the user's name and move to the next state """

    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['name'] = sanitize_text(message.text)

    await FormQuestion.next()
    await send_message_with_parse_mode(
        message,
        array_json('phone_number_query2'))


async def load_phone_number(message: types.Message, state: FSMContext):
    """ Load the user's phone number and finish the form """
    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = sanitize_text(message.text)
    await sql_add_command2(state)
    await state.finish()
    if await send_message_with_parse_mode(
            message,
            array_json('question_complete_answer'),
            reply_markup=inline_m_kb):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text=array_json('send_message_to_owner2'))
        await message.delete()


""" Thematic meeting part"""


async def meeting(callback: types.CallbackQuery):
    await delete_message(callback.message)

    read = await sql_read_events()
    for row in read:
        await send_message_with_parse_mode(
            callback.message,
            f'<b>Тематические встречи</b>\n\n'
            f'Ближайшая встреча:\n\n'
            f'Тема: \n<b>{row[1]}</b>\n\n'
            f'Место проведения: <b>{row[2]}</b>\n'
            f'Дата: <b>{row[3]}</b>\n'
            f'Начало: <b>{row[4]}</b>\n'
            f'Цена: <b>{row[5]}</b>\n',
            reply_markup=meeting_kb)


async def about_meeting(callback: types.CallbackQuery):
    await delete_message(callback.message)

    await send_meeting_response(
        callback.message,
        array_json('query_8'),
        array_json('about_meetings_header')
    )


async def send_meeting_response(message, response_text, header_text):
    await message.answer(f'<b>{header_text}</b>\n\n'
                         f'{response_text}\n\n'
                         f'<b>Вернуться:</b>',
                         parse_mode=ParseMode.HTML,
                         reply_markup=meeting_kb)


class FormMeeting(StatesGroup):
    full_name = State()
    phone_n = State()


async def write_on_meeting(callback: types.CallbackQuery):
    await delete_message(callback.message)

    await FormMeeting.full_name.set()
    await send_message_with_parse_mode(
        callback.message,
        array_json('write_on_meeting'))


async def catch_full_name(message: types.Message, state: FSMContext):
    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['full_name'] = sanitize_text(message.text)

    await FormMeeting.next()
    await send_message_with_parse_mode(
        message,
        array_json('phone_number_query2'))


async def catch_phone_number(message: types.Message, state: FSMContext):
    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = sanitize_text(message.text)
    await sql_add_command_meeting(state)
    await state.finish()
    await send_message_with_parse_mode(
        message,
        array_json('meeting_complete_answer'),
        reply_markup=inline_m_kb)


""" Register handlers part """


def register_handlers_client(dp: Dispatcher):
    """ Menu buttons handlers """

    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(bio, Text(startswith='/bio'))
    dp.register_callback_query_handler(prices, Text(startswith='/price'))
    dp.register_callback_query_handler(show_menu, Text(startswith='/Menu'))

    """ Register handlers for creating values for writing in SQLite table """

    dp.register_callback_query_handler(writing_on_consult, Text(startswith='/write'), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMClient.name)
    dp.register_message_handler(load_phone, state=FSMClient.phone)
    dp.register_message_handler(load_gmt, state=FSMClient.gmt)
    dp.register_message_handler(load_comment, state=FSMClient.comment)

    """ FAQ reg_handlers """

    dp.register_callback_query_handler(faq, Text(startswith='/faq'))
    dp.register_callback_query_handler(first_query, Text(startswith='/first_query'))
    dp.register_callback_query_handler(second_query, Text(startswith='/second_query'))
    dp.register_callback_query_handler(third_query, Text(startswith='/third_query'))
    dp.register_callback_query_handler(four_query, Text(startswith='/four_query'))
    dp.register_callback_query_handler(five_query, Text(startswith='/five_query'))
    dp.register_callback_query_handler(six_query, Text(startswith='/six_query'))
    dp.register_callback_query_handler(seven_query, Text(startswith='/seven_query'))
    dp.register_callback_query_handler(eight_query, Text(startswith='/eight_query'))

    '''FAQ send a question handlers'''

    dp.register_callback_query_handler(send_question, Text(startswith='/question'))
    dp.register_message_handler(load_question, state=FormQuestion.question)
    dp.register_message_handler(load_name2, state=FormQuestion.name)
    dp.register_message_handler(load_phone_number, state=FormQuestion.phone_n)

    """ Thematic meeting handlers """
    dp.register_callback_query_handler(meeting, Text(startswith='/meeting'))
    dp.register_callback_query_handler(about_meeting, Text(startswith='/about_meeting'))
    dp.register_callback_query_handler(write_on_meeting, Text(startswith='/thematic_write'), state=None)
    dp.register_message_handler(catch_full_name, state=FormMeeting.full_name)
    dp.register_message_handler(catch_phone_number, state=FormMeeting.phone_n)
