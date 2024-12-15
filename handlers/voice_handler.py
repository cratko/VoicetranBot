import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram_dialog import BaseDialogManager, DialogManager, StartMode

from config_data import config
from config_data.config import Config
from database.init_db import init_db
from dialogs.loader import Bg
from utils.speech_recognition import recognize_speech
from database.queries import record_stat, get_balance, update_balance

import io

# Подключаем маршруты
voice_router = Router()


@voice_router.message(F.voice)
async def start_bg(
    message: Message,
    dialog_manager: DialogManager,
):
    if get_balance(message.from_user.id) < 1:
        await message.answer("Недостаточно средств. Стоимость обработки: 10 рублей")
        return
    await dialog_manager.start(Bg.progress)
    asyncio.create_task(process_voice_message(message, dialog_manager.bg()))  # noqa: RUF006


async def process_voice_message(message: Message, dialog_manager: BaseDialogManager):
    # Получаем информацию о файле голосового сообщения через file_id
    if get_balance(message.from_user.id) < 1:
        await message.answer("Недостаточно средств")
    await dialog_manager.update({
        "progress": 1 * 100 / 10,
    })

    voice = message.voice

    await dialog_manager.update({
        "progress": 2 * 100 / 10,
    })

    config = Config()
    bot = Bot(token=config.BOT_TOKEN)  # Укажите токен бота
    file = await bot.get_file(voice.file_id)

    await dialog_manager.update({
        "progress": 7 * 100 / 10,
    })

    # Скачиваем файл в буфер
    voice_file = io.BytesIO()
    await bot.download_file(file.file_path, destination=voice_file)
    voice_file.seek(0)  # Сбрасываем указатель начала файла, чтобы можно было читать

    await dialog_manager.update({
        "progress": 8 * 100 / 10,
    })

    # Распознаем текст из голосового сообщения
    text_response = recognize_speech(voice_file)

    await dialog_manager.update({
        "progress":  9 * 100 / 10,
    })

    # Сохраняем статистику пользователя
    record_stat(message.from_user.id)

    await dialog_manager.update({
        "progress": 10 * 100 / 10,
    })

    # Отправляем пользователю распознанный текст
    await message.reply(text_response)
    await dialog_manager.done()
    update_balance(message.from_user.id, -10)
