import os
import config
import telegram_functions
from dotenv import load_dotenv
load_dotenv()

from telegram import Update, InlineQueryResultArticle, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode
from html import escape

from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
CONNECTION_TOKEN = os.getenv("CONNECTION_TOKEN")

app = None


def main():
    global app
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", telegram_functions.start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_functions.text))
    print("Running")
    telegram_functions.get_app(app)
    app.run_polling()


if __name__ == "__main__":
    main()