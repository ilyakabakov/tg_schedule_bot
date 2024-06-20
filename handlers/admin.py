import os

from aiogram.filters import Command, StateFilter

from aiogram import types, Router, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv

from database.db_queries import new_meeting, get_clients_data, get_event_clients_data, delete_meeting_client_data, \
    get_questions_data, delete_question_data, delete_client_data, get_client_data
from database.json_queries import array_json

from keyboards.admin_kb import admin_keyboard, back_to_admin_menu
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
from filters.chat_types import ChatTypeFilter, IsAdmin

from keyboards.client_kb import cancel_state_kb, get_menu_kb

load_dotenv(find_dotenv())
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

""" Admin authentication State Machine """


class Auth(StatesGroup):
    username = State()
    password = State()


@admin_router.message(StateFilter(None), Command('admin'))
async def get_username(message: types.Message, bot: Bot, state: FSMContext) -> None:
    await state.set_state(Auth.username)
    await bot.send_message(
        message.from_user.id,
        text='LOGIN:',
        reply_markup=cancel_state_kb())


@admin_router.message(Auth.username)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Auth.password)
    await message.answer(
        text="PASSWORD:",
        reply_markup=cancel_state_kb())


@admin_router.message(Auth.password)
async def get_access(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if data.get('username') == os.getenv('LOGIN') and data.get('password') == os.getenv('PASSWORD'):
        await state.clear()
        await message.answer(
            await array_json(
                user="admin_content",
                query="hello_page"
            ),
            reply_markup=admin_keyboard()
        )
    else:
        await state.clear()
        await message.answer(text=f"Login: {data.get('username')} and password: {data.get('password')} incorrect.\n"
                                  f"Permission denied")


"""CLIENT DB PART"""


@admin_router.callback_query(F.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    """ Delete one item in clients database """
    await delete_client_data(callback_query.data.replace('del ', ''))
    await callback_query.message.edit_text(text=f'ID: {callback_query.data.replace("del ", "")} был удален!',
                                           reply_markup=back_to_admin_menu())


@admin_router.callback_query(F.data == 'Delete')
async def delete_item(callback: types.CallbackQuery):
    """ Get choice for deleting from clients db"""

    try:
        arr = await get_clients_data()
        for row in arr:
            await callback.message.answer(
                f'Client_id: {row.client_id}\n'
                f'Name: {row.name}\n'
                f'Phone_number: {row.phone_number}\n'
                f'GMT: {row.gmt}\n'
                f'Query: {row.comment}', reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text=f'УДАЛИТЬ: {row.name}',
                                                 callback_data=f'del {row.client_id}'),
                            InlineKeyboardButton(text='Вернуться в меню',
                                                 callback_data='admin_menu')
                        ]
                    ]
                )
            )
    except Exception as ex:
        print(f'Invalid answer from DB: {ex}')


@admin_router.callback_query(F.data == 'admin_menu')
async def admins_menu(callback: types.CallbackQuery):
    await callback.message.answer(await array_json(user="admin_content", query="admins_menu"),
                                  reply_markup=admin_keyboard())


@admin_router.callback_query(F.data == 'Open_db')
async def open_all(callback: types.CallbackQuery):
    """ Open clients table """

    try:
        arr = await get_clients_data()
        for row in arr:
            await callback.message.answer(f"ID: {row.client_id}\n"
                                          f"Имя: {row.name}\n"
                                          f"Номер телефона: {row.phone_number}\n"
                                          f"Город/Часовой пояс:{row.gmt}\n"
                                          f"Запрос: {row.comment}")
            await callback.message.answer("Clients", reply_markup=back_to_admin_menu())
    except Exception as ex:
        print(f'Invalid answer from DB: {ex}')


@admin_router.callback_query(F.data == 'Open_last_client')
async def open_last_client(callback: types.CallbackQuery):
    """ Open last client from clients table"""
    try:
        arr = await get_client_data()
        await callback.message.answer(f"ID: {arr.client_id}\n"
                                      f"Имя: {arr.name}\n"
                                      f"Номер телефона: {arr.phone_number}\n"
                                      f"Город/Часовой пояс:{arr.gmt}\n"
                                      f"Запрос: {arr.comment}\n"
                                      f"МЕНЮ:", reply_markup=back_to_admin_menu())
    except Exception as ex:
        print(f'Invalid answer from DB: {ex}')


""" QUESTIONS DB PART """

"""DELETE FROM questions HANDLERS """


@admin_router.callback_query(F.data.startswith('dlt '))
async def del_callback_run_q(callback_query: types.CallbackQuery):
    """ Delete one item from questions database """
    await delete_question_data(callback_query.data.replace('dlt ', ''))
    await callback_query.message.edit_text(text=f'ID: {callback_query.data.replace("dlt ", "")} был удален!',
                                           reply_markup=back_to_admin_menu())


