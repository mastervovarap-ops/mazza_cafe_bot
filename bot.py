
import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("Не задано BOT_TOKEN у .env")

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

LANG_UA = "uk"
LANG_RU = "ru"

STRINGS = {
    LANG_UA: {
        "greet": "Привіт! Обери мову / Выбери язык:",
        "menu": "Меню",
        "cart": "Кошик",
        "checkout": "Оформити замовлення",
        "back": "⬅️ Назад",
        "add_to_cart": "Додано в кошик ✅",
        "empty_cart": "Твій кошик порожній.",
        "cart_title": "🛒 Кошик",
        "total": "Разом",
        "ask_address": "Вкажи адресу доставки:",
        "ask_phone": "Вкажи номер телефону:",
        "order_sent": "Дякуємо! Замовлення надіслано адміну.",
        "whoami": "Твій chat_id: <code>{}</code>",
        "lang_set": "Мову встановлено: Українська 🇺🇦",
        "categories": {
            "first": "🍲 Перші страви",
            "second": "🍛 Другі страви",
            "main": "🍖 Основні страви"
        }
    },
    LANG_RU: {
        "greet": "Привет! Обери мову / Выбери язык:",
        "menu": "Меню",
        "cart": "Корзина",
        "checkout": "Оформить заказ",
        "back": "⬅️ Назад",
        "add_to_cart": "Добавлено в корзину ✅",
        "empty_cart": "Твоя корзина пуста.",
        "cart_title": "🛒 Корзина",
        "total": "Итого",
        "ask_address": "Укажи адрес доставки:",
        "ask_phone": "Укажи номер телефона:",
        "order_sent": "Спасибо! Заказ отправлен администратору.",
        "whoami": "Твой chat_id: <code>{}</code>",
        "lang_set": "Язык установлен: Русский 🇷🇺",
        "categories": {
            "first": "🍲 Первые блюда",
            "second": "🍛 Вторые блюда",
            "main": "🍖 Основные блюда"
        }
    }
}

# Скорочене меню для прикладу
MenuItem = Tuple[str, str, int]
MENU: Dict[str, List[MenuItem]] = {
    "first": [
        ("Чучвара", "Чучвара", 140),
        ("Шурпа", "Шурпа", 130),
    ],
    "second": [
        ("Долма", "Долма", 150),
        ("Плов узбецький", "Плов узбекский", 130),
    ],
    "main": [
        ("Шаурма середня", "Шаурма средняя", 150),
        ("Чебурек з яловичиною", "Чебурек с говядиной", 90),
    ],
}

@dataclass
class UserData:
    lang: str = LANG_UA
    cart: List[Tuple[str, int]] = None

USERS: Dict[int, UserData] = {}

class OrderFSM(StatesGroup):
    waiting_address = State()
    waiting_phone = State()

def get_user(u_id: int) -> UserData:
    if u_id not in USERS:
        USERS[u_id] = UserData(lang=LANG_UA, cart=[])
    if USERS[u_id].cart is None:
        USERS[u_id].cart = []
    return USERS[u_id]

@dp.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext):
    u = get_user(msg.from_user.id)
    await state.clear()
    await msg.answer(STRINGS[u.lang]["greet"])

@dp.message(Command("whoami"))
async def cmd_whoami(msg: Message):
    await msg.answer(STRINGS[get_user(msg.from_user.id).lang]["whoami"].format(msg.from_user.id))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
