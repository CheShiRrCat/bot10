from aiogram.dispatcher import FSMContext

from handlers.functions import to_main, get_role_name, get_status
from main import bot, dp
from utilities import *


@dp.callback_query_handler(lambda callback: callback.data == 'adm_requests')
async def adm_requests(callback: types.CallbackQuery):
    text = '''
Здесь вы можете просмотреть заявки в работе, историю и новые заявки в разделах <b>"Поломки"</b> и <b>"Обращения"</b>'''
    await callback.message.answer(text, reply_markup=adm_resp_keyboard())


@dp.callback_query_handler(lambda callback: callback.data == 'edit_branches')
async def edit_branches(callback: types.CallbackQuery):
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user and user.user_role == 'admin':
        branches = Branch.select()
        text = f'''Выберите 🏬 филиал для редактирования или удаления
Чтобы ➕ добавить новый филиал, нажмите "Добавить"'''
        await callback.message.answer(text, reply_markup=branches_keyboard(branches, 'choice_branch', user.user_role))
    else:
        await callback.answer('❌ Ошибка!', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data == 'edit_branch')
async def edit_branches(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'branch' in data:
        text = f'''🏬 Введите новое название филиала'''
    else:
        text = f'''🏬 Введите название нового филиала'''
    await state.set_state(Admin.edit_branch)
    await callback.message.answer(text)


@dp.message_handler(state=Admin.edit_branch)
async def add_branch(message: types.Message, state: FSMContext):
    data, text = await state.get_data(), ''
    if 'branch' in data:
        branch = Branch.get_by_id(int(data['branch']))
        branch.name = message.text
        branch.save()
        text = f'✅ Вы успешно изменили название филиала на: {message.text}'
    else:
        Branch.create(name=message.text)
        text = f'✅ Вы успешно добавили новый филиал: {message.text}'
    await to_main(message, state, message.from_user, text)


@dp.callback_query_handler(lambda callback: callback.data == 'delete_branch')
async def edit_branch(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'branch' in data:
        branch = Branch.get_by_id(int(data['branch']))
        text = f'🗑️ Вы успешно удалили филиал {branch.name}'
        branch.delete_instance()
        await to_main(callback.message, state, callback.from_user, text)
    else:
        await callback.answer('❌ Ошибка! Вы не выбрали филиал', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data == 'edit_roles')
async def edit_roles(callback: types.CallbackQuery, state: FSMContext):
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user and user.user_role == 'admin':
        await state.set_state(Admin.edit_user)
        await callback.message.answer('👤 Введите логин пользователя, которому хотите назначить права'
                                      '\nℹ️ Символ @ использовать не требуется',
                                      reply_markup=cancel_inline())


@dp.message_handler(state=Admin.edit_user)
async def find_user(message: types.Message, state: FSMContext):
    user = User.get_or_none(User.username == message.text)
    if user:
        await message.answer(f'👤 Выберите роль для пользователя {user.username}\n'
                             f'🔑 Сейчас его роль - {get_role_name(user.user_role)}',
                             reply_markup=edit_roles_kb())
        await state.update_data(dict(user_to_edit=user))
    else:
        await message.answer('''❌ Данный пользователь в системе не найден
ℹ️ Возможные следующие причины:
1️⃣ Пользователь не запустил бота (/start)
2️⃣ У пользователя не указан логин
3️⃣ Пользователь изменил логин
4️⃣ Логин введён неверно''')


@dp.callback_query_handler(state=Admin.edit_user)
async def edit_roles(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = User.get_by_id(data['user_to_edit'])
    if user and callback.data.split()[0] in ['cashier', 'responsible_break', 'responsible_appeal', 'responsible',
                                             'admin']:
        user.user_role = callback.data.split()[0]
        user.save()
        await bot.send_message(user.user_id, f'🔑 Вам изменили права доступа\nЧтобы обновить меню, введите /start')
        text = f'''✅ Вы изменили роль пользователю {user.username} на {user.user_role}'''
        await to_main(callback.message, state, callback.from_user, text)
    else:
        await callback.answer('❌ Ошибка', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'edit_checklists')
async def edit_checklists(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'edit_checklists':
        text = '👤 Выберите пользователя из списка\nℹ️ Если список пуст - нет пользователей с правами клерка'
        clerks = User.select().where(User.user_role == 'clerk')
        await callback.message.answer(text, reply_markup=edit_checklists_kb(clerks, 'edit_checklists'))
    elif callback.data.split()[1].isdigit():
        clerk = User.get_or_none(User.user_id == int(callback.data.split()[1]))
        if clerk:
            tasks = Task.select().where(Task.user_id == clerk.user_id)
            for i in tasks:
                task_text = f'''🎯 Задача: {i.text}
🧭 Статус: {get_status(i.status)}
{f"Время выполнения: 📅 {i.date.day}-{i.date.month}-{i.date.year}: 🕒 {i.date.hour}-{i.date.minute}"
                if i.status == 2 else ""}'''
                await callback.message.answer(task_text, reply_markup=edit_task_kb(i.id))
            text = f'''Вы выбрали пользователя 👤 {clerk.username}
Выше Вы можете просмотреть его 🎯 задачи (если они есть)
Для того, чтобы ➕ добавить новую задачу пользователю - нажмите "Добавить"
Для ↩️ возвращения в предыдущее меню - нажмите "Назад"'''
            await callback.message.answer(text,
                                          reply_markup=add_task_and_back('edit_checklists'))
            await state.update_data(dict(selected_clerk=clerk.user_id))
        else:
            await to_main(callback.message, state, callback.from_user, '❌ Ошибка, пользователь не найден')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'add_task')  # add and edit task
async def add_task_to_clerk(callback: types.CallbackQuery, state: FSMContext):
    do = 'добавить'
    if len(callback.data.split()) == 2:
        do = 'изменить'
        await state.update_data(dict(task_id=int(callback.data.split()[1])))
    await callback.message.answer(f'ℹ️ Введите описание задачи, которую хотите {do} пользователю')
    await state.set_state(Admin.edit_task_for_clerk)


@dp.message_handler(state=Admin.edit_task_for_clerk)
async def edit_task_for_clerk(message: types.Message, state: FSMContext):
    data, text = await state.get_data(), ''
    if 'selected_clerk' in data:
        clerk = User.get_or_none(User.user_id == int(data['selected_clerk']))
        if 'task_id' not in data:
            Task.create(user_id=clerk.user_id, text=message.text, status=1)
            text = f'✅ Вы успешно создали 🎯 задачу {message.text} для 👤 пользователя {clerk.username}'
        elif 'task_id' in data:
            task = Task.get_by_id(data['task_id'])
            task.text = message.text
            task.save()
            text = f'✅ Вы успешно изменили 🎯 задачу для 👤 пользователя {clerk.username} на {message.text}'
        await bot.send_message(clerk.user_id, '📑 Ваш список задач был обновлен')
    await to_main(message, state, message.from_user, text if text else 'Ошибка')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'delete_task')
async def delete_task(callback: types.CallbackQuery, state: FSMContext):
    task = Task.get_by_id(int(callback.data.split()[1]))
    await bot.send_message(task.user_id, '📑 Ваш список задач был обновлен')
    task.delete_instance()
    await to_main(callback.message, state, callback.from_user, '🗑️ Вы успешно удалили задачу')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'checklist_branch')
async def checklist_branch(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    checklists = ChecklistTemplates.select().where(ChecklistTemplates.is_close == int(callback.data.split()[1])). \
        where(ChecklistTemplates.branch_id == int(data['branch']))
    await callback.message.answer('Выберите задание из чек-листа, которое собираетесь редактировать. Чтобы добавить '
                                  'новое задание, нажмите - "Добавить"',
                                  reply_markup=checklists_branch_kb(checklists, callback.data.split()[1]))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'add_checklist')
async def add_checklist(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название нового задания для выбранного чек-листа')
    await state.update_data(dict(is_close=int(callback.data.split()[1])))
    await state.set_state(Admin.add_checklist)


@dp.message_handler(state=Admin.add_checklist)
async def adding_checklist(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ChecklistTemplates.create(name=message.text, is_close=data['is_close'], branch_id=data['branch'])
    await to_main(message, state, message.from_user, f'Вы успешно добавили задание {message.text}')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'choice_checklist')
async def choice_checklist(callback: types.CallbackQuery, state: FSMContext):
    checklist = ChecklistTemplates.get_by_id(int(callback.data.split()[1]))
    if checklist.photo:
        await callback.message.answer_photo(checklist.photo)
    await callback.message.answer('Чтобы изменить название задания - нажмите "Изменить". Для удаления задания, '
                                  'воспользуйтесь кнопкой "Удалить"',
                                  reply_markup=edit_checklist_kb(checklist.id))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'change_checklist')
async def add_checklist(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новое название выбранного задания из чек-листа')
    await state.update_data(dict(checklist_id=int(callback.data.split()[1])))
    await state.set_state(Admin.change_checklist)


@dp.message_handler(state=Admin.change_checklist)
async def change_checklist(message: types.Message, state: FSMContext):
    data = await state.get_data()
    checklist = ChecklistTemplates.get_by_id(data['checklist_id'])
    await to_main(message, state, message.from_user, f'Вы успешно изменили название для задания {checklist.name} на '
                                                     f'{message.text}')
    checklist.name = message.text
    checklist.save()


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'delete_checklist')
async def delete_checklist(callback: types.CallbackQuery, state: FSMContext):
    checklist = ChecklistTemplates.get_by_id(int(callback.data.split()[1]))
    await to_main(callback.message, state, callback.from_user, f'Вы удалили задание {checklist.name}')
    checklist.delete_instance()


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'photo_checklist')
async def photo_checklist(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте фотографию для выбранного чек-листа', reply_markup=delete_kb())
    await state.update_data(dict(checklist_id=int(callback.data.split()[1])))
    await state.set_state(Admin.change_photo)


@dp.message_handler(state=Admin.change_photo, content_types=['photo', 'text'])
async def change_photo(message: types.Message, state: FSMContext):
    if message.photo or message.text == 'Удалить':
        data = await state.get_data()
        checklist = ChecklistTemplates.get_by_id(data['checklist_id'])
        checklist.photo = message.photo[-1].file_id if message.text != "Удалить" else ""
        checklist.save()
        await to_main(message, state, message.from_user, f'Вы успешно изменили фото для задания {checklist.name}')
    else:
        await message.answer('Отправьте фотографию для выбранного чек-листа', reply_markup=delete_kb())


@dp.callback_query_handler(lambda callback: callback.data == 'edit_categories')
async def edit_categories(callback: types.CallbackQuery):
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user and user.user_role == 'admin':
        category = Category.select()
        text = f'''Выберите 🧾 категорию для редактирования или удаления
Чтобы ➕ добавить новую 🧾 категорию, нажмите "Добавить"'''
        await callback.message.answer(text,
                                      reply_markup=categories_keyboard(category, 'choice_category', user.user_role))
    else:
        await callback.answer('❌ Ошибка!', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data == 'edit_category')
async def edit_categories(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'category' in data:
        await callback.message.answer(
            'Вы можете поменять имя, или назначить ответственного по умолчанию для текущей категории',
            reply_markup=category_edit_type())
    else:
        text = f'''🧾 Введите название новой категории'''
        await state.set_state(Admin.edit_category)
        await callback.message.answer(text)


@dp.callback_query_handler(lambda callback: callback.data == 'change_category_responsible')
async def edit_categories(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'category' in data:
        category = Category.get_by_id(int(data['category']))
        responsible_id = category.responsible
        print(responsible_id)
        if responsible_id is None:
            responsible = 'Отсутствует'
        else:
            responsible = 'Отсутствует'
            for i in User.select().where(User.user_id == int(responsible_id)):
                responsible = f'@{i.username}'
        await callback.message.answer(f'👤 Выберите ответственного по умолчанию для категории <b>"{category.name}"</b>\n'
                                      f'Ответственный на данный момент: <b>"{responsible}"</b>',
                                      reply_markup=edit_checklists_kb(
                                          (User.select().where(User.user_role == 'responsible') + User.select().where(
                                              User.user_role == 'responsible_appeal')),
                                          'set_resp_for_cat'))
    else:
        await callback.message.answer('❌ Ошибка! Не выбрана категория!')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'set_resp_for_cat')
async def set_responsible_for_category(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'category' in data:
        category = Category.get_by_id(int(data['category']))
        category.responsible = int(callback.data.split()[1])
        category.save()
        user = await bot.get_chat_member(int(callback.data.split()[1]), int(callback.data.split()[1]))
        await bot.send_message(category.responsible,
                               f'ℹ️ Вас назначили ответственным за категорию <b>"{category.name}"</b>')
        await to_main(callback.message, state, callback.from_user,
                      _text=f'ℹ️ Вы назначили категории <b>{category.name}</b> нового ответственного: <b>"{user["user"]["first_name"]}"</b>')

    else:
        await callback.message.answer('❌ Ошибка! Не выбрана категория!')


# category_edit_type
@dp.callback_query_handler(lambda callback: callback.data == 'change_category_name')
async def edit_categories(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'category' in data:
        text = f'''🧾 Введите новое название категории'''
    else:
        text = f'''🧾 Введите название новой категории'''
    await state.set_state(Admin.edit_category)
    await callback.message.answer(text)


@dp.message_handler(state=Admin.edit_category)
async def add_category(message: types.Message, state: FSMContext):
    data, text = await state.get_data(), ''
    if 'category' in data:
        category = Category.get_by_id(int(data['category']))
        category.name = message.text
        category.save()
        text = f'✅ Вы успешно изменили название 🧾 категории на: {message.text}'
        await to_main(message, state, message.from_user, text)
    else:
        category = Category.create(name=message.text)
        await state.reset_state(with_data=True)
        text = f'✅ Вы успешно добавили новую 🧾 категорию: {message.text}\n' \
               f'Теперь необходимо назначить ответственного за данную категорию'
        data['category'] = category
        await message.answer(text, reply_markup=edit_checklists_kb(
            (User.select().where(User.user_role == 'responsible') + User.select().where(
                User.user_role == 'responsible_appeal')),
            f'set_resp_for_new_cat {category}'))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'set_resp_for_new_cat')
async def set_resp_for_new_cat(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data.split())
    category = Category.get_by_id(callback.data.split()[1])
    category.responsible = int(callback.data.split()[2])
    category.save()
    user = await bot.get_chat_member(int(callback.data.split()[2]), int(callback.data.split()[2]))
    await bot.send_message(category.responsible,
                           f'ℹ️ Вас назначили ответственным за категорию <b>"{category.name}"</b>')
    await to_main(callback.message, state, callback.from_user,
                  _text=f'ℹ️ Вы назначили категории <b>{category.name}</b> нового ответственного: <b>"{user["user"]["first_name"]}"</b>')


@dp.callback_query_handler(lambda callback: callback.data == 'delete_category')
async def delete_category(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'category' in data:
        category = Category.get_by_id(int(data['category']))
        text = f'🗑️ Вы успешно удалили 🧾 категорию {category.name}'
        category.delete_instance()
        await to_main(callback.message, state, callback.from_user, text)
    else:
        await callback.answer('❌ Ошибка! Вы не выбрали филиал', show_alert=True)
