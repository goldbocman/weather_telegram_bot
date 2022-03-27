import json

import requests as requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ChatType, ParseMode
from forms.user import User
from data import db_session
from tools.geocode import get_coords

from config import WEATHER_TOKEN
from loader import dp, bot
from keyboards import start_keyboard
from config import PROFILE_MESSAGE


@dp.message_handler(text='\U0001F464 Профиль')
async def get_weather(message: types.Message):
    session = db_session.create_session()
    user = session.query(User).filter(message.from_user.id == User.chat_id).first()
    town = user.town
    requestsam = user.requestsam
    text_message = PROFILE_MESSAGE.replace('%user_mention%', f'{message.from_user.mention}')
    text_message = text_message.replace('%user_town%', f'{town}')
    text_message = text_message.replace('%user_weather_requests%', f'{requestsam}')
    UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
    await bot.send_photo(chat_id=message.from_user.id, photo=UserProfilePhotos['photos'][0][0]['file_id'], caption=text_message)
    # await bot.send_message(message.from_user.id, text_message)
    session.commit()
    session.close()
