import logging
from aiogram import types

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from loader import dp, scheduler
from config import ADMINS
from data import db_session
from forms.weathernotifications import WeatherNotifications
import handlers
import asyncio


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
        except Exception as err:
            logging.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("start_notification", "Установить таймер (не готово)"),
        ]
    )


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def process_send_weather_notifications():
    session = db_session.create_session()
    all_users = session.query(WeatherNotifications).all()
    print(all_users)


# scheduler.add_job(process_send_weather_notifications, 'interval', minutes=5)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)