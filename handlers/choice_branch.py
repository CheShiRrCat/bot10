from main import dp
from aiogram import types
from utilities import *
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'choice_branch')
async def create_request(callback: types.CallbackQuery, state: FSMContext):
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user.user_role == 'cashier':
        await callback.message.answer('📝 Расскажите более подробно про обнаруженную техническую неполадку',
                                      reply_markup=cancel_inline())
        await state.set_state(Cashier.enter_text)
    elif user.user_role == 'admin':
        branch = Branch.get_by_id(int(callback.data.split()[1]))
        text = f'''{branch.name}
Для изменения названия 🏬 филиала нажмите "Изменить"
Чтобы 🗑️ удалить филиал - "Удалить"
ℹ️ Нажмите "Отмена" для того, чтобы вернуться в главное меню'''
        await callback.message.answer(text, reply_markup=branch_edit())
    await state.update_data(dict(branch=callback.data.split()[1]))
