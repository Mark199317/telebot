from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ==== НАСТРОЙКИ ====
# Замените BOT_TOKEN на токен вашего бота, полученный от @BotFather
BOT_TOKEN = "8013641652:AAFZglNhuQTLyEG8fQyPgekj4_W3UDkpauA"
# Замените ADMIN_ID на ваш Telegram ID (узнайте его с помощью команды /getid)
ADMIN_ID = 1182328199
# Ссылка на канал, куда будет перенаправлять кнопка "Подписаться на канал"
SUBSCRIBE_LINK = "https://t.me/+HSEhvUkkj2RhMTI6"
# Ссылка на баннер (для кнопки "Перейти")
BANNER_LINK = "https://replit.com/@markriznichok1/MDgroupBot#banner.jfif"
# Путь к локальному файлу баннера (убедитесь, что файл banner.jfif находится в той же папке, что и скрипт)
BANNER_FILE = "banner.jfif"
# Каналы-партнеры
PARTNER_LINKS = [
    ("Канал 1", "https://t.me/+dMRSBarO1rtiNTg6"),
    ("Канал 2", "https://t.me/+eFU5IODwDJxiYzYy"),
]

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Команда /start получена!")  # Для отладки

    # Создаем клавиатуру с двумя кнопками
    keyboard = [
        [InlineKeyboardButton("📢 Подписаться на канал", url=SUBSCRIBE_LINK)],
        [InlineKeyboardButton("🤝 Партнеры", callback_data="show_partners")],
    ]

    # Отправляем баннер (локальный файл)
    try:
        await update.message.reply_photo(
            photo=open(BANNER_FILE, "rb"),
            caption="🌻 Нажми на баннер, чтобы узнать больше!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔗 Перейти", url=BANNER_LINK)]]
            )
        )
    except FileNotFoundError:
        await update.message.reply_text("Ошибка: файл баннера не найден. Проверьте наличие banner.jfif.")
        return

    # Отправляем приветственное сообщение с клавиатурой
    await update.message.reply_text(
        "Привет! Добро пожаловать 👋\n\n"
        "Подпишись на наш канал или посмотри наших партнеров, используя кнопки ниже:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === Обработка кнопок ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_partners":
        text = "📣 Наши партнёрские каналы:\n\n"
        for name, link in PARTNER_LINKS:
            text += f"🔗 [{name}]({link})\n"
        await query.edit_message_text(text, parse_mode="Markdown")

# === Команда /getid ===
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ваш chat_id: {update.effective_chat.id}")

# === Запуск ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", get_id))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен...")
    app.run_polling()