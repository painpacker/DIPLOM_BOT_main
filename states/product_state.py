from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductState(StatesGroup):
    name = State()
    title = State()
    price = State()

