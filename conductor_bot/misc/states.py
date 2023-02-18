from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    user_in_system = State()
