from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ChatType, ParseMode, InputFile
from forms.user import User
from data import db_session
from forms.weather import WeatherNotifications
from tools.get_user_notifications import get_user_notifications
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import NOTIFICATIONS_WEATHER_MENU_MESSAGE
from loader import dp, bot


@dp.callback_query_handler(text='switch_notifications')
async def switch_notifications_handler(call: types.CallbackQuery):
    session = db_session.create_session()
    if session.query(User).filter(call.message.chat.id == User.chat_id).first() is None:
        await bot.send_message(call.message.chat.id, "Добрый день. Введи команду /start")
        return
    user_notifications = await get_user_notifications(call.message.chat.id, session=session)
    notifications_status = user_notifications.is_enable
    if notifications_status:
        user_notifications.is_enable = False
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Уведомления отключены')
    else:
        user_notifications.is_enable = True
        if user_notifications.period is None:
            user_notifications.period = 1
        if user_notifications.ntype is None:
            user_notifications.ntype = 1
        user_notifications.hours_remain = user_notifications.period
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Уведомления включены')
    session.commit()
    session.close()
