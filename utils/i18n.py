from typing import Callable, Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogProtocol, DialogManager, SubManager
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button, ListGroup
from aiogram_dialog.widgets.text import Format, Multi, Const, Text
from aiogram_dialog.widgets.text.format import _FormatDataStub

class Translate(Text):
    def __init__(self, text: str, when: callable = None):
        """
        Ленивый перевод текста, основываясь на i18n-контексте.

        :param text: Ключ перевода
        :param when: Условие отображения виджета.
        """
        super().__init__(when=when)
        self.text_key = text

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        """
        Подставляем перевод из i18n.
        """
        i18n = manager.middleware_data.get("i18n")
        if i18n:
            return i18n.gettext(self.text_key)
        return self.text_key