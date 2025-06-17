import asyncio
import logging
# import asyncpg 
from asyncio import WindowsSelectorEventLoopPolicy

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from data.config import settin
from app.handlers import rout
from app.admin_operation import rou
from data.entry_db import database_entry
# from others.state_user import States
from others.middlware import DbSession
from data.settings import async_session


asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settin.ID_admin, text='Started')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settin.ID_admin, text='Stop_bot')


async def comm(bot: Bot):
    command = [
        BotCommand(
            command='/start',
            description='поехали'
            
        )
    ]
    await bot.set_my_commands(command, BotCommandScopeDefault())


async def start():
    bots = Bot(settin.TOKEN)
    dp = Dispatcher()
    dp.include_router(rout)
    dp.include_router(rou)
    
    dp.shutdown.register(stop_bot)
    dp.startup.register(start_bot)
    
    
    await comm(bots)
    print(f'Bot is ready to work!')
    
    dp.callback_query.middleware(DbSession(async_session))
    dp.update.middleware(DbSession(async_session))
    dp.message.middleware(DbSession(async_session))
    
    sheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    sheduler.add_job(database_entry, 'cron', hour=1, minute=00, start_date='2025-05-05 01:00:00')
    sheduler.start()
    
    await database_entry()
    try:
        await bots.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bots)
    finally:
        await bots.session.close()
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except (KeyboardInterrupt, SystemExit):
        print('Exit')
        
