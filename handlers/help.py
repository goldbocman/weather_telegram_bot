from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import ChatType, ParseMode
from loader import dp, bot


@dp.message_handler(CommandHelp(), chat_type=ChatType.PRIVATE)
async def bot_help(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Это справка. У нашего бота есть функции: \n"
                         f"1) Получение погоды на текущий день\n"
                         f"2) Получение погоды на будущее(максимум - 6 дней)\n"
                         f"3) Запланировать получение погоды каждый определённый промежуток времени(минимум - день, максимум - месяц)\n\n"
                         f"<b>Схема использования бота:</b>\n\n"
                         f"‣ Сперва выберите свой город с помощью кнопки\n"
                         f"<b> \U0001F3D9 Сменить город </b>. По умолчанию выбрана Москва.\n\n"
                         f"‣ Далее можете нажать кнопку \n"
                         f"<b> \U0001F326 Узнать погоду </b>. Бот отправит вам погоду на сегодняшний день", parse_mode=ParseMode.HTML)
