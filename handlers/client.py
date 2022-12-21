from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import dp
from database.sqlite_db import sql_add_command
from keyboards.client_kb import inline_kb, inline_faq_kb, inline_m_kb
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


async def command_start(message: types.Message):
    await message.answer(f'Привет, я бот для записи к высококлассному психологу name! 😎',
                         reply_markup=inline_kb)


async def bio(callback: types.CallbackQuery):
    await callback.message.answer(f'Bio 😁')
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


async def prices(callback: types.CallbackQuery):
    await callback.message.answer(
        '1 консультация - money. \n3 консультации - money. \n5 консультаций - money.')
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


# REQUEST MENU
# @dp.callback_query_handler(Text(startswith='/Menu'))
async def show_menu(callback: types.CallbackQuery):
    await callback.message.answer('Меню', reply_markup=inline_kb)


"""Заявка на консультацию"""

"""Входим в режим машины состояний"""


class FSMClient(StatesGroup):
    name = State()
    phone = State()
    gmt = State()
    comment = State()


async def writing_on_consult(callback: types.CallbackQuery):
    await FSMClient.name.set()
    await callback.message.reply('Подача заявки состоит из четырех вопросов. '
                                 '\nЕсли вы передумали, то достаточно написать "отмена"')
    await callback.message.reply('Шаг1. Напишите ваше имя')


""" CANCEL state"""


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK. Ваша заявка отменена.')


""" catch name and write in table"""


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.next()
    await message.reply('Шаг2. Введите ваш номер телефона(Пример:8-912-345-67-89)')


"""Ловим номер"""


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_n'] = message.text
    await FSMClient.next()
    await message.reply('Шаг3. Укажите город в котором вы проживаете')


"""Часовой пояс"""


async def load_gmt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gmt'] = message.text
    await FSMClient.next()
    await message.reply('Шаг4. Напишите ваш запрос с которым вы хотите обратиться')


"""ловим комментарий"""


async def load_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    await sql_add_command(state)
    await state.finish()
    await message.answer('Спасибо! Ваша заявка принята, Лена скоро с вами свяжется!')
    await message.answer('Вернуться в меню', reply_markup=inline_m_kb)


""" FAQ """


async def faq(callback: types.CallbackQuery):
    await callback.message.reply('Часто задаваемые вопросы', reply_markup=inline_faq_kb)


@dp.callback_query_handler(Text(startswith='/first_query'))  # register_handlers
async def first_query(callback: types.CallbackQuery):
    await callback.message.answer('Потому, что психолог поможет найти ответы,\n'
                                  'на многие вопросы о собственном психологическом состоянии'
                                  ' много много много текста')
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


@dp.callback_query_handler(Text(startswith='/second_query'))
async def first_query(callback: types.CallbackQuery):
    await callback.message.answer('So much text')
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


@dp.callback_query_handler(Text(startswith='/third_query'))
async def first_query(callback: types.CallbackQuery):
    await callback.message.answer('So much text')
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


@dp.callback_query_handler(Text(startswith='/four_query'))
async def first_query(callback: types.CallbackQuery):
    await callback.message.answer('So much text')
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


@dp.callback_query_handler(Text(startswith='/fjve_query'))
async def first_query(callback: types.CallbackQuery):
    await callback.message.answer('So much text')
    await callback.message.answer('Еще вопросы:', reply_markup=inline_faq_kb)
    await callback.message.answer('Вернуться в меню', reply_markup=inline_m_kb)


# registration handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(bio, Text(startswith='/bio'))
    dp.register_callback_query_handler(prices, Text(startswith='/price'))
    dp.register_callback_query_handler(show_menu, Text(startswith='/Menu'))

    dp.register_callback_query_handler(writing_on_consult, Text(startswith='/write'), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMClient.name)
    dp.register_message_handler(load_phone, state=FSMClient.phone)
    dp.register_message_handler(load_gmt, state=FSMClient.gmt)
    dp.register_message_handler(load_comment, state=FSMClient.comment)

    dp.register_callback_query_handler(faq, Text(startswith='/faq'))
