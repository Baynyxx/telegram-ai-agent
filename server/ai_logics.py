import config
import re
import ai
import client_communications
import telegram_functions

sys = config.SYS_PROMPT
history = []

async def process_ai_output(text: str):
    edited = False
    text = text
    for name, value in re.findall(r"\[([^:]+):([^\]]+)\]", text):

        if name == "url":
            a = await client_communications.url(value)
            if a != "Error":
                await telegram_functions.ai_executed(f"Открыто {value}")
            else:
                await telegram_functions.ai_executed("Ошибка")

        elif name == "open":
            a = await client_communications.open_programm(value)
            if a != "Error":
                await telegram_functions.ai_executed(f"Открыто {value}")
            else:
                await telegram_functions.ai_executed("Ошибка")
            

        elif name == "power":
            a = await client_communications.power(value)
            if a != "Error":
                await telegram_functions.ai_executed(f"Выполнено {value}")
            else:
                await telegram_functions.ai_executed("Ошибка")

        elif name == "aspect":
            a = await client_communications.ratio(value)
            if a != "Error":
                await telegram_functions.ai_executed("Разрешение применено")
            else:
                await telegram_functions.ai_executed("Ошибка")

        elif name == "remember":
            a = await ai.remember(value)
            if a != "Error":
                await telegram_functions.ai_executed(f"Бот запомнил: {value}")
            else:
                await telegram_functions.ai_executed("Ошибка")

        elif name == "forget":
            a = await ai.forget(value)
            if a != "Error":
                await telegram_functions.ai_executed(f"Бот забыл: {value}")
            else:
                await telegram_functions.ai_executed("Ошибка")

        text = text.replace(
            f"[{name}:{value}]",
            "",
            1
        )
    if text == "":
        text = "Ok"
    
    return text

async def ask(text):
    ans = await ai.ask_gpt(text, history, sys)
    processed = await process_ai_output(ans)
    return processed
