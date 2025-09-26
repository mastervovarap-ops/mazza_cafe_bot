
# Mazza Cafe Halal Telegram Bot

Цей бот створений для прийому замовлень у кафе **Mazza Cafe Halal**.
Він підтримує дві мови (укр/рос), показує меню, додає товари в кошик і збирає адресу та телефон для доставки.

## 🚀 Запуск на Railway

1. Створи новий репозиторій на GitHub та завантаж сюди ці файли.
2. У Railway натисни **New Project → Deploy from GitHub repo**.
3. Додай змінні у вкладці Variables:
   - `BOT_TOKEN = твій токен від BotFather`
   - `ADMIN_CHAT_ID = твій chat_id` (дізнаєшся, написавши команду `/whoami` у боті)
4. У полі Start Command напиши:
   ```
   python bot.py
   ```
5. Натисни **Deploy**. Бот працюватиме 24/7.

---

## 📦 Локальний запуск (для тесту)
```bash
pip install -r requirements.txt
python bot.py
```
