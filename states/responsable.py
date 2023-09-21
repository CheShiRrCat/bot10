from aiogram.dispatcher.filters.state import State, StatesGroup


class RespStates(StatesGroup):
    REP_MENU = State()
    REQ_MENU = State()
    SELECT_BRANCH = State()
    SEND_DATE = State()
    REP_EDIT = State()
    REQ_EDIT = State()
