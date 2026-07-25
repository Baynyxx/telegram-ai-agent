from telegram import ReplyKeyboardMarkup

async def main_menu():
    keyboard = [
        ["Воспоминания бота"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
    return reply_markup
