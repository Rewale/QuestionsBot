from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationSG(StatesGroup):
    start = State()
    phone = State()
    error = State()  # Ботом могут пользоваться только СТП
