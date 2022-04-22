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


@dp.message_handler(text='\U0001F514 Уведомления')
async def get_notifications(message: types.Message):
    session = db_session.create_session()
    if session.query(User).filter(message.from_user.id == User.chat_id).first() is None:
        await bot.send_message(message.from_user.id, "Добрый день. Введи команду /start")
        return
    user_notifications = await get_user_notifications(message.from_user.id, session=session)
    notifications_status = user_notifications.is_enable
    notifications_period = user_notifications.period
    notifications_type = user_notifications.ntype

    notifications_inline_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('\U000023F0 Изменить пероид отправки', callback_data='change_period_notifications')
        ],
        [
            InlineKeyboardButton('\U0001F4D2 Изменить тип уведомления', callback_data='change_type_notifications')
        ]
    ])

    if notifications_status:
        notifications_inline_menu.add(
            InlineKeyboardButton(text='\U0001F515 Отключить уведомления', callback_data='switch_notifications')
        )
    else:
        notifications_inline_menu.add(
            InlineKeyboardButton(text='\U0001F514 Включить уведомления', callback_data='switch_notifications')
        )

    notifications_status = 'Включены' if notifications_status else 'Выключены'

    if notifications_period is None:
        notifications_period = 'Не выбрано'
    else:
        notifications_period = f'Кажды(е/й) <b>{notifications_period}</b>ч.'
    
    notifications_type = 'На день' if notifications_type == 0 else 'На неделю'
    text_message = NOTIFICATIONS_WEATHER_MENU_MESSAGE.replace('%notifications_status%', notifications_status)
    text_message = text_message.replace('%notifications_period%', notifications_period)
    text_message = text_message.replace('%notifications_type%', notifications_type)
    await bot.send_message(message.from_user.id, text=text_message, parse_mode=ParseMode.HTML,
                           reply_markup=notifications_inline_menu)