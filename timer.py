import asyncio
from datetime import datetime, timedelta

from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utilities import AppealRequest, User, Request

bot = Bot(token=BOT_TOKEN, loop=asyncio.get_event_loop())
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    all_req = AppealRequest.select()
    for req in all_req:
        time_delta = datetime.now() - req.last_update
        if time_delta > timedelta(hours=3) and req.status == 0:
            users = User.select().where(User.user_role == 'responsible_appeal')
            users += User.select().where(User.user_role == 'responsible')
            for user in users:
                try:
                    await bot.send_message(user.user_id,
                                           f"У вас есть непринятое обращение (id {req.id}), обратите на него внимание")
                except:
                    pass
            req.last_update = datetime.now()
            req.save()

        if time_delta > timedelta(days=7) and req.status == 1:
            try:
                await bot.send_message(req.responsible,
                                       f"Обращение(id {req.id})долго висит, закрой его, если оно выполнена, либо не забывайте о нем, все получится)")
            except:
                pass
            req.last_update = datetime.now()
            req.save()

    all_rep = Request.select()
    for rep in all_rep:
        time_delta = datetime.now() - rep.last_update
        if time_delta > timedelta(hours=3) and rep.status == 0:
            users = User.select().where(User.user_role == 'responsible_break')
            users += User.select().where(User.user_role == 'responsible')
            for user in users:
                try:
                    await bot.send_message(user.user_id,
                                           f"У вас есть непринятая заявка на ремонт (id {rep.id}), обратите на нее внимание")
                except:
                    pass
            rep.last_update = datetime.now()
            rep.save()

        if time_delta > timedelta(days=7) and rep.status == 1:
            try:
                await bot.send_message(rep.responsible,
                                       f"Заявка на ремонт (id {rep.id}) долго висит, закрой ее, если она выполнена, либо не забывайте о ней, все получится)")
            except:
                pass
            rep.last_update = datetime.now()
            rep.save()


if __name__ == '__main__':
    while True:
        asyncio.run(main())
