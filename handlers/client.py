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

from database.db_queries import new_client, new_question, new_meeting_client, get_events_data
from keyboards.client_kb import inline_kb, inline_faq_kb, inline_m_kb, meeting_kb, cancel_state_kb, \
    back_to_meeting_page_kb
from database.json_queries import array_json

load_dotenv(find_dotenv())


async def command_start(message: types.Message):
    """ Start bot handler """

    try:
        if message.from_user.id >= 1:
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        await bot.send_message(
            message.from_user.id,
            await array_json(user="client_content", query='hello'),
            reply_markup=inline_kb,
            parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(ex)


async def delete_message(message):
    """ Anti-flood func. This function for deleting previous message by bot. """

    if inline_m_kb or inline_kb:
        await message.delete()


async def bio(callback: types.CallbackQuery):
    """ Show about page """

    await edit_message_with_parse_mode(
        callback.message,
        f"{await array_json(user='client_content', query='bio')}\n\n"
        f"<b>Вернуться в меню:</b>",
        reply_markup=inline_m_kb)


async def prices(callback: types.CallbackQuery):
    """ Show prices page """

    await edit_message_with_parse_mode(
        callback.message,
        f"{await array_json(user='client_content', query='prices')}\n\n"
        f"<b>Вернуться в меню:</b>",
        reply_markup=inline_m_kb)


""" REQUEST MENU """


async def show_menu(callback: types.CallbackQuery):
    """ This page displayed
        when user tap a back to menu button """

    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user="client_content", query="hello"), reply_markup=inline_kb)


def sanitize_text(text: str) -> str:
    """ Remove invalid characters for the writing in db"""
    return text.replace("<", "").replace(">", "").replace("%", "")


async def edit_message_with_parse_mode(message: types.Message, text: str, reply_markup=None, parse_mode=ParseMode.HTML):
    """ Send a message with specified text, reply markup and parse mode """

    await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)


async def send_message_with_parse_mode(message: types.Message, text: str, reply_markup=None, parse_mode=ParseMode.HTML):
    """ Send a message with specified text, reply markup and parse mode """

    await message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)


""" APPLY FOR A CONSULTATION PART. """
""" Uses FSM to write data in database. """


class FSMClient(StatesGroup):
    """ Create FSM model """

    name = State()
    phone = State()
    gmt = State()
    comment = State()


async def writing_on_consult(callback: types.CallbackQuery):
    """ Start the State Machine """
    await FSMClient.name.set()
    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='writing_on_consultation'),
        reply_markup=cancel_state_kb)


async def cancel_state_handler(callback: types.CallbackQuery, state: FSMContext):
    """ CANCEL state. One cancel state handler working for all state machines! """

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text(
        await array_json(user='client_content', query='cancel_state'),
        reply_markup=inline_m_kb)


async def load_name(message: types.Message, state: FSMContext):
    """ Save name in state """

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
        await array_json(user='client_content', query='phone_number_query'),
        reply_markup=cancel_state_kb)


async def load_phone(message: types.Message, state: FSMContext):
    """ Save a phone number in state """

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
        await array_json(user='client_content', query='gmt_query'),
        reply_markup=cancel_state_kb)


async def load_gmt(message: types.Message, state: FSMContext):
    """Save a Timezone in state """

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
        await array_json(user='client_content', query='comment'),
        reply_markup=cancel_state_kb)


async def load_comment(message: types.Message, state: FSMContext):
    """ Save a comment and save all state in db.
        Finish current state """
    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['comment'] = sanitize_text(message.text)
    await new_client(state)
    await state.finish()
    if await send_message_with_parse_mode(
            message,
            await array_json(user='client_content', query='thanks_answer'),
            reply_markup=inline_m_kb):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text=await array_json(user='client_content', query='send_message_to_owner'))
        await message.delete()


""" FAQ PART """


async def faq(callback: types.CallbackQuery):
    """ FAQ main page """

    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='faq_header1'),
        reply_markup=inline_faq_kb)


async def first_query(callback: types.CallbackQuery):
    """ First response page """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_1'),
        await array_json(user='client_content', query='faq_header2'))


async def second_query(callback: types.CallbackQuery):
    """ Second response page """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_2'),
        await array_json(user='client_content', query='faq_header3'))


async def eight_query(callback: types.CallbackQuery):
    """ Eight response page.
        by display order """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_9'),
        await array_json(user='client_content', query='faq_header4'))


