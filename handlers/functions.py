import datetime

from main import bot
from aiogram.dispatcher import FSMContext
from utilities import *


# async def delete_messages(state: FSMContext, message: types.Message = None):
#     data = await state.get_data()
#     if data:
#         for msg in data['messages']:
#             #print(f'state {msg}')
#             if type(msg) == list:
#                 for row in msg:
#                     await row.delete()
#             else:
#                 await msg.delete()
#     if type(message) == types.Message:
#         #print(f'func {message}')
#         await message.delete()
#     elif type(message) == list:
#         for i in message:
#             await i.delete()
#     await state.update_data(dict(messages=[]))


async def to_main(message: types.Message, state: FSMContext, _user: types.User, _text=''):
    await state.reset_state(with_data=True)
    user = User.get_or_none(User.user_id == _user.id)
    if user is None:
        user = User.create(user_id=message.from_user.id, user_role='cashier', username=_user.username)
    if not user.username and _user.username:
        user.username = _user.username
        user.save()
    if user.user_role == 'cashier':
        text = '''<b>📑 Главное меню</b>\nИз этого меню Вы можете: перейти к заявкам о поломках и обращениях (создать новую или 
просмотреть существующие), произвести открытие или закрытие филиала'''
        await message.answer(_text + '\n' + text, reply_markup=cashier_keyboard())
    elif user.user_role == 'responsible_break':
        text = '''<b>📑 Главное меню</b>
Для того, чтобы просмотреть новые заявки, нажмите на кнопку "На рассмотрении"'''
        await message.answer(_text + '\n' + text, reply_markup=break_responsible_keyboard())
    elif user.user_role == 'responsible_appeal':
        text = '''<b>📑 Главное меню</b>
    Для того, чтобы просмотреть новые заявки, нажмите на кнопку "На рассмотрении"'''
        await message.answer(_text + '\n' + text, reply_markup=appeal_responsible_keyboard())
    elif user.user_role == 'responsible':
        text = '''<b>📑 Главное меню</b>
        Для того, чтобы просмотреть новые заявки, нажмите на кнопку "На рассмотрении"'''
        await message.answer(_text + '\n' + text, reply_markup=adm_resp_keyboard())
#     elif user.user_role == 'clerk':
#         text = '''<b>📑 Главное меню</b>
# Для того, чтобы просмотреть свои задачи, нажмите на кнопку "Мои задачи"'''
#         await message.answer(_text + '\n' + text, reply_markup=clerk_keyboard())
#     elif user.user_role == 'resp_clerk':
#         text = '''<b>📑 Главное меню</b>
# Для того, чтобы просмотреть 🎯 задачи пользователей, нажмите на кнопку "Чек-листы"'''
#         await message.answer(_text + '\n' + text, reply_markup=resp_clerk_kb())
    elif user.user_role == 'admin':
        text = '''<b>Административное меню</b>
Здесь Вы можете отредактировать 🏬 филиалы, 🧾 категории, назначить 🔑 роль пользователям или составить 📑 чек-листы'''
        await message.answer(_text + '\n' + text, reply_markup=admin_keyboard())
    else:
        await message.answer('❌ Ошибка! У Вас не назначена роль')


def get_status(status):
    if status == 0:
        return '⏳ На рассмотрении'
    elif status == 1:
        return '🔧 В работе'
    elif status == 2:
        return '✅ Выполнена'
    else:
        return '❌ Ошибка'


def get_role_name(role):
    if role == 'cashier':
        return 'Линейный персонал'
    elif role == 'responsible_appeal':
        return 'Ответственный за обращения'
    elif role == 'responsible_break':
        return 'Ответственный за поломки'
    elif role == 'responsible':
        return 'Универсальный ответственный'
    elif role == 'admin':
        return 'Администратор'


async def notify_users(user_role, text):
    users = User.select().where(User.user_role == user_role)
    for i in users:
        await bot.send_message(i.user_id, text)


async def null_tasks():
    tasks = Task.select()
    for i in tasks:
        i.date = None
        i.status = 1
        i.save()
    today = datetime.date.today()
    tasks = BranchesTasks.select()
    for task in tasks:
        print((datetime.datetime.strptime(task.date, '%Y-%m-%d').date() - today).days)
        if (datetime.datetime.strptime(task.date, '%Y-%m-%d').date() - today).days < -2:
            task.delete_instance()
    checklists = ChecklistTemplates.select()
    for point in checklists:
        BranchesTasks.create(checklist_id=point.id, date=today,
                             branch_id=point.branch_id, is_close=point.is_close)
