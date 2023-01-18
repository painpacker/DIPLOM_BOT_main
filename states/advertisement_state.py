from aiogram.dispatcher.filters.state import StatesGroup, State


class AdvertisementState(StatesGroup):
    name = State()
    title = State()
    price = State()
    url = State()
