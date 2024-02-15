from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from dotenv import load_dotenv, find_dotenv

from database.db_queries import new_meeting_client, get_events_data
from handlers.client import send_message_with_parse_mode, sanitize_text, edit_message_with_parse_mode
from keyboards.client_kb import cancel_state_kb, get_menu_kb, get_meetings_kb, \
    get_back_to_meetings_kb
from database.json_queries import array_json

load_dotenv(find_dotenv())

""" THEMATIC MEETING PART """

meetings_router = Router()


@meetings_router.callback_query(F.data == 'meeting')
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
            reply_markup=get_meetings_kb())


@meetings_router.callback_query(F.data == "about_meeting")
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
                            reply_markup=get_back_to_meetings_kb())


class FormMeeting(StatesGroup):
    """ Create FSM model for Sign up to event """

    full_name = State()
    phone_n = State()


@meetings_router.callback_query(F.data == "thematic_write")
async def write_on_meeting(callback: types.CallbackQuery, state: FSMContext):
    """ Start State Machine """

    await state.set_state(FormMeeting.full_name)
    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='write_on_meeting'),
        reply_markup=cancel_state_kb())


@meetings_router.message(FormMeeting.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    """ Saving first response in state """

    await state.update_data(full_name=sanitize_text(message.text))
    await state.set_state(FormMeeting.phone_n)
    await send_message_with_parse_mode(message,
                                       await array_json(user='client_content',
                                                        query='phone_number_query2'),
                                       reply_markup=cancel_state_kb())


@meetings_router.message(FormMeeting.phone_n)
async def get_phone_number(message: types.Message, state: FSMContext):
    """ Saving second response in state
        and saving all state in db """

    await state.update_data(phone_n=sanitize_text(message.text))
    data = await state.get_data()
    await new_meeting_client(data)
    await state.clear()
    await send_message_with_parse_mode(message,
                                       await array_json(user='client_content',
                                                        query='meeting_complete_answer'),
                                       reply_markup=get_menu_kb())
