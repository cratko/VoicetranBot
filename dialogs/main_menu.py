from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import FSMI18nMiddleware
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from utils.i18n import Translate
from middlewares.i18n import i18n, i18n_middleware

_ = i18n.gettext

class MainMenuSG(StatesGroup):
    main = State()
    about = State()
    help = State()
    settings = State()


# Обработчики для переходов между окнами
async def on_about_clicked(event, widget, manager: DialogManager):
    await manager.done()
    await manager.start(MainMenuSG.about)



async def on_help_clicked(event, widget, manager: DialogManager):
    await manager.done()
    await manager.start(MainMenuSG.help)


async def go_back_main_menu(event, widget, manager: DialogManager):
    await manager.done()
    await manager.start(MainMenuSG.main)


async def start_voice_handler(event, widget, manager: DialogManager):
    # Получаем текущий язык пользователя из FSMContext
    state: FSMContext = manager.middleware_data['state']
    user_data = await state.get_data()
    user_language = user_data.get('language_code', 'en')  # Если языка нет — используем "en"

    # Локализуем перевод через i18n
    i18n.ctx_locale.set(user_language)

    await manager.done()
    await event.message.answer(i18n.gettext("Send a voice message"))
    await manager.done()


async def settings_handler(event, widget, manager: DialogManager):
    await manager.done()
    await manager.start(MainMenuSG.settings)

async def close_handler(event, widget, manager: DialogManager):
    await manager.done()

# Обработчик для смены языка
async def set_language(event: CallbackQuery, button: Button, manager: DialogManager):
    language_code = button.widget_id.split("_")[-1]

    state: FSMContext = manager.middleware_data['state']

    # Сохраняем текущий язык пользователя в FSMContext
    await state.update_data(language_code=language_code)

    # Меняем язык для текущего пользователя в i18n_middleware
    await i18n_middleware.set_locale(state, locale=language_code)
    await i18n_middleware.set_locale(manager.middleware_data["state"], locale=language_code)

    await event.message.answer(
        _("Language successfully changed: {language}").format(
            language="🇬🇧 English" if language_code == "en" else "🇷🇺 Русский"
        )
    )
    await manager.start(MainMenuSG.main)
    await manager.done()


from aiogram_dialog.widgets.text import Text



# Описание окон диалога
main_menu_dialog = Dialog(
    Window(
        Translate("Welcome to the main menu!\nChoose an action:"),
        Row(
            Button(Translate("▶️ Start translation"), id="start_voice", on_click=start_voice_handler),
        ),
        Row(
            Button(Translate("📖 About the bot"), id="about", on_click=on_about_clicked),
            Button(Translate("❓ Help"), id="help", on_click=on_help_clicked),
        ),
        Row(
            Button(Translate("⚙️ Settings"), id="settings", on_click=settings_handler),
        ),
        Row(
            Button(Translate("❌"), id="close", on_click=close_handler),
        ),
        state=MainMenuSG.main,
    ),

    Window(
        Translate("Settings:\nChoose your language:"),
        Row(
            Button(Translate("🇬🇧 English"), id="lang_en", on_click=set_language),
            Button(Translate("🇷🇺 Russian"), id="lang_ru", on_click=set_language),
        ),
        Button(Translate("⬅️ Back"), id="back", on_click=go_back_main_menu),
        state=MainMenuSG.settings,
    ),

    Window(
        Translate("About the bot."),
        Row(
            Button(Translate("⬅️ Back"), id="back", on_click=go_back_main_menu),
        ),
        state=MainMenuSG.about,
    ),

    Window(
        Translate("Help."),
        Row(
            Button(Translate("⬅️ Back"), id="back", on_click=go_back_main_menu),
        ),
        state=MainMenuSG.help,
    )
)
