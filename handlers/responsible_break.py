from main import bot, dp
from main import bot, dp
from aiogram.dispatcher import FSMContext
from handlers.functions import to_main, get_status
from utilities import *
from os import listdir


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_requests')
async def my_requests(callback: types.CallbackQuery):
    # debug
    await bot.send_message(205479592, f'Show all requests')
    user = User.get_or_none(User.user_id == callback.from_user.id)
    if user:
        requests = []
        if user.user_role == 'responsible' or user.user_role == 'responsible_break' or user.user_role == 'admin':
            requests = Request.select().where(Request.status == int(callback.data.split()[1]))
        elif user.user_role == 'cashier':
            requests = Request.select().where(Request.user_id == callback.from_user.id)
        else:
            await callback.answer('❌ Ошибка!')
        if requests:

            for i in requests[::-1]:
                branch = Branch.get_by_id(int(i.branch))
                _user = await bot.get_chat_member(i.responsible, i.responsible) if i.responsible else None
                text = f'''<b>🆔 Заявка номер {i}</b>
📃 Описание заявки: {i.text}
🧭 Статус: {get_status(i.status)}
🏬 Филиал: {branch.name}
👤 Ответственный: {_user['user']['first_name'] if _user else 'Не назначен'}
{f"💵 Цена: {i.price}" if i.status == 2 else ""}'''
                await callback.message.answer(text=text, reply_markup=request_keyboard(i, user.user_role,
                                                                                       i.user_id, i.status))
            await callback.message.answer('ℹ️ Чтобы вернуться в главное меню, нажмите на кнопку отмены',
                                          reply_markup=cancel_inline())
        else:
            await callback.answer('❌ Выбранный раздел пуст', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_media_request')
async def show_media_request(callback: types.CallbackQuery, state: FSMContext):
    # debug
    await bot.send_message(205479592, f'Show media request')

    i = Request.get_by_id(int(callback.data.split()[1]))
    user = User.get_or_none(User.user_id == callback.from_user.id)
    branch = Branch.get_by_id(int(i.branch))
    if user and i:
        file_list = listdir(f'images/{i}')
        if file_list:
            _user = await bot.get_chat_member(i.responsible, i.responsible) if i.responsible else None
            await callback.message.answer('ℹ️ Заявка формируется для отображения . . .')
            text = f'''<b>🆔 Заявка номер {i}</b>
📃 Описание заявки: {i.text}
🧭 Статус: {get_status(i.status)}
🏬 Филиал: {branch.name}
👤 Ответственный: {_user['user']['first_name'] if _user else 'Не назначен'}
{f"💵 Цена: {i.price}" if i.status == 2 else ""}'''
            media = types.MediaGroup()
            for file in file_list:
                if '.mp4' in file:
                    media.attach_video(types.InputFile(f'images/{i}/{file}'), caption=text if file[0] == '0' else '')
                else:
                    media.attach_photo(types.InputFile(f'images/{i}/{file}'), caption=text if file[0] == '0' else '')
            await bot.send_media_group(callback.from_user.id, media=media)
            callback_btn = 'show_requests' if user.user_role == 'cashier' else f'show_requests {i.status}'
            await callback.message.answer('↩️ Чтобы вернуться назад, нажмите на кнопку ниже',
                                          reply_markup=back_inline(callback_btn))
        else:
            await callback.message.answer(f'ℹ️ У заявки №{i.id} нету медиа-файлов', reply_markup=cancel_inline())
    else:
        await callback.answer('❌ Ошибка', show_alert=True)


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'delete')
async def delete_request(callback: types.CallbackQuery, state: FSMContext):
    request = Request.get_by_id(int(callback.data.split()[1]))
    if request:
        await to_main(callback.message, state, callback.from_user, _text=f'🗑️ Вы удалили заявку №{request.id}')
        request.delete_instance()
    else:
        await callback.answer('❌ Ошибка! Заявка не найдена')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'req_change_status')
async def request_change_status(callback: types.CallbackQuery, state: FSMContext):
    request = Request.get_by_id(int(callback.data.split()[1]))
    if request:
        if int(callback.data.split()[2]) != 2:
            await callback.message.answer('ℹ️ Чтобы перенести заявку в работу, выберите ответственного за эту заявку',
                                          reply_markup=edit_checklists_kb(
                                              (User.select().where(User.user_role == 'responsible') + User.select().where(User.user_role == 'responsible_break')),
                                              'set_resp_for_req'))
            await state.update_data(dict(request=request, status=int(callback.data.split()[2])))
        else:
            await callback.message.answer('Введите цену, за которую Вы выполнили заявку')
            await state.update_data(dict(req_id=int(callback.data.split()[1])))
            await state.set_state(Cashier.set_price)
    else:
        await callback.answer('❌ Ошибка! Заявка не найдена')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'set_resp_for_req')
async def set_responsible_for_request(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    request = data['request']
    request.status = data['status']
    request.responsible = int(callback.data.split()[1])
    request.save()
    user = await bot.get_chat_member(int(callback.data.split()[1]), int(callback.data.split()[1]))
    await bot.send_message(request.user_id, f'ℹ️ Вашей заявке с №{request.id} поменяли статус на '
                                            f'{get_status(request.status)}, ей займется {user["user"]["first_name"]}')
    await to_main(callback.message, state, callback.from_user,
                  _text=f'ℹ️ Вы поменяли статус заявке №{request.id} и назначили {user["user"]["first_name"]}'
                        f' ответственным на {get_status(request.status)}\n')


@dp.message_handler(state=Cashier.set_price)
async def set_price_req(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        request = Request.get_by_id(data['req_id'])
        request.status = 2
        request.price = int(message.text)
        request.save()
        await bot.send_message(request.user_id, f'ℹ️ Вашей заявке с №{request.id} поменяли статус на '
                                                f'{get_status(request.status)}')
        await to_main(message, state, message.from_user, _text=f'ℹ️ Вы поменяли статус заявке №{request.id}'
                                                               f' на {get_status(request.status)}\n')
    else:
        await bot.send_message(message.from_user.id, 'Ошибка! Введите цену выполненной заявки')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'show_types_requests')
async def show_types_requests(callback: types.CallbackQuery):
    text = '''<b>🛠️ Поломки</b>
Здесь вы можете посмотреть: 
Новые заявки <b>"⌛ На рассмотрении"</b>
Заявки в работе <b>"🔧 В работе"</b>
Историю заявок <b>✅ Завершенные</b>'''
    await callback.message.answer(text, reply_markup=responsible_requests_keyboard())


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
