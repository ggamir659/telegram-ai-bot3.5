from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

# Берём ключи из переменных окружения Render
TELEGRAM_TOKEN = os.environ["7532910236:AAEO4IILuS_iLdmnXUBAov2hyx0LGY3dK-o"]
OPENROUTER_API_KEY = os.environ["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"]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я умный бот с ИИ 🤖. Спроси меня что-нибудь!")

# Обработка всех обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print("Пришло сообщение:", user_message)

    # Запрос к OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Отвечай дружелюбно и вежливо."},
                {"role": "user", "content": user_message}
            ]
        }
    )

    result = response.json()
    ai_reply = result["choices"][0]["message"]["content"]

    await update.message.reply_text(ai_reply)

# Создаём бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Бот с ИИ запущен. Ждёт сообщений...")
app.run_polling()
