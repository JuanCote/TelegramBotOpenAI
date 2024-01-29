from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    choosing_location = State()
    checklist_1 = State()
    checklist_2 = State()
    checklist_3 = State()
    checklist_4 = State()
    checklist_5 = State()
