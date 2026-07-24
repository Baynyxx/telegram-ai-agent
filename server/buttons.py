from telegram import Update, InlineQueryResultArticle, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode

async def main_menu():
    keyboard = [
        ["Воспоминания бота"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
    return reply_markup
