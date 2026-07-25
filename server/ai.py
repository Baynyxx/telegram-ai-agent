import asyncio
import json
import os
import config
import telegram_functions
from openai import OpenAI, InternalServerError
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
load_dotenv()

AI_HTTP = os.getenv("AI_HTTP")
AI_TOKEN = os.getenv("AI_TOKEN")
AI_HTTP2 = os.getenv("AI_HTTP2")
AI_TOKEN2 = os.getenv("AI_TOKEN2")

MEMORY_FILE = Path("memory.json")
HISTORY_FILE = "chat_history.json"   # имя файла для хранения истории

MODE = 1

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_memory() -> set[str]:
    if not MEMORY_FILE.exists():
        return {
            f"Пользователя зовут {config.USER_NAME}",
            f"Меня зовут {config.AI_NAME}"
        }

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            return set(json.load(file))

    except (json.JSONDecodeError, OSError):
        return {
            f"Пользователя зовут {config.USER_NAME}",
            f"Меня зовут {config.AI_NAME}"
        }


def save_memory():
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            list(memory),
            file,
            ensure_ascii=False,
            indent=4
        )


memory = load_memory()


async def remember(fact: str):
    memory.add(fact)
    save_memory()

    return "Ok"


async def forget(fact: str):
    memory.discard(fact)
    save_memory()

    return "Ok"


client = OpenAI(
    base_url=AI_HTTP,
    api_key=AI_TOKEN
)

client2 = OpenAI(
    base_url=AI_HTTP2,
    api_key=AI_TOKEN2
)
async def ask_gpt(message: str, history: list, sys: str, reply=None):
    if MODE == 1:
        answer = await ask(message, history, sys, reply=reply)
    elif MODE == 2:
        answer = await ask2(message, history, sys, reply=reply)
    return answer


async def ask(message: str, history: list, sys: str, reply=None):
    global MODE
    try:
        await telegram_functions.texting()
        moscow_tz = ZoneInfo("Europe/Moscow")
        now_moscow = datetime.now(moscow_tz)
        formatted_time = now_moscow.strftime("%Y-%m-%d %H:%M:%S")

        if not history:
            history.extend(load_history())

        now = datetime.now()
        if reply is not None:
            history.append({
                "role": "user",
                "content": f"{message} MESSAGE TIME: {formatted_time} MEMORIES: {memory} REPLY TO: {reply}"
            })
        else:
            history.append({
                "role": "user",
                "content": f"{message} MESSAGE TIME: {formatted_time} MEMORIES: {memory}"
            })

        messages = [
            {"role": "system", "content": sys},
            *history[-30:],
        ]

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="deepseek-expert",
            messages=messages,
            extra_body={"thinking": False, "search": True},
        )

        answer = response.choices[0].message.content

        history.append({
            "role": "assistant",
            "content": answer
        })

        if len(history) > 30:
            del history[:-30]

        save_history(history)
        if answer == "":
            del history[-1]
            del history[-1]
            answer = await ask2(message, history, sys, reply=reply)
        else:
            MODE = 1
        return answer
    except InternalServerError:
        MODE = 2
        answer = await ask2(message, history, sys, reply=reply)
        return answer

async def ask2(message: str, history: list, sys: str, reply=None):
    try:
        await telegram_functions.texting()
        moscow_tz = ZoneInfo("Europe/Moscow")
        now_moscow = datetime.now(moscow_tz)
        formatted_time = now_moscow.strftime("%Y-%m-%d %H:%M:%S")

        if not history:
            history.extend(load_history())

        now = datetime.now()
        if reply is not None:
            history.append({
                "role": "user",
                "content": f"{message} MESSAGE TIME: {formatted_time} MEMORIES: {memory} REPLY TO: {reply}"
            })
        else:
            history.append({
                "role": "user",
                "content": f"{message} MESSAGE TIME: {formatted_time} MEMORIES: {memory}"
            })

        messages = [
            {"role": "system", "content": sys},
            *history[-30:],
        ]

        response = await asyncio.to_thread(
            client2.chat.completions.create,
            model="deepseek-expert",
            messages=messages,
            extra_body={"thinking": False, "search": True},
        )

        answer = response.choices[0].message.content

        history.append({
            "role": "assistant",
            "content": answer
        })

        if len(history) > 30:
            del history[:-30]

        save_history(history)
        if answer == "":
            del history[-1]
            del history[-1]
            return "Server error"
        else:
            MODE = 1
        return answer
    except Exception:
        return "Server error"