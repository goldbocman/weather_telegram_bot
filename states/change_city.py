from aiogram.dispatcher.filters.state import StatesGroup, State


class CityChanger(StatesGroup):
    Q_CITY_NAME = State()
