from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ChatType, ParseMode
from forms.user import User
from data import db_session

from loader import dp, bot
from states.change_city import CityChanger


class FSMCity(StatesGroup):
    city = State()


@dp.message_handler(commands='set_city', state=None)
async def cm_start(message: types.Message):
    await FSMCity.city.set()
    await message.reply('Напишите название города')


@dp.message_handler(state=FSMCity.city)
async def get_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        session = db_session.create_session()
        user = session.query(User).filter(message.from_user.id == User.chat_id).first()
        user.town = message.text
        session.commit()
        session.close()
    await message.reply('Название города сохранено')
    await state.finish()
