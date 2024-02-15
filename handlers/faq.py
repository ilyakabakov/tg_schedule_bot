import os

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from create_bot import bot
from dotenv import load_dotenv, find_dotenv

from database.db_queries import new_question
from handlers.client import sanitize_text, send_message_with_parse_mode, edit_message_with_parse_mode
from keyboards.client_kb import cancel_state_kb, get_menu_kb, get_faq_keyboard, get_back_to_faq_list_btn
from database.json_queries import array_json

load_dotenv(find_dotenv())

""" FAQ PART """
faq_router = Router()


@faq_router.callback_query(F.data == 'faq')
async def faq(callback: types.CallbackQuery):
    """ FAQ main page """

    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='faq_header1'),
        reply_markup=get_faq_keyboard())


@faq_router.callback_query(F.data == 'first_query')
async def first_query(callback: types.CallbackQuery):
    """ First response page """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_1'),
        await array_json(user='client_content', query='faq_header2'))


@faq_router.callback_query(F.data == 'second_query')
async def second_query(callback: types.CallbackQuery):
    """ Second response page """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_2'),
        await array_json(user='client_content', query='faq_header3'))


@faq_router.callback_query(F.data == 'eight_query')
async def eight_query(callback: types.CallbackQuery):
    """ Eight response page.
        by display order """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_9'),
        await array_json(user='client_content', query='faq_header4'))


@faq_router.callback_query(F.data == 'third_query')
async def third_query(callback: types.CallbackQuery):
    """ Third response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_3'),
        await array_json(user='client_content', query='faq_header5'))


@faq_router.callback_query(F.data == 'four_query')
async def four_query(callback: types.CallbackQuery):
    """ Four response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_4'),
        await array_json(user='client_content', query='faq_header6'))


@faq_router.callback_query(F.data == 'five_query')
async def five_query(callback: types.CallbackQuery):
    """ Five response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_5'),
        await array_json(user='client_content', query='faq_header7'))


@faq_router.callback_query(F.data == 'six_query')
async def six_query(callback: types.CallbackQuery):
    """ Six response page. """

    await send_faq_response(
        callback.message,
        await array_json(user='client_content', query='query_6'),
        await array_json(user='client_content', query='faq_header8'))


@faq_router.callback_query(F.data == 'seven_query')
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
                            reply_markup=get_back_to_faq_list_btn())


""" SEND YOUR QUESTION PART """


class FormQuestion(StatesGroup):
    """ Create FSM model for Ask a Question """

    question = State()
    name = State()
    phone_n = State()


@faq_router.callback_query(F.data == 'question')
async def send_question(callback: types.CallbackQuery, state: FSMContext) -> None:
    """ Start the form by asking the user to enter their question """

    await state.set_state(FormQuestion.question)

    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='send_question'),
        reply_markup=cancel_state_kb())


@faq_router.message(FormQuestion.question)
async def load_question(message: types.Message, state: FSMContext):
    """ Save the user's question and move to the next state """

    await state.update_data(question=sanitize_text(message.text))
    await state.set_state(FormQuestion.name)
    await send_message_with_parse_mode(
        message,
        await array_json(user='client_content', query='name_query'),
        reply_markup=cancel_state_kb())


@faq_router.message(FormQuestion.name)
async def load_name2(message: types.Message, state: FSMContext):
    """ Save the user's name and move to the next state """

    await state.update_data(name=sanitize_text(message.text))
    await state.set_state(FormQuestion.phone_n)
    await send_message_with_parse_mode(
        message,
        await array_json(user='client_content', query='phone_number_query2'),
        reply_markup=cancel_state_kb())


@faq_router.message(FormQuestion.phone_n)
async def load_phone_number(message: types.Message, state: FSMContext):
    """ Saving last response in state
        and saving all state in db """

    await state.update_data(phone_n=sanitize_text(message.text))
    data = await state.get_data()
    await new_question(data)
    await state.clear()
    if await send_message_with_parse_mode(
            message,
            await array_json(user='client_content', query='question_complete_answer'),
            reply_markup=get_menu_kb()):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text=await array_json(user='client_content', query='send_message_to_owner2'))
        await message.delete()
