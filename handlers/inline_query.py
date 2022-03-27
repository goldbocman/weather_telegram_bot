import json
import re

import requests
from aiogram.types import InlineQueryResultArticle, InlineKeyboardMarkup, InputTextMessageContent, InlineKeyboardButton, \
    InlineQuery, ParseMode

from config import WEATHER_TOKEN
from loader import dp, bot
from tools.geocode import get_coords
from config import GET_WEATHER_MESSAGE


@dp.inline_handler()  # Обработчик любых инлайн-запросов
async def inline(query: InlineQuery):
    try:
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
        text_message = GET_WEATHER_MESSAGE.replace('%town%', str(town))
        text_message = text_message.replace('%forecast%', str(forecast))
        text_message = text_message.replace('%temp_now%', str(temp_now))
        text_message = text_message.replace('%feels_like%', str(feels_like))
        text_message = text_message.replace('%pressure%', str(pressure))
        text_message = text_message.replace('%humidity%', str(humidity))
        text_message = text_message.replace('%wind_speed%', str(wind_speed))
        text_message = text_message.replace('%wind_gust%', str(wind_gust))
        query_answer = InlineQueryResultArticle(
            id='1', title="Погода",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description=f"Узнать погоду города: {town}",
            input_message_content=InputTextMessageContent(
                message_text=text_message, parse_mode=ParseMode.HTML)
        )
        await query.answer([query_answer])
    except Exception as ex:
        query_answer = InlineQueryResultArticle(
            id='1', title="Ошибка",
            # Описание отображается в подсказке,
            # message_text - то, что будет отправлено в виде сообщения
            description=f"Проверьте корректность названия города",
            input_message_content=InputTextMessageContent(
                message_text=f"<b>Что-то пошло не так. Проверьте корректность названия города</b>",
                parse_mode=ParseMode.HTML),
        )
        await query.answer([query_answer])

    # hint = "Введите ровно 2 числа и получите результат!"
    # try:
    #     m_sum = int(num1) + int(num2)
    #     r_sum = InlineQueryResultArticle(
    #         id='1', title="Сумма",
    #         # Описание отображается в подсказке,
    #         # message_text - то, что будет отправлено в виде сообщения
    #         description="Результат: {!s}".format(m_sum),
    #         input_message_content=InputTextMessageContent(
    #             message_text="{!s} + {!s} = {!s}".format(num1, num2, m_sum))
    #     )
    #     await query.answer([r_sum])
    #     # bot.answer_inline_query(query.id, [r_sum])
    # except Exception as e:
    #     print(e)
    # text = query.query or None
    # if text == None:
    #     await query.answer([])
    #     return
    #
    # thumb_url = 'https://media.lpgenerator.ru/uploads/2019/07/11/1_thumb600x460.jpg'
    # items = [InlineQueryResultArticle(
    #     id='2131',
    #     title='Название',
    #     description='Описание',
    #     thumb_url=thumb_url,
    #     input_message_content=InputTextMessageContent(f'<a href="{thumb_url}">-</a>', parse_mode="HTML"),
    #     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Текст', callback_data='data'))
    # )]
    # await query.answer(items)