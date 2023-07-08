# import redis
import logging
import os

import aiogram.dispatcher.filters

from create_bot import dp
from aiogram.utils import executor
from handlers import client, admin, other
from database import db_creating

""" Logging configuration """
cwd = os.getcwd()

logging.basicConfig(filename=os.path.join(cwd, 'logs/main.log'))

# Settings for logging
logger = logging.getLogger('sqlalchemy')
logger.setLevel(logging.INFO)

# Creating handler for writing logs to a file
file_handler = logging.FileHandler(os.path.join(cwd, 'logs/sql.log'))
file_handler.setLevel(logging.INFO)

# Format of log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Adding the handler to the logger
logger.addHandler(file_handler)

# Disable logging to console
logger.propagate = False


# pip install:
# aiogram
# sqlalchemy
# aiosqlite
# python-dotenv
# xlsxwriter
# redis

async def if_started():
    logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.WARNING)
    """Bot started from here"""
    try:
        print('Bot is ONLINE')
        await db_creating.base_start()
    except Exception as ex:
        print(f" FAILED TO START: {ex}")
    except aiogram.dispatcher.filters.ExceptionsFilter as ex_filter:
        print(f" FAILED TO START DISPATHCHER: {ex_filter}")


async def on_startup(dp):
    """ This function is needed to start to avoid
     an exception('courutine was never awaited')"""
    await if_started()


async def on_shutdown(dp):
    """ Func to closing connection to Redis """
    await dp.storage.close()
    await dp.storage.wait_closed()
    print('Shutdown Redis')


# Register handlers here
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown)

    except Exception as ex:
        print(f"FAILED: {ex}")
