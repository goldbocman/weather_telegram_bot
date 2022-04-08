from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('\U0001F464 Профиль')],
    [KeyboardButton('\U0001F326 Узнать погоду'), KeyboardButton('\U0001F3D9 Сменить город')],
    [KeyboardButton('\U0001F326 Красивая погода')],
])
