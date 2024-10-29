from aiogram import Bot, Dispatcher
import asyncio
import os
import logging
from app.handlers import echo, reply 
from logs import log

logging.basicConfig(filename='logs/logs.txt',level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    
    dp.include_routers(
        reply.r,
        echo.r
        )

    asyncio.create_task(log.logs_del())
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())