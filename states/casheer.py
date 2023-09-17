from aiogram.dispatcher.filters.state import State, StatesGroup


class CasheerStates(StatesGroup):
    MAIN_MENU = State()


class CasheerRepStates(StatesGroup):
    REP_MENU = State()
    SELECT_BRANCH = State()
    WRITE = State()
    PHOTO = State()
    MY_REQUESTS = State()


class CasheerReqStates(StatesGroup):
    REQ_MENU = State()
    SELECT_THEME = State()
    WRITE = State()
    PHOTO = State()
    MY_REQUESTS = State()
