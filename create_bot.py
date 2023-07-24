from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
storage_m = RedisStorage2('localhost',
                          6379,
                          db=5,
                          password=os.getenv('REDIS_PASSWORD'),
                          pool_size=10,
                          prefix="my_fsm_key")

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage_m)
