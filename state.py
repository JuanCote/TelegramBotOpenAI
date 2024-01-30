from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    choosing_location = State()
    checklist = State()
    comment = State()
    image = State()