async def third_query(callback: types.CallbackQuery):
    """ Third response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_3'),
        await array_json(user='client_content', query='faq_header5'))


async def four_query(callback: types.CallbackQuery):
    """ Four response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_4'),
        await array_json(user='client_content', query='faq_header6'))


async def five_query(callback: types.CallbackQuery):
    """ Five response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_5'),
        await array_json(user='client_content', query='faq_header7'))


async def six_query(callback: types.CallbackQuery):
    """ Six response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_6'),
        await array_json(user='client_content', query='faq_header8'))


async def seven_query(callback: types.CallbackQuery):
    """ Seven response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_7'),
        await array_json(user='client_content', query='faq_header9'))


async def send_faq_response(message, response_text, header_text):
    """ This feature reduces
        the amount of repetitive code  """

    await message.edit_text(f'<b>{header_text}</b>\n\n'
                            f'{response_text}\n\n'
                            f'<b>Еще вопросы:</b>',
                            parse_mode=ParseMode.HTML,
                            reply_markup=inline_faq_kb)


""" SEND YOUR QUESTION PART """


class FormQuestion(StatesGroup):
    """ Create FSM model for Ask a Question """

    question = State()
    name = State()
    phone_n = State()


async def send_question(callback: types.CallbackQuery):
    """ Start the form by asking the user to enter their question """

    await FormQuestion.question.set()

    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='send_question'),
        reply_markup=cancel_state_kb)


async def load_question(message: types.Message, state: FSMContext):
    """ Save the user's question and move to the next state """

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
        await array_json(user='client_content', query='name_query'),
        reply_markup=cancel_state_kb)


async def load_name2(message: types.Message, state: FSMContext):
    """ Save the user's name and move to the next state """

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
        await array_json(user='client_content', query='phone_number_query2'),
        reply_markup=cancel_state_kb)


async def load_phone_number(message: types.Message, state: FSMContext):
    """ Saving last response in state
        and saving all state in db """

    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id,
                                 message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = sanitize_text(message.text)
    await new_question(state)
    await state.finish()
    if await send_message_with_parse_mode(
            message,
            await array_json(user='client_content', query='question_complete_answer'),
            reply_markup=inline_m_kb):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text=await array_json(user='client_content', query='send_message_to_owner2'))
        await message.delete()


""" THEMATIC MEETING PART """


async def meeting(callback: types.CallbackQuery):
    """ Events page """

    read = await get_events_data()
    for row in read:
        await edit_message_with_parse_mode(
            callback.message,
            f'<b>Мероприятия</b>\n\n'
            f'Ближайшая встреча:\n\n'
            f'Тема: \n<b>{row.naming}</b>\n\n'
            f'Место проведения: <b>{row.place}</b>\n'
            f'Дата: <b>{row.date}</b>\n'
            f'Начало: <b>{row.time}</b>\n'
            f'Цена: <b>{row.price} {await array_json(user="other_content", query="currency_gel")}</b>\n',
            reply_markup=meeting_kb)


async def about_meeting(callback: types.CallbackQuery):
    """ Page with info about events """

    await send_meeting_response(
        callback.message,
        await array_json(user='client_content', query='query_8'),
        await array_json(user='client_content', query='about_meetings_header'))


async def send_meeting_response(message, response_text, header_text):
    await message.edit_text(f'<b>{header_text}</b>\n\n'
                            f'{response_text}\n\n'
                            f'<b>Вернуться:</b>',
                            parse_mode=ParseMode.HTML,
                            reply_markup=back_to_meeting_page_kb)


class FormMeeting(StatesGroup):
    """ Create FSM model for Sign up to event """

    full_name = State()
    phone_n = State()


async def write_on_meeting(callback: types.CallbackQuery):
    """ Start State Machine """

    await FormMeeting.full_name.set()
    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='write_on_meeting'),
        reply_markup=cancel_state_kb)


async def catch_full_name(message: types.Message, state: FSMContext):
    """ Saving first response in state """

    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['full_name'] = sanitize_text(message.text)

    await FormMeeting.next()
    await send_message_with_parse_mode(message,
                                       await array_json(user='client_content',
                                                        query='phone_number_query2'),
                                       reply_markup=cancel_state_kb)


async def catch_phone_number(message: types.Message, state: FSMContext):
    """ Saving second response in state
        and saving all state in db """

    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = sanitize_text(message.text)
    await new_meeting_client(state)
    await state.finish()
    await send_message_with_parse_mode(message,
                                       await array_json(user='client_content',
                                                        query='meeting_complete_answer'),
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
    dp.register_callback_query_handler(cancel_state_handler, Text(startswith='/cancel'), state="*")
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
