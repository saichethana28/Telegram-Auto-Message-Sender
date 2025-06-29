from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "BOT_TOKEN"

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Professor's Chat ID: {chat_id}")  # Shows in YOUR console
    await update.message.reply_text(f"🔍 Your Chat ID: {chat_id}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, show_id))
print("🆔 ID Collector is running...")
app.run_polling()
