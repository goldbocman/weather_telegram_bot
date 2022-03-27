import json

import requests as requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ChatType, ParseMode
from forms.user import User
from data import db_session
from tools.geocode import get_coords

from config import WEATHER_TOKEN, GET_WEATHER_MESSAGE
from loader import dp, bot
from keyboards import start_keyboard


@dp.message_handler(text='\U0001F326 Узнать погоду')
async def get_weather(message: types.Message):
    try:
        session = db_session.create_session()
        user = session.query(User).filter(message.from_user.id == User.chat_id).first()
        town = user.town
        if town is None:
            raise ValueError
        coords = get_coords(town)
        response = json.loads(requests.get(f'https://api.weather.yandex.ru/v1/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU', headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)
        temp_now = response['fact']['temp']
        feels_like = response['fact']['feels_like']
        sky = response['fact']['condition']
        wind_speed = response['fact']['wind_speed']
        pressure = response['fact']['pressure_mm']
        humidity = response['fact']['humidity']
        wind_gust = response['fact']['wind_gust']
        forecast = response['forecasts'][0]['date']
        text_message = GET_WEATHER_MESSAGE.replace('%town%', str(town))
        text_message = text_message.replace('%forecast%', str(forecast))
        text_message = text_message.replace('%temp_now%', str(temp_now))
        text_message = text_message.replace('%feels_like%', str(feels_like))
        text_message = text_message.replace('%pressure%', str(pressure))
        text_message = text_message.replace('%humidity%', str(humidity))
        text_message = text_message.replace('%wind_speed%', str(wind_speed))
        text_message = text_message.replace('%wind_gust%', str(wind_gust))
        await bot.send_message(message.from_user.id, text_message)
        user.requestsam += 1
        session.commit()
        session.close()
    except ValueError:
        await bot.send_message(message.from_user.id, 'Сперва вам нужно вызвать команду /set_city, чтобы мы знали, какой город вам нужен =)')
