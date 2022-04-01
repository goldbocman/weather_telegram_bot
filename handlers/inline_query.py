import json
import re

import requests
from aiogram.types import InlineQueryResultArticle, InlineKeyboardMarkup, InputTextMessageContent, InlineKeyboardButton, \
    InlineQuery

from config import WEATHER_TOKEN
from loader import dp, bot
from tools.geocode import get_coords


@dp.inline_handler()  # Обработчик любых инлайн-запросов
async def inline(query: InlineQuery):
    town = query.query
    coords = get_coords(town)
    req = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU',
                     headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content
    response = json.loads(req)
    temp_now = response['fact']['temp']
    feels_like = response['fact']['feels_like']
    sky = response['fact']['condition']
    wind_speed = response['fact']['wind_speed']
    pressure = response['fact']['pressure_mm']
    humidity = response['fact']['humidity']
    wind_gust = response['fact']['wind_gust']
    forecast = response['forecasts'][0]['date']
    r_sum = InlineQueryResultArticle(
        id='1', title="Погода",
        # Описание отображается в подсказке,
        # message_text - то, что будет отправлено в виде сообщения
        description=f"Узнать погоду города: {town}",
        input_message_content=InputTextMessageContent(
            message_text=f"Прогноз для города {town}"
                           f" на {forecast}:\n"
                           f"Температура: {temp_now}°C\n"
                           f"Ощущается как {feels_like}°C\n"
                           f"Давление: {pressure} мм.рт.ст.\n"
                           f"Влажность: {humidity}%\n"
                           f"Ветер: {wind_speed} м/c\n"
                           f"Порывы ветра до {wind_gust} м/c\n")
    )
    await query.answer([r_sum])
