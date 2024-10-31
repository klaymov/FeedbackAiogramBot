from __future__ import annotations

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from loguru import logger
from bot.handlers import get_handlers_router
from bot.middlewares import register_middlewares

def configure_logger() -> None:
    logger.add(
        "logs/telegram_bot.log",
        level="DEBUG",
        format="{time:YYYY-MM-DDTHH:mm:ss.SSSZ!UTC} {level} {message}",
        rotation="50 KB",
        compression="zip",
    )

def get_bot_token() -> str:
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set!")
    return token

async def log_bot_info(bot: Bot) -> None:
    bot_info = await bot.get_me()
    states = {True: "Enabled", False: "Disabled", None: "Unknown (This's not a bot)"}

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")
    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")
    logger.info("Bot successfully started")

async def main() -> None:
    load_dotenv()
    configure_logger()

    token = get_bot_token()
    bot = Bot(token=token)
    dp = Dispatcher()

    await register_middlewares(dp)
    await log_bot_info(bot)

    router = get_handlers_router()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Polling error: {e}")
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
