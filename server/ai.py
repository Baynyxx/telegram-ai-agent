from openai import OpenAI

from datetime import datetime
from pathlib import Path
import json
import os
import config
from dotenv import load_dotenv
load_dotenv()

AI_HTTP = os.getenv("AI_HTTP")
AI_TOKEN = os.getenv("AI_TOKEN")

MEMORY_FILE = Path("memory.json")


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

async def ask_gpt(message: str, history: list, sys: str):
    now = datetime.now()
    history.append({
        "role": "user",
        "content": f"{message} MESSAGE TIME: {now.strftime("%Y-%m-%d %H:%M:%S")} MEMORIES: {memory}"
    })

    messages = [
        {"role": "system", "content": sys},
        *history[-30:],
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )

    answer = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": answer
    })

    if len(history) > 30:
        del history[:-30]

    answer = answer.replace("***", "")
    return answer