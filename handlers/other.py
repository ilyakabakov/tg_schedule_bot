import json
import string
from aiogram import types, Dispatcher

"""censoring filter"""


async def cens_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cens.json')))) != set():
        await message.reply('Выражайтесь культурно!')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(cens_filter)
