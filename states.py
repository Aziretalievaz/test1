from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    age = State()