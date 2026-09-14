from aiogram.fsm.state import StatesGroup, State


class List(StatesGroup):
    choosingType = State()
    viewing = State()
    viewingOrder = State()
    viewingAdditionalInfo = State()
