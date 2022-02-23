from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Узнать погоду')],
    [KeyboardButton('Сменить город')],
])
