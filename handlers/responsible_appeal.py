from main import bot, dp
from main import bot, dp
from aiogram.dispatcher import FSMContext
from handlers.functions import to_main, get_status
from utilities import *
from os import listdir


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_appeals')
async def my_appeals_requests(callback: types.CallbackQuery):
    # debug
    await bot.send_message(205479592, f'Show all appeals')
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user:
        requests = []
        if user.user_role == 'responsible_appeal' or user.user_role == 'admin':
            requests = AppealRequest.select().where(AppealRequest.status == int(callback.data.split()[1]))
        elif user.user_role == 'cashier':
            requests = AppealRequest.select().where(AppealRequest.user_id == callback.from_user.id)
        else:
            await callback.answer('❌ Ошибка!')
        if requests:
            for i in requests:

                if user.user_role != 'admin' and i.responsible and i.responsible != user.user_id:
                    continue

                category = Category.get_by_id(int(i.category))
                _user = await bot.get_chat_member(i.responsible, i.responsible) if i.responsible else None
                _user_2 = await bot.get_chat(i.user_id)
                text = f'''<b>🆔 Заявка номер {i}</b>
📃 Описание заявки: {i.text}
🧭 Статус: {get_status(i.status)}
🧾 Категория: {category.name}
👤 Ответственный: {_user['user']['first_name'] if _user else 'Не назначен'}
💡 Заявку оставил: {f'@{_user_2.username}' if _user_2.username else _user_2.first_name}'''
                await callback.message.answer(text=text, reply_markup=appeal_request_keyboard(i, user.user_role,
                                                                                       i.user_id, i.status))
            await callback.message.answer('ℹ️ Чтобы вернуться в главное меню, нажмите на кнопку отмены',
                                          reply_markup=cancel_inline())
        else:
            await callback.answer('❌ Выбранный раздел пуст', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_media_appeal_request')
async def show_media_appeal_request(callback: types.CallbackQuery, state: FSMContext):
    # debug
    await bot.send_message(205479592, f'Show media appeal')

    i = AppealRequest.get_by_id(int(callback.data.split()[1]))
    user = User.get_or_none(User.user_id == callback.from_user.id)
    category = Category.get_by_id(int(i.category))
    if user and i:
        file_list = listdir(f'images/appeal_{i}')
        if file_list:
            _user = await bot.get_chat_member(i.responsible, i.responsible) if i.responsible else None
            await callback.message.answer('ℹ️ Заявка формируется для отображения . . .')
            text = f'''<b>🆔 Заявка номер {i}</b>
📃 Описание заявки: {i.text}
🧭 Статус: {get_status(i.status)}
🧾 Категория: {category.name}
👤 Ответственный: {_user['user']['first_name'] if _user else 'Не назначен'}'''
            media = types.MediaGroup()
            for file in file_list:
                if '.mp4' in file:
                    media.attach_video(types.InputFile(f'images/appeal_{i}/{file}'), caption=text if file[0] == '0' else '')
                else:
                    media.attach_photo(types.InputFile(f'images/appeal_{i}/{file}'), caption=text if file[0] == '0' else '')
            await bot.send_media_group(callback.from_user.id, media=media)
            callback_btn = 'show_appeals' if user.user_role == 'cashier' else f'show_appeals {i.status}'
            await callback.message.answer('↩️ Чтобы вернуться назад, нажмите на кнопку ниже',
                                          reply_markup=back_inline(callback_btn))
        else:
            await callback.message.answer(f'ℹ️ У заявки №{i.id} нету медиа-файлов', reply_markup=cancel_inline())
    else:
        await callback.answer('❌ Ошибка', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'delete_appeal')
async def delete_appeal_request(callback: types.CallbackQuery, state: FSMContext):
    appeal = AppealRequest.get_by_id(int(callback.data.split()[1]))
    if appeal:
        await to_main(callback.message, state, callback.from_user, _text=f'🗑️ Вы удалили заявку №{appeal.id}')
        appeal.delete_instance()
    else:
        await callback.answer('❌ Ошибка! Заявка не найдена')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'req_appeal_change_status')
