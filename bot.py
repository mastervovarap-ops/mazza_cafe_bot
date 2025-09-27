import os
import logging
from aiogram import Bot, Dispatcher, executor, types

# Логування
logging.basicConfig(level=logging.INFO)

# Змінні середовища
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

if not BOT_TOKEN:
    raise RuntimeError("Не задано BOT_TOKEN у змінних середовища")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привіт 👋 Це бот *Mazza Cafe*!\nНатисни /menu щоб побачити меню.", parse_mode="Markdown")

# Команда /menu
@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🥙 Шаурма", callback_data="order:Шаурма"))
    keyboard.add(types.InlineKeyboardButton("🍛 Плов", callback_data="order:Плов"))
    keyboard.add(types.InlineKeyboardButton("🥟 Чебурек", callback_data="order:Чебурек"))
    await message.answer("Оберіть страву:", reply_markup=keyboard)

# Обробка замовлення
@dp.callback_query_handler(lambda c: c.data.startswith("order:"))
async def process_order(callback: types.CallbackQuery):
    item = callback.data.split(":", 1)[1]
    user = callback.from_user

    order_text = f"🛒 Замовлення від @{user.username or user.id}\nСтрава: {item}"

    # Відправка адміну
    if ADMIN_USER_ID:
        try:
            await bot.send_message(ADMIN_USER_ID, order_text)
        except Exception as e:
            logging.error(f"Помилка відправки адміну: {e}")

    await callback.message.answer(f"✅ Ваше замовлення '{item}' прийняте!")
    await callback.answer()

# Запуск
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
