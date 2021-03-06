from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ChatType
from forms.user import User
from forms.weathernotifications import WeatherNotifications
from data import db_session

from loader import dp, bot
from keyboards import start_keyboard


@dp.message_handler(commands=['start_notification'])
async def start_notification(message: types.Message):
    hours = 1

    session = db_session.create_session()
    if session.query(User).filter(message.from_user.id == User.chat_id).first() is None:
        await bot.send_message(message.from_user.id, "Добрый день. Введи команду /start")
        return
    user = session.query(User).filter(message.from_user.id == User.chat_id).first()
    town = user.town
    user_notifications = await get_user_notifications(message_user_id=message.from_user.id, session=session)
    user_notifications.hours_remain = hours
    user_notifications.is_enable = True
    session.commit()
    session.close()
    await bot.send_message(
        message.from_user.id,
        f"Вам теперь будет отправлятся рассылка погоды города <b>{town}</b> каждые <b>{hours}</b>ч.")


async def get_user_notifications(message_user_id: int, session):
    if session.query(WeatherNotifications).filter(message_user_id == WeatherNotifications.user_id).first() is None:
        user_notifications = WeatherNotifications()
        user_notifications.user_id = message_user_id
    else:
        user_notifications = session.query(WeatherNotifications).filter(message_user_id == WeatherNotifications.user_id).first()
    return user_notifications
