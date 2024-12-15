from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.queries import get_stats

stats_router = Router()


@stats_router.message(Command("stats"))
async def show_stats(message: Message):
    if message.from_user.id != 451469271:
        await message.reply("Недостаточно прав")
    stats_text = get_stats()  # Получаем статистику из базы данных
    await message.reply(stats_text)
