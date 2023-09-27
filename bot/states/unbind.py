from aiogram.fsm.state import StatesGroup, State


class Unbind(StatesGroup):
    confirming = State()
    awaitingCode = State()
