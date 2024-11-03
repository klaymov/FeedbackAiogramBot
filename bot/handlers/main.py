from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramForbiddenError
import os
from typing import TYPE_CHECKING, Optional
from loguru import logger
from aiogram.filters import Command

if TYPE_CHECKING:
    from aiogram.types import Message

router = Router(name='echo')

@router.message(Command("reply"))
async def reply(message: Message) -> None:
    try:
        logger.info(f"Reply command received from {message.from_user.username} ({message.from_user.id})")
        admin_id = int(os.getenv("ADMINS_ID"))
        if message.from_user.id != admin_id:
            return
        
        command_parts = message.text.split(maxsplit=2)
        if len(command_parts) < 3:
            await message.reply(
                text="Ошибка: Пожалуйста, используйте формат <code>/reply 'user_id' 'текст ответа'</code>",
                parse_mode="html",
            )
            return

        user_id = int(command_parts[1])
        reply_text = command_parts[2]

        await message.bot.send_message(
            chat_id=user_id,
            text=reply_text,
        )
        await message.reply("Ответ успешно отправлен!")

    except Exception as e:
        logger.error(f"Error while sending reply: {e}")

@router.message(F)
async def echo(message: Message, bot: Bot) -> None:
    try:
        # if not message or message.text.startswith("/"): -> Неправильное ипользование тиньковоф!
        #     return

        admin_id: Optional[int] = os.getenv('ADMINS_ID')
        if not admin_id:
            logger.error("ADMINS_ID не установлено.")
            return
        
        admin_id = int(admin_id)
        if message.from_user.id == admin_id:
            return

        user_identifier = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        if message.text:
            base_text = f"Новое сообщение от {user_identifier}! 👇\n\n{message.text}"
        elif message.caption:
            base_text = f"Новое сообщение от {user_identifier}! 👇\n\n{message.caption}"
        else:
            base_text = f"Новое сообщение от {user_identifier}! 👇"
        reply_instruction = f"Чтобы ответить напишите: <code>/reply {message.from_user.id} текст</code>"

        await message.reply("Сообщение успешно отправлено!")

        async def send_to_admin(content_type: str, **kwargs):
            await getattr(bot, f'send_{content_type}')(chat_id=admin_id, **kwargs)
            await bot.send_message(chat_id=admin_id, text=reply_instruction, parse_mode='html')

        content_dispatcher = {
            'text': lambda: send_to_admin('message', text=base_text, parse_mode='html'),
            'photo': lambda: send_to_admin('photo', photo=message.photo[-1].file_id, caption=base_text, parse_mode='html'),
            'document': lambda: send_to_admin('document', document=message.document.file_id, caption=base_text, parse_mode='html'),
            'video': lambda: send_to_admin('video', video=message.video.file_id, caption=base_text, parse_mode='html'),
            'audio': lambda: send_to_admin('audio', audio=message.audio.file_id, caption=base_text, parse_mode='html'),
            'voice': lambda: send_to_admin('voice', voice=message.voice.file_id, caption=base_text, parse_mode='html'),
            'video_note': lambda: send_to_admin('video_note', video_note=message.video_note.file_id),
            'sticker': lambda: send_to_admin('sticker', sticker=message.sticker.file_id),
            'location': lambda: send_to_admin('location', latitude=message.location.latitude, longitude=message.location.longitude),
            'contact': lambda: send_to_admin('contact', phone_number=message.contact.phone_number, first_name=message.contact.first_name, last_name=message.contact.last_name),
        }

        for content_type, handler in content_dispatcher.items():
            if getattr(message, content_type, None):
                await handler()
                break

    except (TelegramForbiddenError, Exception) as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")