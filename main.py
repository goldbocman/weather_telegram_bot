import logging

from aiogram import types

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from loader import dp, scheduler
from config import ADMINS
from data import db_session
from forms.weather import WeatherNotifications
import handlers
import asyncio

from tools.send_message_notification import send_message_notification


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
    await process_send_weather_notifications()
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def process_send_weather_notifications():
    session = db_session.create_session()
    all_users = session.query(WeatherNotifications).filter(WeatherNotifications.is_enable == 1).all()
    ok_sent = 0
    for user in all_users:
        user.hours_remain -= 1
        if user.hours_remain == 0:
            asyncio.create_task(send_message_notification(user_id=user.user_id, type_notification=user.ntype))
            ok_sent += 1
            user.hours_remain = user.period
        session.commit()
        if ok_sent % 15 == 0:
            await asyncio.sleep(1)


scheduler.add_job(process_send_weather_notifications, 'cron', hour='0-23')


if __name__ == '__main__':
    db_session.global_init('db/user.sqlite')
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)