from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    tier = State()

