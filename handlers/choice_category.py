from main import dp
from aiogram import types

from states.admin import Admin
from states.casheer import CasheerStates, CasheerReqStates
from utilities import *
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'choice_category', state="*")
async def edit_cat(callback: types.CallbackQuery, state: FSMContext):
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user.user_role == 'cashier':
        await callback.message.answer('Введите текст обращения',
                                      reply_markup=cancel_inline())
        await CasheerReqStates.WRITE.set()
    elif user.user_role == 'admin':
        await Admin.cat_decide.set()
        category = Category.get_by_id(int(callback.data.split()[1]))
        text = f'''{category.name}
Для изменения имени 🧾категории "Изменить"
Чтобы 🗑️ удалить 🧾категорию - "Удалить"
ℹ️ Нажмите "Отмена" для того, чтобы вернуться в главное меню'''
        await callback.message.answer(text, reply_markup=category_edit())
    await state.update_data(dict(category=callback.data.split()[1]))


@dp.callback_query_handler(text="back", state=Admin.cat_edit)
async def back(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        cat_id = data["category"]
    callback.data = f"cat {cat_id}"
    await edit_cat(callback, state)