async def request_appeal_change_status(callback: types.CallbackQuery, state: FSMContext):
    appeal = AppealRequest.get_by_id(int(callback.data.split()[1]))
    if appeal:
        if int(callback.data.split()[2]) != 2:
            await callback.message.answer('ℹ️ Чтобы перенести заявку в работу, выберите ответственного за эту заявку',
                                          reply_markup=edit_checklists_kb(
                                              User.select().where(User.user_role == 'responsible_appeal'),
                                              'set_appeal_resp_for_req'))
            await state.update_data(dict(request=appeal, status=int(callback.data.split()[2])))
        else:
            appeal.status = 2
            appeal.save()
            await bot.send_message(appeal.user_id, f'ℹ️ Вашей заявке с №{appeal.id} поменяли статус на '
                                                    f'{get_status(appeal.status)}')
            await bot.send_message(appeal.responsible, f'ℹ️ Вы поменяли статус заявке №{appeal.id}'
                                                    f' на {get_status(appeal.status)}\n')
            user = User.get_or_none(User.user_id == appeal.responsible)
            if user.user_role == 'responsible_appeal':
                text = '''<b>📑 Главное меню</b>
            Для того, чтобы просмотреть новые заявки, нажмите на кнопку "На рассмотрении"'''
                await bot.send_message(user.user_id, text + '\n' + text, reply_markup=responsible_keyboard())
            elif user.user_role == 'clerk':
                text = '''<b>📑 Главное меню</b>
            Для того, чтобы просмотреть свои задачи, нажмите на кнопку "Мои задачи"'''
                await bot.send_message(user.user_id, text + '\n' + text, reply_markup=clerk_keyboard())
            elif user.user_role == 'resp_clerk':
                text = '''<b>📑 Главное меню</b>
            Для того, чтобы просмотреть 🎯 задачи пользователей, нажмите на кнопку "Чек-листы"'''
                await bot.send_message(user.user_id, text + '\n' + text, reply_markup=resp_clerk_kb())
            elif user.user_role == 'admin':
                text = '''<b>Административное меню</b>
            Здесь Вы можете отредактировать 🏬 филиалы, 🧾 категории,  назначить 🔑 роль пользователям или составить 📑 чек-листы'''
                await bot.send_message(user.user_id, text + '\n' + text, reply_markup=admin_keyboard())
    else:
        await callback.answer('❌ Ошибка! Заявка не найдена')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'set_appeal_resp_for_req')
async def set_appeal_responsible_for_request(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    appeal = data['request']
    appeal.status = data['status']
    appeal.responsible = int(callback.data.split()[1])
    appeal.save()
    user = await bot.get_chat_member(int(callback.data.split()[1]), int(callback.data.split()[1]))
    await bot.send_message(appeal.user_id, f'ℹ️ Вашей заявке с №{appeal.id} поменяли статус на '
                                            f'{get_status(appeal.status)}, ей займется {user["user"]["first_name"]}')
    await to_main(callback.message, state, callback.from_user,
                  _text=f'ℹ️ Вы поменяли статус заявке №{appeal.id} и назначили {user["user"]["first_name"]}'
                        f' ответственным на {get_status(appeal.status)}\n')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_types_appeals_requests')
async def show_types_appeals_requests(callback: types.CallbackQuery):
    text = '''<b>🧾 Обращения</b>
Здесь вы можете посмотреть: 
Новые заявки <b>"⌛ На рассмотрении"</b>
Заявки в работе <b>"🔧 В работе"</b>
Историю заявок <b>✅ Завершенные</b>'''
    await callback.message.answer(text, reply_markup=responsible_appeal_requests_keyboard())


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_checklists')
async def show_checklists(callback: types.CallbackQuery):
    branches = Branch.select()
    await callback.message.answer('Выберите филиал, в котором хотите просмотреть чек-листы',
                                  reply_markup=branches_keyboard(branches, 'resp_choice_branch'))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'resp_choice_branch')
async def resp_choice_branch(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(dict(resp_choice_branch=int(callback.data.split()[1])))
    tasks = BranchesTasks.select()
    dates = []
    for task in tasks:
        if task.date not in dates:
            dates.append(task.date)
    print(dates)
    await callback.message.answer('Выберите дату, за которую хотите просмотреть чек-листы открытия/закрытия филиалов',
                                  reply_markup=resp_checklists_kb(dates, 'resp_choice_date'))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'resp_choice_date')
async def resp_choice_date(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(dict(resp_choice_date=callback.data.split()[1]))
    await callback.message.answer('Выберите действие, которое хотите просмотреть. Открытие / Закрытие',
                                  reply_markup=open_close_kb('resp_choice_do'))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'resp_choice_do')
async def resp_choice_do(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_close = True if callback.data.split()[1] == 'True' else False
    tasks = BranchesTasks.select().where(BranchesTasks.branch_id == data['resp_choice_branch']). \
        where(BranchesTasks.is_close == is_close). \
        where(BranchesTasks.date == data['resp_choice_date'])
    for task in tasks:
        text = f'''🏷️ Название задания: {task.checklist_id.name}
Статус: {"✅ Выполнено" if task.status else "❌ Не выполнено"}'''
        if task.photo:
            await callback.message.answer_photo(task.photo, text)
        else:
            await callback.message.answer(text)
