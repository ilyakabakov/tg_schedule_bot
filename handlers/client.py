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
            '<b>Приветствую! ✨\nЯ Бот для записи к КПТ и АСТ психологу '
            'Лене Кабаковой 🤩\n\n</b>'
            'Здесь вы можете немного познакомиться с Леной, '
            'как специалистом, задать вопрос или записаться на сессию.\n\n'
            '🔸 Прямо сейчас\nЛена ведет прием только онлайн\n\n'
            'Но если вы из Батуми, не пропустите крутые и полезные'
            ' тематические встречи: <b>@point_of_support</b> 😎',
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
        f'{array_json[9]}\n\n'
        f'<b>Вернуться в меню:</b>',
        reply_markup=inline_m_kb)


async def prices(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_message_with_parse_mode(
        callback.message,
        f'{array_json[10]}\n\n'
        f'<b>Вернуться в меню:</b>',
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


""" Apply for a consultation """


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
        'Чтобы оставить заявку, ответьте, пожалуйста, на 4 вопроса.'
        '\n⚠️ Если передумали, достаточно написать: <b>отмена</b>\n\n'
        'Шаг 1.\n'
        'Давайте немного познакомимся!☺️\n'
        '<b>Как Вас зовут?</b>')


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
        'OK. Ваша заявка отменена. 👍🏻',
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
    await message.answer(
        'Шаг 2.\nВведите Ваш номер телефона')


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
    await message.answer(
        'Шаг3.\nНапишите город, в котором вы проживаете.'
        ' Или укажите часовой пояс.')


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
    await message.answer(
        'Шаг4.\nМожете коротко описать ваш запрос,\n'
        ' с которым хотите обратиться.')


async def load_comment(message: types.Message, state: FSMContext):
    """ Catch a comment """

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
            f'Спасибо! Ваша заявка принята.\n'
            ' Лена скоро с вами свяжется!😊\n\n'
            '<b>Вернуться в меню:</b>',
            reply_markup=inline_m_kb):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text='You have a new query! 😊 '
                 'Please check the database!')
        await message.delete()


""" FAQ part """


async def faq(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_message_with_parse_mode(
        callback.message,
        '<b>🔶 Часто задаваемые вопросы</b>',
        reply_markup=inline_faq_kb)


async def first_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[0],
        '🔶 Как понять, что мне нужно к психологу?')


async def second_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[1],
        '🔶 Как выбрать психолога?👍🏻')


async def eight_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[8],
        '🔶 Что такое КПТ и ACT?')


async def third_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[2],
        '🔶 С какими запросами я могу обратиться?')


async def four_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[3],
        '🔶 Как проходит терапия?')


async def five_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[4],
        '🔶 Как часто нужно встречаться?')


async def six_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[5],
        '🔶 Сколько нужно сессий, для результата?')


async def seven_query(callback: types.CallbackQuery):
    await delete_message(callback.message)
    await send_faq_response(
        callback.message, array_json[6],
        '🔶 Психолог, психотерапевт и психиатр - в чем отличия?')


async def send_faq_response(message, response_text, header_text):
    await message.answer(f'<b>{header_text}</b>\n\n'
                         f'{response_text}\n\n'
                         f'<b>Еще вопросы:</b>',
                         parse_mode=ParseMode.HTML,
                         reply_markup=inline_faq_kb)


"""Send Your Question part"""


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
        '🔶 Напишите свой вопрос\n'
        ' и Лена ответит вам в ближайшее время.\n\n'
        '⚠️ Или напишите: <b>отмена</b>')


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
    await message.answer('Напишите свое имя:')


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
    await message.answer('Укажите ваш номер телефона:')


async def load_phone_number(message: types.Message, state: FSMContext):
    """ Load the user's phone number and finish the form """
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
            'Спасибо!\n Ваш вопрос принят.\n'
            ' Лена скоро с вами свяжется!😊\n\n'
            '<b>Вернуться в меню</b>',
            reply_markup=inline_m_kb):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text='Вам задали вопрос! 😊 '
                 'Please check the database with Questions!')
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

    await send_message_with_parse_mode(
        callback.message,
        f'<b>🔶 Что такое тематические встречи с психологом?</b>\n\n'
        f'{array_json[7]}\n\n'
        f'<b>Вернуться:</b>',
        reply_markup=meeting_kb)


class FormMeeting(StatesGroup):
    full_name = State()
    phone_n = State()


async def write_on_meeting(callback: types.CallbackQuery):
    await delete_message(callback.message)

    await FormMeeting.full_name.set()
    await send_message_with_parse_mode(
        callback.message,
        'Записываююю✍🏻 \n<b>Напишите ваши имя и фамилию.</b>\n\n'
        '⚠️ Если вы передумали, отправьте сообщение c текстом: '
        '<b>отмена</b>')


async def catch_full_name(message: types.Message, state: FSMContext):
    await delete_message(message)
    if message.from_user.id >= 1:
        await bot.delete_message(
            message.chat.id,
            message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['full_name'] = sanitize_text(message.text)

    await FormMeeting.next()
    await message.answer('Укажите номер телефона, для связи:')


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
        f'<b>Вы успешно зарегистрированы на мероприятие!</b>🤩\n\n'
        f'Мы пришлём напоминание на указанный вами номер,\n\n'
        f' за день до начала мероприятия',
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
