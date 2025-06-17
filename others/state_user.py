from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    state_name = State()
    state_date = State()
    state_time = State() 
    state_service = State()
    state_add_service = State()
    state_get_phone = State()
    hand_enter_number = State()
    