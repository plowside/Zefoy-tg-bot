from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())