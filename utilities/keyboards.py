from aiogram import types


def cashier_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🛠️ Поломка', callback_data=f'repair_request'))
    kb.add(types.InlineKeyboardButton(text='🧾 Обращение', callback_data=f'appeal_request'))
    kb.add(types.InlineKeyboardButton(text='Открытие/Закрытие', callback_data=f'open_close'))
    return kb


def cashier_keyboard_repairs():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🛠️ Оставить заявку', callback_data=f'create_request'))
    kb.add(types.InlineKeyboardButton(text='📋 Мои заявки', callback_data=f'show_requests'))
    kb.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back'))
    return kb


def cashier_keyboard_appeals():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🧾 Оставить обращение', callback_data=f'create_appeal'))
    kb.add(types.InlineKeyboardButton(text='📋 Мои обращения', callback_data=f'show_appeals'))
    kb.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back'))
    return kb


def adm_resp_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🛠️ Поломки', callback_data=f'show_types_requests'))
    kb.add(types.InlineKeyboardButton(text='🧾 Обращения', callback_data=f'show_types_appeals_requests'))
    kb.add(types.InlineKeyboardButton(text='📋 Чек-листы линейного персонала', callback_data=f'show_checklists'))
    return kb


def appeal_responsible_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🧾 Обращения', callback_data=f'show_types_appeals_requests'))
    kb.add(types.InlineKeyboardButton(text='📋 Чек-листы линейного персонала', callback_data=f'show_checklists'))
    return kb


def break_responsible_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🛠️ Поломки', callback_data=f'show_types_requests'))
    kb.add(types.InlineKeyboardButton(text='📋 Чек-листы линейного персонала', callback_data=f'show_checklists'))
    return kb


def responsible_requests_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='⏳ На рассмотрении', callback_data=f'show_requests 0'))
    kb.add(types.InlineKeyboardButton(text='🔧 В работе', callback_data=f'show_requests 1'))
    kb.add(types.InlineKeyboardButton(text='✅ Завершенные', callback_data=f'show_requests 2'))
    return kb


def responsible_appeal_requests_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='⏳ На рассмотрении', callback_data=f'show_appeals 0'))
    kb.add(types.InlineKeyboardButton(text='🔧 В работе', callback_data=f'show_appeals 1'))
    kb.add(types.InlineKeyboardButton(text='✅ Завершенные', callback_data=f'show_appeals 2'))
    return kb


def resp_clerk_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='📑 Чек-листы', callback_data=f'edit_checklists'))
    return kb


def resp_checklists_kb(dates, callback):
    kb = types.InlineKeyboardMarkup()
    for i in dates:
        kb.add(types.InlineKeyboardButton(text=i, callback_data=f'{callback} {i}'))
    return kb


def clerk_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🎯 Мои задачи', callback_data=f'my_tasks'))
    return kb


def clerk_task_kb(task_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='✅ Выполнить', callback_data=f'task_complete {task_id}'))
    return kb


def admin_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🛠️ Заявки', callback_data=f'adm_requests'))
    kb.add(types.InlineKeyboardButton(text='🏬 Филиалы', callback_data=f'edit_branches'))
    kb.add(types.InlineKeyboardButton(text='🧾 Категории', callback_data=f'edit_categories'))
    kb.add(types.InlineKeyboardButton(text='🔑 Права доступа', callback_data=f'edit_roles'))
    kb.add(types.InlineKeyboardButton(text='📑 Чек-листы', callback_data=f'edit_checklists'))
    return kb


