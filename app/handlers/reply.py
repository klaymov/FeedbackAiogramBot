from aiogram import Bot, types, F, Router
from aiogram.filters import Command
import logging
import os


logging.basicConfig(filename='logs/logs.txt',level=logging.INFO)
r = Router()


@r.message(Command("reply"))
async def reply(message: types.Message, bot: Bot):
    admin_id = int(os.getenv('ADMINS_ID'))
    if message.from_user.id != admin_id:
        return
    try:
        command_parts = message.text.split(maxsplit=2)
        if len(command_parts) < 3:
            await message.reply(
                text="Ошибка: Пожалуйста, используйте формат <code>/reply 'user_id' 'текст ответа'</code>",
                parse_mode='html'
                )
            return

        user_id = int(command_parts[1])
        reply_text = command_parts[2]

        await bot.send_message(
            chat_id=user_id,
            text=reply_text
            )
        await message.reply("Ответ успешно отправлен!")

    except Exception as e:
        logging.error(e)
        await message.reply("Произошла ошибка при отправке ответа.")