from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ChatType, ParseMode

from loader import dp, bot
from states.change_city import CityChanger


@dp.message_handler(Text('Сменить город'), chat_type=ChatType.PRIVATE, state=None)
async def change_city_start(message: types.Message):
    await message.answer(f"Выберите свой город")
    await CityChanger.Q_CITY_NAME.set()


@dp.message_handler(state=CityChanger.Q_CITY_NAME)
async def get_user_city(message: types.Message, state: FSMContext):
    city = message.text
    await message.answer(f"Вы выбрали город <b>{city}</b>", parse_mode=ParseMode.HTML)
    await state.finish()
