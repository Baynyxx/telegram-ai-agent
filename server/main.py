import os
import telegram_functions
from dotenv import load_dotenv
load_dotenv()

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from html import escape


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