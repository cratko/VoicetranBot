from .loader import bg_dialog
from .main_menu import *


# Регистрация всех диалогов
def setup_dialogs():
    return [main_menu_dialog, bg_dialog]
