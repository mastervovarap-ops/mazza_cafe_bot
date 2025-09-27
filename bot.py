from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# 🔑 Твій токен
BOT_TOKEN = "8443371276:AAF4Cd6GLVj4xwLneIu8hDAE8UTOsYTEJ8c"

# Створення бота
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# 👋 Команда /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привіт! 👋 Я бот для Mazza Cafe.")

# 🚀 Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