def branch_edit():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton(text='✏️ Изменить', callback_data=f'edit_branch'),
           types.InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete_branch'))
    kb.row(types.InlineKeyboardButton(text='Открытие', callback_data='checklist_branch 0'),
           types.InlineKeyboardButton(text='Закрытие', callback_data='checklist_branch 1'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def category_edit():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton(text='✏️ Изменить', callback_data=f'edit_category'),
           types.InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete_category'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def category_edit_type():
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton(text='✏️ Изменить имя', callback_data=f'change_category_name'),
           types.InlineKeyboardButton(text='👤 Изменить ответственного', callback_data=f'change_category_responsible'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def edit_roles_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Линейный персонал', callback_data='cashier'))
    kb.add(types.InlineKeyboardButton(text='Универсальный ответственный', callback_data='responsible'))
    kb.add(types.InlineKeyboardButton(text='Ответственный за поломки', callback_data='responsible_break'))
    kb.add(types.InlineKeyboardButton(text='Ответственный за обращения', callback_data='responsible_appeal'))
    # kb.add(types.InlineKeyboardButton(text='Клерк', callback_data='clerk'))
    # kb.add(types.InlineKeyboardButton(text='Ответственный клерк', callback_data='resp_clerk'))
    kb.add(types.InlineKeyboardButton(text='Администратор', callback_data='admin'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def edit_checklists_kb(users, callback):
    kb = types.InlineKeyboardMarkup()
    for i in users:
        kb.add(types.InlineKeyboardButton(text=i.username, callback_data=f'{callback} {i.user_id}'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def add_task_and_back(callback):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='➕ Добавить', callback_data=f'add_task'))
    kb.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data=callback))
    return kb


def edit_task_kb(task_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='✏️ Изменить', callback_data=f'add_task {task_id}'))
    kb.add(types.InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete_task {task_id}'))
    return kb


def branches_keyboard(branches, callback, user_role='cashier'):
    kb = types.InlineKeyboardMarkup()
    print(callback)
    for i in branches:
        kb.add(types.InlineKeyboardButton(text=i.name, callback_data=f'{callback} {i.id}'))
    if user_role == 'admin' and callback == 'choice_branch':
        kb.add(types.InlineKeyboardButton(text='➕ Добавить', callback_data='edit_branch'))
    kb.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def categories_keyboard(categories, callback, user_role='cashier'):
    kb = types.InlineKeyboardMarkup()
    for i in categories:
        kb.add(types.InlineKeyboardButton(text=i.name, callback_data=f'{callback} {i.id}'))
    if user_role == 'admin' and callback == 'choice_category':
        kb.add(types.InlineKeyboardButton(text='➕ Добавить', callback_data='edit_category'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def open_close_kb(callback):
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton(text='Открытие', callback_data=f'{callback} False'),
           types.InlineKeyboardButton(text='Закрытие', callback_data=f'{callback} True'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def branch_tasks_kb(tasks, callback, user_role='cashier'):
    kb = types.InlineKeyboardMarkup()
    for i in tasks:
        symbol = '✅' if i.status else '❌'
        kb.add(types.InlineKeyboardButton(text=symbol + ' ' + i.checklist_id.name, callback_data=f'{callback} {i.id}'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def checklists_branch_kb(checklists, is_close):
    kb = types.InlineKeyboardMarkup()
    for i in checklists:
        kb.add(types.InlineKeyboardButton(text=i.name, callback_data=f'choice_checklist {i.id}'))
    kb.add(types.InlineKeyboardButton(text='➕ Добавить', callback_data=f'add_checklist {is_close}'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def edit_checklist_kb(checklist_id):
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton(text='Изменить', callback_data=f'change_checklist {checklist_id}'),
           types.InlineKeyboardButton(text='Удалить', callback_data=f'delete_checklist {checklist_id}'))
    kb.add(types.InlineKeyboardButton(text='Фото', callback_data=f'photo_checklist {checklist_id}'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def cancel_inline():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back'))
    kb.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return kb


def back_inline(callback):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data=callback))
    return kb


def request_keyboard(request, role=None, user_id=None, status=None):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='📸 Просмотр медиа', callback_data=f'show_media_request {request}'))
    if role == 'responsible_break' or role == 'responsible_appeal' or role == 'responsible' or role == 'admin':
        text, callback = '', ''
        if status == 0 or status == 2:
            text, callback = '🔧 В работу', f'req_change_status {request} 1'
        elif status == 1:
            text, callback = '✅ Завершен', f'req_change_status {request} 2'
        kb.row(types.InlineKeyboardButton(text=text, callback_data=callback),
               types.InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete {request}'))
        kb.add(types.InlineKeyboardButton(text='🤵 Написать', url=f'tg://user?id={user_id}'))
    return kb


def appeal_request_keyboard(request, role=None, user_id=None, status=None):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='📸 Просмотр медиа', callback_data=f'show_media_appeal_request {request}'))
    if role == 'responsible_break' or role == 'responsible_appeal' or role == 'responsible' or role == 'admin':
        text, callback = '', ''
        if status == 0 or status == 2:
            text, callback = '🔧 В работу', f'req_appeal_change_status {request} 1'
        elif status == 1:
            text, callback = '✅ Завершен', f'req_appeal_change_status {request} 2'
        kb.row(types.InlineKeyboardButton(text=text, callback_data=callback),
               types.InlineKeyboardButton(text='🗑️ Удалить', callback_data=f'delete_appeal {request}'))
        kb.add(types.InlineKeyboardButton(text='🤵 Написать', url=f'tg://user?id={user_id}'))
    return kb


def next_step():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add('Пропустить')
    kb.add('⬅️ Назад')
    return kb


def delete_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add('Удалить')
    return kb