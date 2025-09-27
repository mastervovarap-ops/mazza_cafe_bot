import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from dotenv import load_dotenv

# Завантажуємо змінні локально (.env)
load_dotenv()

# Читаємо змінні з середовища (Render або .env)
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

if not BOT_TOKEN:
    raise RuntimeError("❌ Не знайдено BOT_TOKEN")

# Логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# Стан для FSM
class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_phone = State()

# Кошик користувача
user_cart = {}

# Меню категорій
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥘 Перші страви", callback_data="cat_first")],
        [InlineKeyboardButton(text="🍖 Другі страви", callback_data="cat_second")],
        [InlineKeyboardButton(text="🥗 Салати", callback_data="cat_salad")],
        [InlineKeyboardButton(text="🛒 Переглянути кошик", callback_data="cart")],
    ])
    return kb

# Старт
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привіт 👋 Я бот Mazza Cafe! Обери категорію:", reply_markup=main_menu())

# Обробка категорій
@dp.callback_query(lambda c: c.data.startswith("cat_"))
async def category_handler(callback: types.CallbackQuery):
    category = callback.data
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Страва 1", callback_data=f"add_{category}_1")],
        [InlineKeyboardButton(text="➕ Страва 2", callback_data=f"add_{category}_2")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu")],
    ])
    await callback.message.edit_text("Оберіть страву:", reply_markup=kb)

# Додавання у кошик
@dp.callback_query(lambda c: c.data.startswith("add_"))
async def add_to_cart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    item = callback.data.replace("add_", "")
    user_cart.setdefault(user_id, []).append(item)
    await callback.answer("✅ Додано у кошик!")

# Показати кошик
@dp.callback_query(lambda c: c.data == "cart")
async def show_cart(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    items = user_cart.get(user_id, [])
    if not items:
        await callback.message.edit_text("🛒 Ваш кошик порожній.", reply_markup=main_menu())
        return
text = "📋 Ваше замовлення:\n" + "\n".join([f"- {i}" for i in items])
text += "\n\nВведіть своє ім'я:"

    await state.set_state(OrderState.waiting_for_name)
    await callback.message.edit_text(text)

# Отримати ім’я
@dp.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderState.waiting_for_address)
    await message.answer("Введіть адресу:")

# Отримати адресу
@dp.message(OrderState.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(OrderState.waiting_for_phone)
    await message.answer("Введіть номер телефону:")

# Отримати телефон і підтвердити
@dp.message(OrderState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    name, address, phone = data["name"], data["address"], message.text
    items = user_cart.get(user_id, [])
    
    order_text = (
        f"📦 <b>Нове замовлення!</b>\n\n"
        f"👤 Ім’я: {name}\n"
        f"📍 Адреса: {address}\n"
        f"📞 Телефон: {phone}\n\n"
        f"🛒 Замовлення:\n" + "\n".join([f"- {i}" for i in items])
    )

    # Відправка адміну
    if ADMIN_USER_ID:
        try:
            await bot.send_message(int(ADMIN_USER_ID), order_text)
        except Exception as e:
            logging.error(f"Помилка відправки адміну: {e}")

    # Відправка клієнту
    await message.answer("✅ Дякуємо! Ваше замовлення прийнято.")
    user_cart[user_id] = []
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
