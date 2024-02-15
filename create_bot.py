from aiogram import Bot
from aiogram import Dispatcher
import os

from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# storage_m = RedisStorage('localhost',
#                         6379,
                         #  password=os.getenv('REDIS_PASSWORD'),
#                         )
# pool_size=10,
# prefix="my_fsm_key")
storage_m = RedisStorage.from_url(
    # f"redis://{os.getenv('REDIS_PASSWORD')}@localhost:6379/my_fsm_key"
    "redis://localhost:6379/my_fsm_key"
)
bot = Bot(token=os.getenv('TOKEN'),
          parse_mode=ParseMode.HTML
          )
bot.my_admins_list = []
dp = Dispatcher(storage=storage_m)
