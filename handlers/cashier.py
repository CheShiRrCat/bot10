import datetime
import types

from main import dp, bot
from handlers.functions import to_main, get_status
from aiogram.dispatcher import FSMContext
from utilities import *
from typing import List
import os


@dp.callback_query_handler(lambda callback: callback.data == 'cancel', state=['*'])
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await to_main(callback.message, state, callback.from_user, 'ℹ️ Вы вернулись в главное меню\n')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'create_request')
async def create_request(callback: types.CallbackQuery):
    branches = Branch.select()
    await callback.message.answer('🏬 Выберите филиал среди предложенных ниже',
                                  reply_markup=branches_keyboard(branches, 'choice_branch'))


@dp.message_handler(state=Cashier.enter_text_category)
async def enter_text_category(message: types.Message, state: FSMContext):
    await message.answer(f'📸 Отлично! Теперь прикрепите медиа, если это необходимо', reply_markup=next_step())
    await state.set_state(Cashier.enter_attach_category)
    await state.update_data(dict(req_text=message.text))


@dp.message_handler(state=Cashier.enter_text)
async def enter_text(message: types.Message, state: FSMContext):
    await message.answer(f'📸 Отлично! Теперь отправьте фото или видео доказательства', reply_markup=next_step())
    await state.set_state(Cashier.enter_attach)
    await state.update_data(dict(req_text=message.text))


@dp.message_handler(state=Cashier.enter_attach, content_types=types.ContentType.ANY)
async def handle_albums(message: types.Message, state: FSMContext, album: List[types.Message] = None):
    await message.answer('ℹ️ Заявка в процессе создания . . .')
    data = await state.get_data()
    request = Request.create(user_id=message.from_user.id,
                             text=data['req_text'],
                             branch=data['branch'],
                             status=0)
    os.mkdir(f'images/{request.id}')
    image_urls = []
    if album:
        for i, item in enumerate(album):
            if 'photo' in item:
                url = f'images/{request.id}/{i}.jpg'
                image_urls.append(url)
                await item.photo[-1].download(destination_file=url)
            if 'video' in item:
                url = f'images/{request.id}/{i}.mp4'
                file = await bot.get_file(item.video.file_id)
                await bot.download_file(file.file_path, url)
                image_urls.append(url)
    else:
        if 'photo' in message:
            url = f'images/{request.id}/0.jpg'
            image_urls.append(url)
            await message.photo[-1].download(destination_file=url)
        if 'video' in message:
            url = f'images/{request.id}/0.mp4'
            file = await bot.get_file(message.video.file_id)
            await bot.download_file(file.file_path, url)
            image_urls.append(url)
    request.image = str(image_urls)
    request.save()
    await to_main(message, state, message.from_user,
                  f'''✅ Вы успешно оставили заявку 🆔{request.id}, о 🛠️ технической неполадке
⏳ В ближайшее время наши специалисты займутся Вашим обращением
🧭 Посмотреть статус данной заявки Вы можете в разделе "Мои заявки"''')
    users = User.select().where(User.user_role == 'responsible')
    users += User.select().where(User.user_role == 'admin')
    for i in users:
        branch = Branch.get_by_id(int(data['branch']))
        text = f'''<b>🆔 Заявка номер {request}</b>
📃 Описание заявки: {request.text}
🧭 Статус: {get_status(request.status)}
🏬 Филиал: {branch.name}
👤 Ответственный: Не назначен'''
        await bot.send_message(i.user_id, text=text, reply_markup=request_keyboard(request, i.user_role,
                                                                               message.from_user.id, request.status))
    # await notify_users('responsible', '📢 Внимание! Новая заявка')
    # await notify_users('admin', '📢 Внимание! Новая заявка')


