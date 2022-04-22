from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('\U0001F464 Профиль')],
    [KeyboardButton('\U0001F514 Уведомления'), KeyboardButton('\U0001F3D9 Сменить город')],
    [KeyboardButton('\U0001F326 Узнать погоду'), KeyboardButton('\U0001F326 Красивая погода')],
])

notifications_inline_menu_type = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('\U000023F0 На день', callback_data='change_type_notifications_day')
    ],
    [
        InlineKeyboardButton('\U0001F4D2 На неделю', callback_data='change_type_notifications_week')
    ]
])

notifications_inline_menu_period = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Час', callback_data='set_notifications_period_1')
    ],
    [
        InlineKeyboardButton('Два часа', callback_data='set_notifications_period_2')
    ],
    [
        InlineKeyboardButton('Четыре часа', callback_data='set_notifications_period_4')
    ],
    [
        InlineKeyboardButton('12 часов', callback_data='set_notifications_period_12')
    ],
    [
        InlineKeyboardButton('24 часа', callback_data='set_notifications_period_24')
    ]
])