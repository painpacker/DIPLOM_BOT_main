from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    name = State()
    phone = State()
    email = State()