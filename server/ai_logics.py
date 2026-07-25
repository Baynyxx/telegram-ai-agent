import config
import re
import ai
import client_communications
import telegram_functions

sys = config.SYS_PROMPT
history = []

async def process_ai_output(text: str):
    edited = False
    si = None
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
        elif name == "get":
            if value == "system_info":
                si = await client_communications.get_system_info()
                if si != "Error":
                    if si != "System info error":
                        await telegram_functions.ai_executed(f"Бот запросил сведения о системе")
                    else:
                        await telegram_functions.ai_executed("Ошибка")
                    rs = await ask(si)
                    return rs
                else:
                    await telegram_functions.ai_executed("Ошибка")
            if value == "focus":
                si = await client_communications.get_focus()
                if si != "Error":
                    if si != "System focus error":
                        await telegram_functions.ai_executed(f"Бот запросил фокус")
                    else:
                        await telegram_functions.ai_executed("Ошибка")
                    rs = await ask(si)
                    return rs
                else:
                    await telegram_functions.ai_executed("Ошибка")
                    

        text = text.replace(
            f"[{name}:{value}]",
            "",
            1
        )
    if text == "" or text == " ":
        text = "В этом нет текста."
    
    return text

async def ask(text:str, reply=None):
    if reply != None:
        ans = await ai.ask_gpt(text, history, sys, reply=reply)
    else:
        ans = await ai.ask_gpt(text, history, sys)
    processed = await process_ai_output(ans)
    if processed != "wait":
        return processed
