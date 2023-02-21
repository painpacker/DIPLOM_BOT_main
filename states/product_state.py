from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductState(StatesGroup):
    product = State()
    name = State()
    title = State()
    price = State()
    contact = State()
    name_2 = State()
    title_2 = State()
    price_2 = State()
    contacts_2 = State()


