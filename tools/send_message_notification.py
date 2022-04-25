import datetime
import json
import os
import random

import requests
from PIL import Image, ImageFont, ImageDraw
from aiogram import types
from aiogram.types import ParseMode, InputFile

from config import WEATHER_TOKEN, WEATHER_CONDITIONS_URLS, WEATHER_SHORTCUTS, GET_WEATHER_MESSAGE
from data import db_session
from forms.user import User
from loader import bot
from tools.geocode import get_coords


WINDOW_SIZE = (860, 400)


async def send_message_notification(user_id: int, type_notification: int):
    if type_notification == 1:
        session = db_session.create_session()
        user = session.query(User).filter(user_id == User.chat_id).first()
        town = user.town
        if town is None:
            raise ValueError
        coords = get_coords(town)
        response = json.loads(requests.get(
            f'https://api.weather.yandex.ru/v1/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU&limit=7',
            headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)
        file_to_send_id = 'AgACAgIAAxkDAAICXWJQbsx2_m92oEuaFinehsIjFvQyAAIeuzEbW-OASqiHJXIDPw69AQADAgADeQADIwQ'
        sec_message = await bot.send_photo(user_id, photo=file_to_send_id, caption='<b>Секундочку...</b>',
                                           parse_mode=ParseMode.HTML)

        im = Image.new('RGBA', WINDOW_SIZE, color=('white'))  # #202124
        font_main = ImageFont.truetype('19755.ttf', size=25)
        font_day = ImageFont.truetype('19755.ttf', size=20)
        font_simple = ImageFont.truetype('arial.ttf', size=18)

        ## градиент начало
        gradient = Image.new('RGBA', im.size, color=0)
        drawer = ImageDraw.Draw(gradient)

        f_co = (57, 62, 70)
        t_co = (34, 40, 49)
        for i, color in enumerate(interpolate(f_co, t_co, im.width * 2)):
            drawer.line([(i, 0), (0, i)], tuple(color), width=1)
        im.paste(gradient, mask=gradient)
        ## градиент конец

        draw = ImageDraw.Draw(im)

        draw.rounded_rectangle((2, 2, WINDOW_SIZE[0] - 2, WINDOW_SIZE[1] - 2), outline="#FFD369",
                               width=4, radius=7)
        draw.text(xy=(WINDOW_SIZE[0] // 2, 25),
                  text='Прогноз погоды на следующие 7 дней',
                  font=font_main,
                  fill='#EEEEEE',
                  anchor='mm')
        start_position = [22, 280]

        for i in range(7):
            forecast = response['forecasts'][i]['parts']['day']
            temp_min = forecast['temp_min']
            temp_max = forecast['temp_max']
            feels_like = forecast['feels_like']
            condition = forecast['condition']
            wind_speed = forecast['wind_speed']
            pressure = forecast['pressure_mm']
            humidity = forecast['humidity']
            wind_gust = forecast['wind_gust']
            date = response['forecasts'][i]['date']

            time = datetime.datetime.strptime(date, '%Y-%m-%d')
            day_text = WEATHER_SHORTCUTS[time.strftime('%A').lower()]

            condition_image = Image.open(f'data//photos//{WEATHER_CONDITIONS_URLS[condition]}')
            condition_image = condition_image.resize((84, 84))
            condition_image = condition_image.convert("RGBA")
            im.paste(condition_image, (start_position[0] + 5, start_position[1] + 10), condition_image)
            draw.rounded_rectangle((start_position[0] - 2, 50, start_position[0] + 98, 380), outline="#8f732f",
                                   width=4, radius=7)
            draw.text(xy=(start_position[0] + 50, 72),  # -40
                      text=day_text,
                      font=font_day,
                      fill='#EEEEEE',
                      anchor='mm')

            draw.rounded_rectangle((start_position[0] + 10, 90, start_position[0] + 85, 93), outline="#8f732f", fill="#8f732f",
                                   width=1, radius=2)

            draw.text(xy=(start_position[0] + 67, 150),
                      text=f'{temp_min}°C',
                      font=font_simple,
                      fill='#bfbdbd',
                      anchor="mm")
            draw.text(xy=(start_position[0] + 67, 130),
                      text=f'{temp_max}°C',
                      font=font_simple,
                      fill='#EEEEEE',
                      anchor="mm")

            draw.text(xy=(start_position[0] + 67, 190),
                      text=f'{humidity}%',
                      font=font_simple,
                      fill='#EEEEEE',
                      anchor="mm")

            draw.text(xy=(start_position[0] + 67, 230),
                      text=f'{wind_speed}',
                      font=font_simple,
                      fill='#EEEEEE',
                      anchor="mm")
            draw.text(xy=(start_position[0] + 67, 250),
                      text=f'м/с',
                      font=font_simple,
                      fill='#bfbdbd',
                      anchor="mm")
            thermometer_image = Image.open('data//photos//thermometer.png')
            thermometer_image = thermometer_image.resize((40, 40))
            thermometer_image = thermometer_image.convert("RGBA")
            im.paste(thermometer_image, (start_position[0], 120), thermometer_image)

            humidity_image = Image.open('data//photos//humidity.png')
            humidity_image = humidity_image.resize((32, 32))
            humidity_image = humidity_image.convert("RGBA")
            im.paste(humidity_image, (start_position[0] + 2, 170), humidity_image)

            wind_speed_image = Image.open('data//photos//wind_speed.png')
            wind_speed_image = wind_speed_image.resize((32, 32))
            wind_speed_image = wind_speed_image.convert("RGBA")
            im.paste(wind_speed_image, (start_position[0] + 6, 220), wind_speed_image)
            start_position[0] += 120
        trash_number = random.randint(1000, 9999)
        im.save(f'trash//{trash_number}.png', 'PNG')
        file_to_send = InputFile(f'trash//{trash_number}.png')
        media = types.InputMediaPhoto(media=file_to_send)
        await sec_message.edit_media(media=media)
        await sec_message.edit_caption(caption=f'<b>А вот и погода подъехала!</b>', parse_mode=ParseMode.HTML)
        os.remove(f'trash//{trash_number}.png')
        user.requestsam += 1
        session.commit()
        session.close()
    else:
        session = db_session.create_session()
        user = session.query(User).filter(user_id == User.chat_id).first()
        town = user.town
        if town is None:
            raise ValueError
        coords = get_coords(town)
        response = json.loads(requests.get(
            f'https://api.weather.yandex.ru/v1/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU&limit=7',
            headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)
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
        await bot.send_message(user-id, text_message)
        user.requestsam += 1
        session.commit()
        session.close()


def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]