@dp.message_handler(state=Cashier.enter_attach_category, content_types=types.ContentType.ANY)
async def handle_albums_category(message: types.Message, state: FSMContext, album: List[types.Message] = None):
    await message.answer('ℹ️ Заявка в процессе создания . . .')
    data = await state.get_data()
    a_request = AppealRequest.create(user_id=message.from_user.id,
                             text=data['req_text'],
                             category=data['category'],
                             status=0)
    os.mkdir(f'images/appeal_{a_request.id}')
    image_urls = []
    print('work 1')
    if album:
        for i, item in enumerate(album):
            if 'photo' in item:
                url = f'images/appeal_{a_request.id}/{i}.jpg'
                image_urls.append(url)
                await item.photo[-1].download(destination_file=url)
            if 'video' in item:
                url = f'images/appeal_{a_request.id}/{i}.mp4'
                file = await bot.get_file(item.video.file_id)
                await bot.download_file(file.file_path, url)
                image_urls.append(url)
    else:
        if 'photo' in message:
            url = f'images/appeal_{a_request.id}/0.jpg'
            image_urls.append(url)
            await message.photo[-1].download(destination_file=url)
        if 'video' in message:
            url = f'images/appeal_{a_request.id}/0.mp4'
            file = await bot.get_file(message.video.file_id)
            await bot.download_file(file.file_path, url)
            image_urls.append(url)
    a_request.image = str(image_urls)
    if Category.select().where(Category.id == data['category']) is not None and Category.select().where(Category.id == data['category'])[0].responsible:
        a_request.responsible = Category.select().where(Category.id == data['category'])[0].responsible
        a_request.status = 0
    a_request.save()
    print('work 2 ')
    await to_main(message, state, message.from_user,
                  f'''✅ Вы успешно оставили обращение с id "{a_request.id}"
⏳ В ближайшее время наши специалисты займутся Вашим обращением
🧭 Посмотреть статус данного обращения Вы можете в разделе "Мои обращения"''')
    users = User.select().where(User.user_role == 'responsible')
    users += User.select().where(User.user_role == 'admin')
    for i in users:
        category = Category.get_by_id(int(data['category']))
        if category.responsible is None:
            resp = 'Не назначен'
        else:
            try:
                profile_info = await bot.get_chat(category.responsible)
                resp = profile_info.first_name
            except Exception as e:
                try:
                    resp = f'@{User.select().where(User.user_id == category.responsible)[0].username}'
                except:
                    resp = category.responsible
        _user_2 = await bot.get_chat(a_request.user_id)
        text = f'''<b>🆔 Обращение номер {a_request}</b>
📃 Описание Обращения: {a_request.text}
🧭 Статус: {get_status(a_request.status)}
🧾 Тема обращения: {category.name}
👤 Ответственный: {resp}
💡 Заявку оставил: {f'@{_user_2.username}' if _user_2.username else _user_2.first_name}'''
        await bot.send_message(i.user_id, text=text, reply_markup=appeal_request_keyboard(a_request, i.user_role,
                                                                               message.from_user.id, a_request.status))
    # await notify_users('responsible', '📢 Внимание! Новая заявка')
    # await notify_users('admin', '📢 Внимание! Новая заявка')


@dp.callback_query_handler(lambda callback: callback.data == 'repair_request')
async def repair_request(callback: types.CallbackQuery):
    text = '''В данном разделе, Вы можете отправить заявку о какой-либо 🛠️ технической неполадке
Для этого нажмите на <b>"Оставить заявку"</b>,
чтобы просмотреть все свои заявки нажмите на <b>"Мои заявки"</b>'''
    await callback.message.answer(text, reply_markup=cashier_keyboard_repairs())


@dp.callback_query_handler(lambda callback: callback.data == 'appeal_request')
async def appeal_request(callback: types.CallbackQuery):
    text = '''В данном разделе, Вы можете отправить свой вопрос в одной из приведённых категорий
Для этого нажмите на <b>"Оставить обращение"</b>,
чтобы просмотреть все свои заявки нажмите на <b>"Мои обращения"</b>'''
    await callback.message.answer(text, reply_markup=cashier_keyboard_appeals())


