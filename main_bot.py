import asyncio
import logging
import os
import sys

from create_bot import dp, bot
from handlers import client, faq, events, admin, other
from database import db_creating

""" Logging configuration. """

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
# aiogram framework (bot is written on 3.3.0 version of aiogram)
# sqlalchemy
# aiosqlite
# python-dotenv
# xlsxwriter
# redis

""" Starting the bot """
ALLOWED_UPDATES = [
    'message',
    'edited_message',
    'callback_query'
]


async def if_started():
    """ Function for connecting to database,
        routing and starting polling """

    logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.WARNING)

    try:
        print('Bot is ONLINE')
        await db_creating.base_start()
        dp.include_routers(client.client_router,
                           faq.faq_router,
                           events.meetings_router
                           )
        dp.include_router(admin.admin_router)
        dp.include_router(other.user_group_router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               allowed_updates=ALLOWED_UPDATES)
    except Exception as ex:
        print(f" FAILED TO START: {ex}")

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(if_started())
    except Exception as ex:
        print(f"FAILED: {ex}")
