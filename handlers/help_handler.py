from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

# Регистрируем маршруты
help_router = Router()


@help_router.message(Command("help"))
async def send_help(message: Message):
    await message.answer(
        "Чтобы воспользоваться ботом, отправьте ему голосовое сообщение, и он переведёт его в текст.\n"
    )
