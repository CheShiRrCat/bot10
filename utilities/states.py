from aiogram.dispatcher.filters.state import State, StatesGroup


class Cashier(StatesGroup):
    choice_branch = State()
    choice_category = State()
    enter_text = State()
    enter_text_category = State()
    enter_attach = State()
    enter_attach_category = State()
    set_price = State()

    edit_task_photo = State()


class Admin(StatesGroup):
    edit_branch = State()
    edit_category = State()
    set_category_resp = State()
    edit_user = State()
    edit_task_for_clerk = State()
    edit_new_category_resp = State()

    add_checklist = State()
    change_checklist = State()
    change_photo = State()
