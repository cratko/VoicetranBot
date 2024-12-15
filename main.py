from aiogram.filters import CommandStart

import dialogs
from config_data.config import Config
from database.init_db import init_db
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from handlers import voice_handler, help_handler, stats_handler, start_handler, \
    payment_handler  # Импортируем все роутеры

from aiogram_dialog import (
    setup_dialogs,
)

from handlers.payment_handler import payment_router
from middlewares.i18n import i18n_middleware


async def main():
    # Загружаем конфигурацию
    config = Config()

    # Инициализируем бота и диспетчер
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем базу данных
    init_db()

    dp.message.middleware(i18n_middleware)

    dp.include_router(dialogs.main_menu_dialog)
    dp.include_router(dialogs.bg_dialog)


    # Регистрируем все роутеры
    dp.include_router(payment_handler.payment_router)
    dp.include_router(start_handler.start_router)
    dp.include_router(voice_handler.voice_router)  # Роутер для обработки голосовых сообщений
    dp.include_router(help_handler.help_router)  # Роутер для команды /help
    dp.include_router(stats_handler.stats_router)  # Роутер для команды /stats



    setup_dialogs(dp)
    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
