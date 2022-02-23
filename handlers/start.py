from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ChatType

from loader import dp, bot
from keyboards import start_keyboard


@dp.message_handler(CommandStart(), chat_type=ChatType.PRIVATE)
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=start_keyboard)
