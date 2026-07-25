import asyncio
import os
import config
import buttons
import ai_logics
from dotenv import load_dotenv
load_dotenv()
from ai import memory
from telegram import Update, constants
from telegram.ext import ContextTypes

OWNER_ID = os.getenv("OWNER_ID")

app = None
last_message = None
name_change = False
# Functions

def get_app(appg):
    global app
    app = appg

def is_owner(update: Update):
    return update.effective_user.id == int(OWNER_ID)

async def ai_executed(text: str):
    if text != "Ошибка":
        await send_tg(f"✅ {text}")
    else:
        await send_tg(f"⛔ {text}")

async def edit_devide(text: str):
    count = text.count("|||")
    if count > 0:
        parts = text.split("|||")
        for i, part in enumerate(parts):
            await texting()
            if i == 0:
                await send_tg(part)
                await asyncio.sleep(1)
            else:
                await send_tg(part)
                await asyncio.sleep(1)
    else:
        await send_tg(text)


async def send_tg(text: str, reply_markup=None, parse_mode="HTML"):
    if not text:
        return
    try:
        msg = await app.bot.send_message(
            chat_id=OWNER_ID,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        return msg.message_id
    except Exception as e:
        print("Telegram error:", e)


async def edit_tg(text: str, id: int, reply_markup=None, parse_mode="HTML"):
    if not text:
        return
    try:
        await app.bot.edit_message_text(
            chat_id=OWNER_ID,
            message_id=id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        return id
    except Exception as e:
        print("Telegram error:", e)

async def texting():
    await app.bot.send_chat_action(
        chat_id=OWNER_ID, 
        action=constants.ChatAction.TYPING
    )

# User commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    global last_message
    keyboard = await buttons.main_menu()
    await send_tg(f"Привет {config.USER_NAME}!", reply_markup=keyboard)

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    global last_message
    global name_change
    message = update.message
    user_text = update.message.text
    if user_text == "Настройки":
        keyboard = await buttons.settings()
        await send_tg(f"Настройки:", reply_markup=keyboard)

    elif user_text == "Воспоминания бота":
        memory_text = "\n".join(
            f"• {fact}"
            for fact in memory
        )
        await send_tg(memory_text)

    elif user_text == "Назад":
        keyboard = await buttons.main_menu()
        await send_tg(f"Главное меню:", reply_markup=keyboard)


    else:
        if message.reply_to_message:
            original_message = message.reply_to_message
            ans = await ai_logics.ask(user_text, reply=original_message.text)
        else:
            ans = await ai_logics.ask(user_text)
        await edit_devide(ans)
        
