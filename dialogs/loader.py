from aiogram_dialog import (
    BaseDialogManager,
    Dialog,
    DialogManager,
    StartMode,
    Window,
    setup_dialogs,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Multi, Progress, Format
from aiogram.fsm.state import State, StatesGroup

from utils.i18n import Translate

class Bg(StatesGroup):
    progress = State()


async def get_bg_data(dialog_manager: DialogManager, **kwargs):
    return {
        "progress": dialog_manager.dialog_data.get("progress", 0),
    }

bg_dialog = Dialog(
    Window(
        Multi(
            Progress("progress", 10),
        ),
        state=Bg.progress,
        getter=get_bg_data,
    ),
)
