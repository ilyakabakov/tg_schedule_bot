import os

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from create_bot import bot
from dotenv import load_dotenv, find_dotenv

from database.db_queries import new_client
from keyboards.client_kb import cancel_state_kb, main_menu_kb, get_menu_kb
from database.json_queries import array_json

load_dotenv(find_dotenv())
client_router = Router()


@client_router.message(CommandStart())
async def command_start(message: types.Message):
    """ Start bot handler """

    try:
        await bot.send_message(
            message.from_user.id,
            await array_json(user="client_content", query='hello'),
            reply_markup=main_menu_kb(),
            parse_mode=ParseMode.HTML)
    except Exception as ex:
        print(ex)


async def delete_message(message):
    """ Anti-flood from bot func. This function for deleting previous message by bot. """

    if get_menu_kb() or get_menu_kb():
        await message.delete()


@client_router.callback_query(F.data == "bio")
async def bio(callback: types.CallbackQuery):
    """ Show about page """

    await edit_message_with_parse_mode(
        callback.message,
        f"{await array_json(user='client_content', query='bio')}\n\n"
        f"<b>Вернуться в меню:</b>",
        reply_markup=get_menu_kb())


@client_router.callback_query(F.data == "price")
async def prices(callback: types.CallbackQuery):
    """ Show prices page """

    await edit_message_with_parse_mode(
        callback.message,
        f"{await array_json(user='client_content', query='prices')}\n\n"
        f"<b>Вернуться в меню:</b>",
        reply_markup=get_menu_kb())


""" REQUEST MENU """


@client_router.callback_query(F.data == 'Menu')
async def show_menu(callback: types.CallbackQuery):
    """ This page displayed
        when user tap a back to menu button """

    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user="client_content", query="hello"), reply_markup=main_menu_kb())


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


@client_router.callback_query(F.data == 'write')
async def writing_on_consult(callback: types.CallbackQuery, state: FSMContext) -> None:
    """ Start the State Machine """
    await state.set_state(FSMClient.name)
    await edit_message_with_parse_mode(
        callback.message,
        await array_json(user='client_content', query='writing_on_consultation'),
        reply_markup=cancel_state_kb())


@client_router.callback_query(F.text.startswith('cancel'))
@client_router.callback_query(F.data == 'cancel')
@client_router.callback_query(F.text.casefold() == 'cancel')
async def cancel_state_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """ CANCEL state. """

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.edit_text(
        await array_json(user='client_content', query='cancel_state'),
        reply_markup=get_menu_kb())


@client_router.message(FSMClient.name)
async def load_name(message: types.Message, state: FSMContext):
    """ Save name in state """
    await message.delete()
    await state.update_data(name=sanitize_text(message.text))
    await state.set_state(FSMClient.phone)
    await send_message_with_parse_mode(
        message,
        await array_json(user='client_content', query='phone_number_query'),
        reply_markup=cancel_state_kb())


@client_router.message(FSMClient.phone)
async def load_phone(message: types.Message, state: FSMContext):
    """ Save a phone number in state """

    await message.delete()
    await state.update_data(phone=sanitize_text(message.text))
    await state.set_state(FSMClient.gmt)
    await send_message_with_parse_mode(
        message,
        await array_json(user='client_content', query='gmt_query'),
        reply_markup=cancel_state_kb())


@client_router.message(FSMClient.gmt)
async def load_gmt(message: types.Message, state: FSMContext):
    """Save a Timezone in state """

    await message.delete()
    await state.update_data(gmt=sanitize_text(message.text))
    await state.set_state(FSMClient.comment)
    await send_message_with_parse_mode(
        message,
        await array_json(user='client_content', query='comment'),
        reply_markup=cancel_state_kb())


@client_router.message(FSMClient.comment)
async def load_comment(message: types.Message, state: FSMContext):
    """ Save a comment and save all state in db.
        Finish current state """
    await delete_message(message)
    await state.update_data(comment=sanitize_text(message.text))
    data = await state.get_data()
    await new_client(data)
    await state.clear()
    if await send_message_with_parse_mode(
            message,
            await array_json(user='client_content', query='thanks_answer'),
            reply_markup=get_menu_kb()):
        await bot.send_message(
            chat_id=os.getenv('ID_NUM'),
            text=await array_json(user='client_content', query='send_message_to_owner'))
        await message.delete()