@admin_router.callback_query(F.data == 'Clear_question')
async def delete_question(callback: types.CallbackQuery):
    """ Get choice for deleting from questions db"""

    try:
        arr = await get_questions_data()
        for row in arr:
            await callback.message.answer(
                f'ID: {row.question_id}\n'
                f'Имя: {row.name}\n'
                f'Номер телефона: {row.phone_number}\n'
                f'Вопрос: {row.question}\n',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text=f'УДАЛИТЬ: {row.name}',
                                                 callback_data=f'dlt {row.question_id}'),
                            InlineKeyboardButton(text='Вернуться в меню',
                                                 callback_data='admin_menu')
                        ]
                    ]
                )
            )
    except Exception as ex:
        print(f'Invalid answer from DB: {ex}')


""" GET FROM questions HANDLERS"""


@admin_router.callback_query(F.data == 'Open_questions_db')
async def open_questions_db(callback: types.CallbackQuery):
    """ Get all questions from questions table """

    try:
        arr = await get_questions_data()
        for row in arr:
            await callback.message.answer(f"ID: {row.question_id}\n"
                                          f"Вопрос: <b>{row.question}</b>\n"
                                          f"Имя: <b>{row.name}</b>\n"
                                          f"Номер телефона:\n "
                                          f"<b>{row.phone_number}</b>",
                                          parse_mode=ParseMode.HTML)
        await callback.message.answer("Questions", reply_markup=back_to_admin_menu())
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


@admin_router.callback_query(StateFilter(None), F.data == 'Create_event')
async def create_event(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FormEvent.naming)
    await callback.message.answer(await array_json(user='admin_content', query="meeting_naming"),
                                  reply_markup=cancel_state_kb())


@admin_router.callback_query(F.text.startswith('cancel'))
@admin_router.callback_query(F.data == 'cancel')
@admin_router.callback_query(F.text.casefold() == 'cancel')
async def event_cancel_handler(message: types.Message, state: FSMContext):
    """ CANCEL state """
    await message.delete()
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('👍🏻 Отменено.', reply_markup=back_to_admin_menu())


@admin_router.message(FormEvent.naming)
async def get_naming(message: types.Message, state: FSMContext):
    await state.update_data(naming=message.text)
    await state.set_state(FormEvent.place)
    await message.answer(await array_json(user='admin_content', query="meeting_place"),
                         reply_markup=cancel_state_kb())


@admin_router.message(FormEvent.place)
async def get_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(FormEvent.date)
    await message.answer(await array_json(user='admin_content', query="meeting_date"),
                         reply_markup=cancel_state_kb())


@admin_router.message(FormEvent.date)
async def get_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(FormEvent.time)
    await message.answer(await array_json(user='admin_content', query="meeting_time"),
                         reply_markup=cancel_state_kb())


@admin_router.message(FormEvent.time)
async def get_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(FormEvent.price)
    await message.answer(f"{await array_json(user='admin_content', query='meeting_price')}\n"
                         f"{await array_json(user='other_content', query='currency_gel')}",
                         reply_markup=cancel_state_kb())


@admin_router.message(FormEvent.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await new_meeting(data)
    await state.clear()
    await message.answer(await array_json(user='admin_content', query="meeting_complete"),
                         reply_markup=get_menu_kb())


"""EVENT CLIENTS DB"""


@admin_router.callback_query(F.data.startswith('clr '))
async def del_callback_run_meet(callback_query: types.CallbackQuery):
    """ Delete one item from meeting database """
    await delete_meeting_client_data(callback_query.data.replace('clr ', ''))
    await callback_query.message.edit_text(text=f'{callback_query.data.replace("clr ", "")} was deleted!',
                                           reply_markup=back_to_admin_menu())


@admin_router.callback_query(F.data == 'Delete_list')
async def delete_meeting_clients(callback: types.CallbackQuery):
    """ Get choice for deleting from meetings db"""

    read = await get_event_clients_data()
    for row in read:
        await callback.message.answer(
            f'ID: {row.client_id}\n'
            f'Имя и Фамилия: {row.full_name}\n'
            f'Номер телефона: {row.phone_number}\n',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f'УДАЛИТЬ: {row.full_name}',
                                             callback_data=f'clr {row.client_id}'),
                        InlineKeyboardButton(text='Вернуться в меню',
                                             callback_data='admin_menu')
                    ]
                ]
            )
        )


@admin_router.callback_query(F.data == 'show_list')
async def get_meeting_client_list(callback: types.CallbackQuery):
    try:
        read = await get_event_clients_data()
        for row in read:
            await callback.message.answer(f'ID: <b>{row.client_id}</b>\n\n'
                                          f'Full name: <b>{row.full_name}</b>\n'
                                          f'номер телефона: <b>{row.phone_number}</b>\n',
                                          reply_markup=back_to_admin_menu(), parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(f'Invalid answer from DB: {ex}')
