import asyncio
import aioschedule


from config import BOT_TOKEN, TIME_FOR_CLERK
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from classes.album import *

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML, loop=asyncio.get_event_loop())
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    from handlers.functions import to_main
    await to_main(message, state, message.from_user)


@dp.message_handler(commands=['exit'], state='*')
async def exit(message: types.Message, state: FSMContext):
    from handlers.functions import to_main
    await to_main(message, state, message.from_user)


async def scheduler():
    from handlers.functions import null_tasks
    aioschedule.every().day.at(TIME_FOR_CLERK).do(null_tasks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    from handlers.cashier import *
    from handlers.responsible_appeal import *
    from handlers.responsible_break import *
    from handlers.admin import *
    from handlers.choice_branch import *
    from handlers.choice_category import *
    from handlers.clerk import *

    dp.middleware.setup(AlbumMiddleware())
    print('bot started')
    executor.start_polling(dp, on_startup=on_startup)
