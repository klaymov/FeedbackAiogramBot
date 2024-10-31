from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from loguru import logger

async def register_middlewares(dp: Dispatcher) -> None:
    from .logging import LoggingMiddleware

    dp.update.outer_middleware(LoggingMiddleware())
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    logger.info("Middlewares registered")