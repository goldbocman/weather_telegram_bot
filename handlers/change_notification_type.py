from aiogram import types
from aiogram.types import ChatType, ParseMode
from forms.user import User
from data import db_session

from loader import dp, bot
from states.change_city import CityChanger
from tools.get_user_notifications import get_user_notifications
from keyboards import notifications_inline_menu_type


@dp.callback_query_handler(text='change_type_notifications')
async def change_type_notifications_handler(call: types.CallbackQuery):
    session = db_session.create_session()
    if session.query(User).filter(call.message.chat.id == User.chat_id).first() is None:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Добрый день. Введи команду /start")
        return
    session.commit()
    session.close()
    user_notifications = await get_user_notifications(call.message.chat.id, session=session)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите тип уведомления',
                                reply_markup=notifications_inline_menu_type)


@dp.callback_query_handler(text='change_type_notifications_day')
async def change_type_notifications_handler_day(call: types.CallbackQuery):
    session = db_session.create_session()
    if session.query(User).filter(call.message.chat.id == User.chat_id).first() is None:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Добрый день. Введи команду /start")
        return
    user_notifications = await get_user_notifications(call.message.chat.id, session=session)
    user_notifications.ntype = 0
    session.commit()
    session.close()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Теперь вам будет присылаться прогноз на день!')


@dp.callback_query_handler(text='change_type_notifications_week')
async def change_type_notifications_handler_week(call: types.CallbackQuery):
    session = db_session.create_session()
    if session.query(User).filter(call.message.chat.id == User.chat_id).first() is None:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Добрый день. Введи команду /start")
        return
    user_notifications = await get_user_notifications(call.message.chat.id, session=session)
    user_notifications.ntype = 1
    session.commit()
    session.close()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Теперь вам будет присылаться прогноз на неделю!')

