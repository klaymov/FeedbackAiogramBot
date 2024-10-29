from aiogram import Bot, types, F, Router
import logging
import os

logging.basicConfig(filename='logs/logs.txt',level=logging.INFO)
r = Router()


@r.message(F)
async def echo(message: types.Message, bot: Bot):
    admin_id = int(os.getenv('ADMINS_ID'))
    if message.from_user.id == admin_id:
        return
    if message.from_user.username:
        text = f"""Новое сообщение от @{message.from_user.username}! 👇"""
    else:
        text = f"""Новое сообщение от ID{message.from_user.id}! 👇"""
    text2 = f"""Чтобы ответить напишите: <code>/reply {message.from_user.id} текст</code>"""
    
    if message.text:
        await bot.send_message(
            chat_id=os.getenv('ADMINS_ID'),
            text=f"{text}\n\n{message.text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.photo:
        await bot.send_photo(
            chat_id=os.getenv('ADMINS_ID'),
            photo=message.photo[-1].file_id,
            caption=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.document:
        await bot.send_document(
            chat_id=os.getenv('ADMINS_ID'),
            document=message.document.file_id,
            caption=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.video:
        await bot.send_video(
            chat_id=os.getenv('ADMINS_ID'),
            video=message.video.file_id,
            caption=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.audio:
        await bot.send_audio(
            chat_id=os.getenv('ADMINS_ID'),
            audio=message.audio.file_id,
            caption=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.voice:
        await bot.send_voice(
            chat_id=os.getenv('ADMINS_ID'),
            voice=message.voice.file_id,
            caption=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.video_note:
        await bot.send_video_note(
            chat_id=os.getenv('ADMINS_ID'),
            video_note=message.video_note.file_id,
            )
        await bot.send_message(
            chat_id=os.getenv('ADMINS_ID'),
            text=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.sticker:
        await bot.send_sticker(
            chat_id=os.getenv('ADMINS_ID'),
            sticker=message.sticker.file_id,
            )
        await bot.send_message(
            chat_id=os.getenv('ADMINS_ID'),
            text=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.location:
        await bot.send_location(
            chat_id=os.getenv('ADMINS_ID'),
            latitude=message.location.latitude,
            longitude=message.location.longitude,
            )
        await bot.send_message(
            chat_id=os.getenv('ADMINS_ID'),
            text=f"{text}\n\n{text2}",
            parse_mode='html'
            )
    elif message.contact:
        await bot.send_contact(
            chat_id=os.getenv('ADMINS_ID'),
            phone_number=message.contact.phone_number,
            first_name=message.contact.first_name,
            last_name=message.contact.last_name,
            )
        await bot.send_message(
            chat_id=os.getenv('ADMINS_ID'),
            text=f"{text}\n\n{text2}",
            parse_mode='html'
            )