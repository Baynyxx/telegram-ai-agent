import webbrowser
import notifications
import subprocess
import notifications
import aspect_ratio
from programms_list import paths



def action(command: str, value: str):
    if command == "url":
        url(value)
    elif command == "open":
        open_programm(value)
    elif command == "power":
        power(value)
    elif command == "aspect":
        aspect(value)




def url(value: str):
    webbrowser.open(value)
    notifications.notify("Web", f"Открыто {value}")

def open_programm(value: str):
    if value in paths:
        exec(paths[value])
        notifications.notify("Programm", f"Открыто {value}")
    else:
        notifications.notify("Programm", f"Ошибка при запуске {value}")

def power(value: str):
    if value == "off":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    elif value == "reboot":
        subprocess.run(["shutdown", "/r", "/t", "0"])

def aspect(value: str):
    if value == "on":
        aspect_ratio.ratio(True)
        notifications.notify("Aspect Ratio", "Включен растяг")
    elif value == "off":
        aspect_ratio.ratio(False)
        notifications.notify("Aspect Ratio", "Выключен растяг")