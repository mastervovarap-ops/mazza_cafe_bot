import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- Меню ---
MENU = {
    "🥘 Другі страви": [
        "Долма – 150 грн",
        "Кавурма-лагман – 160 грн",
        "Плов узбецький – 130 грн",
        "Манти – 130 грн"
    ],
    "🍲 Перші страви": [
        "Чучвара – 140 грн",
        "Шурпа – 130 грн",
        "Лагман – 150 грн",
        "Мастава – 130 грн"
    ],
    "🍖 Основні страви": [
        "Салат грецький – 80 грн",
        "Салат овочевий – 70 грн",
        "Шашлик з куркою – 150 грн",
        "Шашлик з яловичиною – 160 грн",
        "Чебурек з яловичиною – 90 грн",
        "Чебурек з сиром – 90 грн",
        "Чебурек міх – 110 грн",
        "Шаурма міні – 120 грн",
        "Шаурма середня – 150 грн",
        "Шаурма подвійна – 170 грн"
    ]
}


# --- Команди ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*MENU.keys())
    await message.answer("Вітаю 👋\nОберіть категорію страв:", reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text in MENU.keys())
async def show_category(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in MENU[message.text]:
        keyboard.add(item)
    keyboard.add("⬅️ Назад")
    await message.answer(f"{message.text}\nОберіть страву:", reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text in sum(MENU.values(), []))
async def order(message: types.Message):
    await message.answer(f"✅ Ви замовили: {message.text}\nАдмін скоро з вами зв’яжеться 📞")
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"Нове замовлення: {message.text}\nВід @{message.from_user.username}")


@dp.message_handler(lambda msg: msg.text == "⬅️ Назад")
async def back(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*MENU.keys())
    await message.answer("🔙 Повернулись у головне меню:", reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
