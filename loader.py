from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from data import db_session

from config import TOKEN


storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
db_session.global_init('db/user.sqlite')
