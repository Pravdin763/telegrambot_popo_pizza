from aiogram import Bot, Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp= Dispatcher(bot, storage=storage)