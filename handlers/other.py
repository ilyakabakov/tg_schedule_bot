import json
import string
from aiogram import types, Dispatcher
from create_bot import bot

"""censoring filter"""


async def cens_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('database/cens.json')))) != set():
        cens_message = await message.answer('Выражайтесь культурно!')
        await message.delete()

        if message.from_user.id >= 1:
            await bot.delete_message(message.chat.id, message_id=cens_message.message_id)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(cens_filter)
