from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import ChatType

from loader import dp, bot


@dp.message_handler(CommandHelp(), chat_type=ChatType.PRIVATE)
async def bot_help(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Это справка")
