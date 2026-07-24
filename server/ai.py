from openai import OpenAI

from datetime import datetime

import os
import config
from dotenv import load_dotenv
load_dotenv()

AI_HTTP = os.getenv("AI_HTTP")
AI_TOKEN = os.getenv("AI_TOKEN")

client = OpenAI(
    base_url=AI_HTTP,
    api_key=AI_TOKEN
)

async def ask_gpt(message: str, history: list, sys: str):
    now = datetime.now()
    history.append({
        "role": "user",
        "content": f"{message} MESSAGE TIME: {now.strftime("%Y-%m-%d %H:%M:%S")}"
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