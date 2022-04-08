import datetime
import json

import requests

WINDOW_SIZE = (430, 200)


response = json.loads(requests.get(
            f'https://api.weather.yandex.ru/v1/forecast?lat={coords[1]}&lon={coords[0]}&lang=ru_RU&limit=7',
            headers={'X-Yandex-API-Key': WEATHER_TOKEN}).content)

        im = Image.new('RGBA', WINDOW_SIZE, color=('white'))  # #202124
        font_main = ImageFont.truetype('19755.ttf', size=15)
        font_day = ImageFont.truetype('19755.ttf', size=10)
        target_weather_conditions = ['clear', 'clear', 'rain', 'rain', 'thunderstorm-with-rain',
                                     'thunderstorm-with-rain',
                                     'showers']
        draw = ImageDraw.Draw(im)

        draw.rounded_rectangle((2, 2, WINDOW_SIZE[0] - 2, WINDOW_SIZE[1] - 2), outline="#202124",
                               width=4, radius=7)
        draw.text(xy=(80, 10),
                  text='Прогноз погоды на след неделю',
                  font=font_main,
                  fill='black',
                  align='center')
        start_position = [10, 130]

        for i in range(7):
            forecast = response['forecasts'][i]['parts']['day']
            temp_now = forecast['temp']
            feels_like = forecast['feels_like']
            condition = forecast['condition']
            wind_speed = forecast['wind_speed']
            pressure = forecast['pressure_mm']
            humidity = forecast['humidity']
            wind_gust = forecast['wind_gust']
            date = response['forecasts'][i]['date']

            time = datetime.datetime.strptime(date, '%Y-%m-%d')
            day_text = time.strftime('%A')

            condition_image = Image.open(f'data//photos//{WEATHER_CONDITIONS_URLS[condition]}')
            condition_image = condition_image.resize((48, 48))
            im.paste(condition_image, (start_position[0], start_position[1]))
            draw.rounded_rectangle((start_position[0] - 2, 50, start_position[0] + 50, 180), outline="#202124",
                                   width=2, radius=7)
            draw.text(xy=(80, 10),
                      text=day_text,
                      font=font_day,
                      fill='black',
                      align='center')
            start_position[0] += 60