from create_bot import dp
from aiogram.utils import executor
from handlers import client, admin, other
from database import sqlite_db


def if_started():
    """Bot started from here"""
    print('Bot is ONLINE')
    sqlite_db.sql_start()


# Register handlers here
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=if_started())
