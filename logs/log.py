#удаление логов

import asyncio
import aiofiles
import logging

logging.basicConfig(filename='logs/logs.txt',level=logging.INFO)
file_path = 'logs/logs.txt'
    

async def clear(file_path):
    try:
        async with aiofiles.open(file_path, mode='r') as file:
            lines = await file.readlines()

        if len(lines) >= 5000:
            async with aiofiles.open(file_path, mode='w') as file:
                await file.write('')
        else:
            pass

    except Exception as e:
        logging.error(e)

async def logs_del():
    global file_path
    while True:
        await clear(file_path)
        await asyncio.sleep(10)