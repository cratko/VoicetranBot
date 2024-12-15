from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создание клавиатуры
def get_main_keyboard():
    # Создаем кнопки
    top_up_button = KeyboardButton(text="/payment Пополнить")
    balance_button = KeyboardButton(text="/balance Баланс")

    show_menu = KeyboardButton(text="/menu Меню")

    # Добавляем кнопки в клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [top_up_button, balance_button],
            [show_menu],
        ],
        resize_keyboard=True  # Подгон размера под интерфейс пользователя
    )
    return keyboard