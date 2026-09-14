from aiogram.fsm.state import StatesGroup, State


class Replenishment(StatesGroup):
    choosingMethod = State()
