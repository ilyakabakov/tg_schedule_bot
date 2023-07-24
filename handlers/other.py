import json
import string
from aiogram import types, Dispatcher
from create_bot import bot

""" Censoring filter """


async def cens_filter(message: types.Message):
    """ the function deletes both swear words with cens.json file
        and all the entered text, soon,
        after the reorganization of the admin panel,
        this function will delete all the entered text """

    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('database/cens.json')))) != set():
        cens_message = await message.answer('Выражайтесь культурно!')
        await message.delete()
        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=cens_message.message_id)
    await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(cens_filter)
