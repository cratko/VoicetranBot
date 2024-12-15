from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, ContentType, Message
from aiogram_dialog import (
    ChatEvent,
    Dialog,
    DialogManager,
    ShowMode,
    StartMode,
    Window,
    setup_dialogs,
)

from database.queries import register
from keyboards.main_menu import get_main_keyboard

start_router = Router()

@start_router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    from dialogs.main_menu import MainMenuSG
    # it is important to reset stack because user wants to restart everything
    register(message.from_user.id)
    await message.answer("Добро пожаловать!", reply_markup=get_main_keyboard())

@start_router.message(Command("menu"))
async def start(message: Message, dialog_manager: DialogManager):
    from dialogs.main_menu import MainMenuSG
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)
