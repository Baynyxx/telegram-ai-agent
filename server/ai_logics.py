import config
import re
import ai
import client_communications
import telegram_functions

name = config.AGENT_DEFAULT_NAME
sys = config.SYS_PROMPT
history = []

async def process_ai_output(text: str):
    edited = False
    text = text
    for name, value in re.findall(r"\[([^:]+):([^\]]+)\]", text):

        if name == "url":
            a = await client_communications.url(value)
            if a != "Error":
                await telegram_functions.ai_executed(value)
            else:
                await telegram_functions.ai_executed("Ошибка")

        if name == "open":
            a = await client_communications.open_programm(value)
            if a != "Error":
                await telegram_functions.ai_executed(value)
            else:
                await telegram_functions.ai_executed("Ошибка")
            

        if name == "power":
            a = await client_communications.power(value)
            if a != "Error":
                await telegram_functions.ai_executed(value)
            else:
                await telegram_functions.ai_executed("Ошибка")

        text = text.replace(
            f"[{name}:{value}]",
            "[Выполнено]",
            1
        )
    return text

async def ask(text):
    ans = await ai.ask_gpt(text, history, sys)
    processed = await process_ai_output(ans)
    return processed
