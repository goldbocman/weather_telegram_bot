from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ChatType

from loader import dp, bot
from keyboards import start_keyboard


@dp.message_handler(Text('Узнать погоду'), chat_type=ChatType.PRIVATE)
async def bot_start(message: types.Message):
    await message.answer(f"Погода в городе ...")
