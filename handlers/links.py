from aiogram import types
from keyboards import inline_keyboard

from aiogram.types import ChatType

from loader import dp, bot


@dp.message_handler(commands=['links'], chat_type=ChatType.PRIVATE)
async def links(message: types.Message):
    await message.answer(f"Наш гитхаб: ", reply_markup=inline_keyboard)