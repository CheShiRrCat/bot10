# import time
#
# from main import dp
# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from utilities import *
# from handlers.functions import to_main, notify_users, get_status
# from datetime import datetime, timedelta
#
#
# @dp.callback_query_handler(lambda callback: callback.data == 'my_tasks')
# async def show_my_tasks(callback: types.CallbackQuery, state: FSMContext):
#     tasks = Task.select().where(Task.user_id == callback.from_user.id)
#     for i in tasks:
#         task_text = f'''🎯 Задача: {i.text}
# 🧭 Статус: {get_status(i.status)}
# {f"Время выполнения: 📅 {i.date.day}-{i.date.month}-{i.date.year}: 🕒 {i.date.hour}-{i.date.minute}"
#         if i.status == 2 else ""}'''
#         await callback.message.answer(task_text, reply_markup=clerk_task_kb(i.id) if i.status == 1 else None)
#     text = f'''❌ Для возвращения в главное меню - нажмите "Отмена"'''
#     await callback.message.answer(text, reply_markup=cancel_inline())
#
#
# @dp.callback_query_handler(lambda callback: callback.data.split()[0] == 'task_complete')
# async def task_complete(callback: types.CallbackQuery, state: FSMContext):
#     task = Task.get_by_id(int(callback.data.split()[1]))
#     task.status = 2
#     task.date = datetime.now() + timedelta(hours=7)
#     task.save()
#     await notify_users('resp_clerk', f'📢 {callback.from_user.full_name} '
#                                      f'{callback.from_user.username + " " if callback.from_user.username else ""}'
#                                      f'выполнил задание "{task.text}"')
#     await notify_users('admin', f'📢 {callback.from_user.full_name} '
#                                      f'{callback.from_user.username + " " if callback.from_user.username else ""}'
#                                      f'выполнил задание "{task.text}"')
#     await to_main(callback.message, state, callback.from_user, '✅ Вы успешно выполнили задачу')
#