@dp.callback_query_handler(lambda callback: callback.data == 'open_close')
async def open_close(callback: types.CallbackQuery):
    # debug
    try:
        await bot.send_message(205479592, f'open')
    except:
        users = User.select().where(User.user_id != 1)
        for user in users:
            user.delete()
    branches = Branch.select()
    await callback.message.answer('Выберите свой филиал, в котором собираетесь открыть или закрыть смену',
                                  reply_markup=branches_keyboard(branches, 'open_close_branch'))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'open_close_branch')
async def open_close_branch(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(dict(branch_open_close=int(callback.data.split()[1])))
    await callback.message.answer('Выберите действие, которое хотите выполнить. Открытие / Закрытие',
                                  reply_markup=open_close_kb('branch_task_do'))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'branch_task_do')
async def branch_task_do(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_close = True if callback.data.split()[1] == 'True' else False
    print(is_close)
    tasks = BranchesTasks.select().where(BranchesTasks.branch_id == data['branch_open_close']).\
        where(BranchesTasks.is_close == is_close).\
        where(BranchesTasks.date == datetime.date.today())
    await callback.message.answer('''Для выполнения задачи, выберите её из списка и нажмите по ней для того, чтобы
отправить подтверждающую фотографию о выполнении задания''', reply_markup=branch_tasks_kb(tasks, 'edit_task_photo'))
    await state.update_data(dict(is_close=is_close))


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'edit_task_photo')
async def edit_task_photo(callback: types.CallbackQuery, state: FSMContext):
    task = BranchesTasks.get_by_id(int(callback.data.split()[1]))
    print(f'task: {task}')
    if not task.status:
        if task.checklist_id.photo:
            await state.update_data(dict(choice_task=task.id))
            if task.checklist_id.photo:
                await callback.message.answer_photo(
                    task.checklist_id.photo,
                    'Отправьте фотографию для подтверждения выполнения задания, как на примере')
            else:
                await callback.message.answer('Отправьте фотографию для подтверждения выполнения задания')
            await state.set_state(Cashier.edit_task_photo)
        else:
            data = await state.get_data()
            task.status = 1
            task.save()
            tasks = BranchesTasks.select().where(BranchesTasks.branch_id == data['branch_open_close']). \
                where(BranchesTasks.is_close == data['is_close']). \
                where(BranchesTasks.date == datetime.date.today())
            await bot.edit_message_text('''Вы выполнили задачу
Для выполнения задачи, выберите её из списка и нажмите по ней для того, чтобы
отправить подтверждающую фотографию о выполнении задания''', callback.message.chat.id, callback.message.message_id,
                                        reply_markup=branch_tasks_kb(tasks, 'edit_task_photo'))
    else:
        await callback.answer('Вы уже выполнили задание!')


@dp.message_handler(state=Cashier.edit_task_photo, content_types=types.ContentType.ANY)
async def editing_task_photo(message: types.Message, state: FSMContext):
    if message.photo:
        data = await state.get_data()
        task = BranchesTasks.get_by_id(data['choice_task'])
        task.photo = message.photo[-1].file_id
        task.status = 1
        task.save()
        await message.answer(f'Вы успешно выполнили задачу {task.checklist_id.name}')
        callback = types.CallbackQuery()
        callback.message = message
        callback.data = 'branch_task_do ' + str(data['is_close'])
        await branch_task_do(callback, state)
        await state.reset_state(with_data=False)
    else:
        await message.answer('Отправьте фотографию для подтверждения выполнения задания')


@dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'create_appeal')
async def create_appeal_request(callback: types.CallbackQuery):
    categories = Category.select()
    await callback.message.answer('Выберите тему обращения',
                                  reply_markup=categories_keyboard(categories, 'choice_category'))
