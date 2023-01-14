from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import os
from dotenv import load_dotenv, find_dotenv
from create_bot import bot
from database.sqlite_db import sql_add_command, sql_add_command2
from keyboards.client_kb import inline_kb, inline_faq_kb, inline_m_kb
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from to_json import read_from_file, read_price, arr_j

load_dotenv(find_dotenv())


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '<b>Приветствую! ✨\nЯ Бот для записи к КПТ и АСТ психологу '
                           'Лене Кабаковой 🤩\n\n</b>'
                           'Здесь вы можете немного познакомиться с Леной, '
                           'как специалистом, задать вопрос или записаться на сессию.\n\n'
                           '🔸 Прямо сейчас\nЛена ведет прием только онлайн\n\n'
                           'Но если вы из Батуми, не пропустите крутые и очень полезные'
                           ' очные встречи: <b>@point_of_support</b> 😎',
                           reply_markup=inline_kb,
                           parse_mode=ParseMode.HTML)


async def bio(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'{read_from_file()}\n\n'
                                  f'<b>Вернуться в меню</b>',
                                  reply_markup=inline_m_kb,
                                  parse_mode=ParseMode.HTML)


async def prices(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'{read_price()}\n\n'
                                  f'<b>Вернуться в меню</b>',
                                  reply_markup=inline_m_kb,
                                  parse_mode=ParseMode.HTML)


# REQUEST MENU
async def show_menu(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer('<B>Меню</b>', reply_markup=inline_kb,
                                  parse_mode=ParseMode.HTML)


""" Заявка на консультацию """


class FSMClient(StatesGroup):
    """ Start the StatesMachine"""

    name = State()
    phone = State()
    gmt = State()
    comment = State()


async def writing_on_consult(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await FSMClient.name.set()
    await callback.message.answer('Чтобы оставить заявку, ответьте, пожалуйста, на 4 вопроса.'
                                  '\n⚠️ Если передумали, достаточно написать: отмена\n\n'
                                  'Шаг 1.\n'
                                  'Давайте немного познакомимся!☺️\n'
                                  'Как Вас зовут?')


async def cancel_handler(message: types.Message, state: FSMContext):
    """ CANCEL state """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('OK. Ваша заявка отменена. 👍🏻', reply_markup=inline_m_kb)


async def load_name(message: types.Message, state: FSMContext):
    """ Catch name and write in table """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)

    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.next()
    await message.answer('Шаг 2.\nВведите Ваш номер телефона')


async def load_phone(message: types.Message, state: FSMContext):
    """ Catch a phone number """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = message.text
    await FSMClient.next()
    await message.answer('Шаг3.\nНапишите город, в котором вы проживаете. Или укажите часовой пояс.')


async def load_gmt(message: types.Message, state: FSMContext):
    """Catch a Timezone """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['gmt'] = message.text
    await FSMClient.next()
    await message.answer('Шаг4.\nМожете коротко описать ваш запрос,\n'
                         ' с которым хотите обратиться.')


async def load_comment(message: types.Message, state: FSMContext):
    """ Catch a comment """

    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['comment'] = message.text
    await sql_add_command(state)
    await state.finish()
    if await message.answer(f'Спасибо! Ваша заявка принята.\n'
                            ' Лена скоро с вами свяжется!😊\n\n'
                            '<b>Вернуться в меню:</b>',
                            reply_markup=inline_m_kb,
                            parse_mode=ParseMode.HTML
                            ):
        await bot.send_message(chat_id=os.getenv('ID_NUM'),
                               text='You have a new query! 😊 '
                                    'Please check the database!')
        await message.delete()


""" FAQ part """


async def faq(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer('<b>🔶 Часто задаваемые вопросы</b>',
                                  reply_markup=inline_faq_kb,
                                  parse_mode=ParseMode.HTML)


async def first_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 Как понять, что мне нужно к психологу?</b>\n\n'
                                  f'{arr_j[0]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


async def second_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 Как выбрать психолога?👍🏻</b>\n\n'
                                  f'{arr_j[1]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


async def third_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 С какими запросами я могу обратиться?</b>\n\n'
                                  f'{arr_j[2]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


async def four_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 Как проходит сессия?</b>\n\n'
                                  f'{arr_j[3]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


async def five_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 Как часто нужно встречаться?</b>\n\n'
                                  f'{arr_j[4]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


async def six_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 Сколько нужно сессий, для результата?</b>\n\n'
                                  f'{arr_j[5]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


async def seven_query(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await callback.message.answer(f'<b>🔶 Психолог, психотерапевт и психиатр - в чем отличия?</b>\n\n'
                                  f'{arr_j[6]}\n\n'
                                  f'<b>Еще вопросы:</b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=inline_faq_kb)


"""Send Your Question part"""


class FormQuestion(StatesGroup):
    """ Start the StatesMachine """
    question = State()
    name = State()
    phone_n = State()


async def send_question(callback: types.CallbackQuery):
    if inline_m_kb or inline_kb:
        await callback.message.delete()
    await FormQuestion.question.set()
    await callback.message.answer('<b>🔶 Напишите свой вопрос</b>\n'
                                  ' и Лена ответит вам в ближайшее время.\n'
                                  'или напишите: <b>отмена</b>', parse_mode=ParseMode.HTML)


async def cancel_state(message: types.Message, state: FSMContext):
    """ Cancel states """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.reply('OK. 👍🏻', reply_markup=inline_m_kb)


async def load_question(message: types.Message, state: FSMContext):
    """ Catch a first state """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['question'] = message.text

    await FormQuestion.next()
    await message.answer('Напишите свое имя:')


async def load_name2(message: types.Message, state: FSMContext):
    """ Catch a second state """

    await message.delete()
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['name'] = message.text

    await FormQuestion.next()
    await message.answer('Укажите ваш номер телефона,'
                         '\nчтобы Лена вам ответила:'
                         )


async def load_phone_n(message: types.Message, state: FSMContext):
    """ Catch a third state and send it all in db """
    if message.from_user.id >= 1:
        await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
    async with state.proxy() as data:
        data['phone_n'] = message.text
    await sql_add_command2(state)
    await state.finish()
    if await message.answer('Спасибо!\n Ваш вопрос принят.\n'
                            ' Лена скоро с вами свяжется!😊\n\n'
                            '<b>Вернуться в меню:</b>',
                            reply_markup=inline_m_kb,
                            parse_mode=ParseMode.HTML):
        await bot.send_message(chat_id=os.getenv('ID_NUM'),
                               text='Вам задали вопрос! 😊 '
                                    'Please check the database with Questions!')
        await message.delete()


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

    '''FAQ send a question handlers'''

    dp.register_callback_query_handler(send_question, Text(startswith='/question'))
    dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_question, state=FormQuestion.question)
    dp.register_message_handler(load_name2, state=FormQuestion.name)
    dp.register_message_handler(load_phone_n, state=FormQuestion.phone_n)
