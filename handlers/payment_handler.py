import hashlib
from urllib.parse import urlencode

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

from config_data.config import Config
from database.queries import update_balance, get_balance

PAYMASTER_URL = "https://paymaster.ru/Payment/Init"  # URL PayMaster для платежей
config = Config()

# FSM для оплаты
class PaymentState(StatesGroup):
    waiting_for_amount = State()


# Роутер для обработки команд и состояния
payment_router = Router()


def generate_payment_link(user_id: int, amount: float, description: str, success_url: str, secret_key: str,
                          merchant_id: str):
    """
    Генерация платежной ссылки для PayMaster.
    """
    data = {
        "LMI_MERCHANT_ID": merchant_id,
        "LMI_PAYMENT_AMOUNT": f"{amount:.2f}",  # Сумма (например, 100.00)
        "LMI_PAYMENT_DESC": description,  # Описание платежа
        "LMI_PAYMENT_NO": f"{user_id}_{int(amount * 100)}",  # Уникальный номер заказа
        "LMI_LANGUAGE": "en",  # Язык интерфейса ("ru" или "en")
        "LMI_SUCCESS_URL": success_url,  # URL для перенаправления после успешной оплаты
    }

    # Создаем подпись (signature)
    signature_data = f"{data['LMI_MERCHANT_ID']};{data['LMI_PAYMENT_AMOUNT']};{data['LMI_PAYMENT_DESC']};{secret_key}"
    data["LMI_HASH"] = hashlib.sha256(signature_data.encode('utf-8')).hexdigest()

    # Формируем ссылку
    payment_url = f"{PAYMASTER_URL}?{urlencode(data)}"
    return payment_url


# Обработчик команды /payment
@payment_router.message(Command("payment"))
async def ask_payment(message: Message, state: FSMContext):
    # Создаем клавиатуру с кнопкой "Указать сумму"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Указать сумму", callback_data="set_amount")],
        ]
    )

    # Сообщение с кнопкой
    await message.answer("Чтобы оплатить подписку, нажмите кнопку и укажите сумму:", reply_markup=keyboard)


# Обработка нажатия кнопки "Указать сумму"
@payment_router.callback_query(F.data == "set_amount")
async def prompt_for_amount(callback_query, state: FSMContext):
    await callback_query.message.edit_text("Введите сумму для пополнения в формате (например, 100.50):")
    await state.set_state(PaymentState.waiting_for_amount)  # Устанавливаем состояние ожидания суммы


# Обработка ввода суммы
@payment_router.message(PaymentState.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext, bot):

        # Проверяем, правильный ли формат суммы
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительным числом.")

        PRICE = LabeledPrice(label="Пополнение VoiceTran", amount=amount*100)
        await bot.send_invoice(message.chat.id,
                               title="Пополнение VoiceTran",
                               description="Пополнение возможности перевода голосовых сообщений",
                               provider_token=config.PAYMASTER,
                               currency="rub",
                               photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                               photo_width=416,
                               photo_height=234,
                               photo_size=416,
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="one-month-subscription",
                               payload="test-invoice-payload")

        # Сбрасываем состояние
        await state.clear()


@payment_router.message(F.successful_payment)
async def successful_payment(message: Message, bot):
    print("SUCCESSFUL PAYMENT:")

    update_balance(message.from_user.id, message.successful_payment.total_amount//100)
    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")

@payment_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@payment_router.message(Command("balance"))
async def balance(message: Message):
    await message.answer("💳" + str(get_balance(message.from_user.id)))