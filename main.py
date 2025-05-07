import os
import logging
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, save_entry, get_entries_by_user
from mood_analysis import analyze_mood

TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-дневник SoulLog. Напиши /new чтобы добавить запись.")

async def new_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши свою запись, и я сохраню её.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    save_entry(user_id, text)
    mood = analyze_mood(text)
    await update.message.reply_text(f"Запись сохранена. Настроение: {mood}")

async def list_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    entries = get_entries_by_user(user_id)
    if entries:
        await update.message.reply_text("\n\n".join(f"{e[2]}: {e[3]}" for e in entries))
    else:
        await update.message.reply_text("Записей пока нет.")

if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_entry))
    app.add_handler(CommandHandler("list", list_entries))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
