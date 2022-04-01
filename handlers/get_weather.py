import json

import requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ChatType, ParseMode
from forms.user import User
from data import db_session
from tools.geocode import get_coords

from config import WEATHER_TOKEN
from loader import dp, bot
from keyboards import start_keyboard


@dp.message_handler(text=['\U0001F326 Узнать погоду'])
async def get_weather(message: types.Message):
    try:
        session = db_session.create_session()
        user = session.query(User).filter(message.from_user.id == User.chat_id).first()
        town = user.town
        coords = get_coords(town)
        response = json.loads(requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU&hours=false', headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)
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
    except IndexError:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так. Проверьте правильность написания города.')


@dp.message_handler(commands=['get_weather'])
async def gt_wthr(message: types.Message):
    try:
        session = db_session.create_session()
        user = session.query(User).filter(message.from_user.id == User.chat_id).first()
        town = user.town
        arg = message.get_args()
        if town is None:
            raise IndexError
        coords = get_coords(town)
        if len(arg) == 0:
            response = json.loads(requests.get(
                f'https://api.weather.yandex.ru/v2/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU&hours=false',
                headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)
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
        else:
            if int(arg[0]) > 6:
                raise ValueError
            response = json.loads(
                requests.get(
                    f'https://api.weather.yandex.ru/v2/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU&limit={str(int(arg[0])+1)}',
                    headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)
            temp_avg = response['forecasts'][int(arg[0])]['parts']['day']['temp_avg']
            temp_max = response['forecasts'][int(arg[0])]['parts']['day']['temp_max']
            wind_speed = response['forecasts'][int(arg[0])]['parts']['day']['wind_speed']
            pressure = response['forecasts'][int(arg[0])]['parts']['day']['pressure_mm']
            humidity = response['forecasts'][int(arg[0])]['parts']['day']['humidity']
            wind_gust = response['forecasts'][int(arg[0])]['parts']['day']['wind_gust']
            forecast = response['forecasts'][int(arg[0])]['date']
            await bot.send_message(message.from_user.id,
                                   f"Прогноз для города {town}"
                                   f" на {forecast}:\n"
                                   f"<b>Средняя температура:</b> {temp_avg}°C\n"
                                   f"<b>Максимальная температура</b> {temp_max}°C\n"
                                   f"<b>Давление:</b> {pressure} мм.рт.ст.\n"
                                   f"<b>Влажность:</b> {humidity}%\n"
                                   f"<b>Ветер:</b> {wind_speed} м/c\n"
                                   f"<b>Порывы ветра до</b> {wind_gust} м/c\n", parse_mode=ParseMode.HTML)
        user.requestsam += 1
        session.commit()
        session.close()
    except IndexError:
        await bot.send_message(message.from_user.id,
                               'Что-то пошло не так. Проверьте правильность написания города.')
    except ValueError:
        await bot.send_message(message.from_user.id,
                               'Получить прогноз можно максимум на 6 дней вперёд')

