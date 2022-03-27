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
        await bot.send_message(message.from_user.id,
                                  f"Прогноз для города {town}"
                                  f" на {forecast}:\n"
                                  f"<b>Температура:</b> {temp_now}°C\n"
                                  f"Ощущается как {feels_like}°C\n"
                                  f"<b>Давление:</b> {pressure} мм.рт.ст.\n"
                                  f"<b>Влажность:</b> {humidity}%\n"
                                  f"<b>Ветер:</b> {wind_speed} м/c\n"
                                  f"Порывы ветра до {wind_gust} м/c\n", parse_mode=ParseMode.HTML)
        user.requestsam += 1
        session.commit()
        session.close()
    except ValueError:
        await bot.send_message(message.from_user.id, 'Сперва вам нужно вызвать команду /set_city, чтобы мы знали, какой город вам нужен =)')
