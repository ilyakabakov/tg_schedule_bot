from aiogram import Bot
from aiogram import Dispatcher
import os

from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

storage_m = RedisStorage.from_url(
    # f"redis://{os.getenv('REDIS_PASSWORD')}@localhost:6379/0"  # Uncomment this string if bot deployed on server.
    "redis://localhost:6379/0"  # For redis on my machine. Comment this string if deployed on server
)
bot = Bot(token=os.getenv('TOKEN'),
          parse_mode=ParseMode.HTML
          )
bot.my_admins_list = []
dp = Dispatcher(storage=storage_m)
