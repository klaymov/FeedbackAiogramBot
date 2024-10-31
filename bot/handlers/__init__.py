from __future__ import annotations

from aiogram import Router, F
from loguru import logger

def get_handlers_router() -> Router:
    import bot.handlers.main as main
    
    router = Router()

    private_router = Router()
    private_router.message.filter(F.chat.type == "private")
    private_router.include_router(main.router)

    router.include_router(private_router)
    logger.info("Routers successfully loaded and started")
    return router