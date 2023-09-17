from main import dp
from aiogram import types
from utilities import *
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'choice_category')
async def create_appeal(callback: types.CallbackQuery, state: FSMContext):
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user.user_role == 'cashier':
        await callback.message.answer('Введите текст обращения',
                                      reply_markup=cancel_inline())
        await state.set_state(Cashier.enter_text_category)
    elif user.user_role == 'admin':
        category = Category.get_by_id(int(callback.data.split()[1]))
        text = f'''{category.name}
Для изменения имени 🧾категории "Изменить"
Чтобы 🗑️ удалить 🧾категорию - "Удалить"
ℹ️ Нажмите "Отмена" для того, чтобы вернуться в главное меню'''
        await callback.message.answer(text, reply_markup=category_edit())
    await state.update_data(dict(category=callback.data.split()[1]))
