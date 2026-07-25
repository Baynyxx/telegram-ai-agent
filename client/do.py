import ctypes
from ctypes import wintypes
import json
import shutil
import webbrowser
import winreg
import GPUtil
import psutil
import notifications
import subprocess
import notifications
import aspect_ratio
import keyboard
import os
import aspect_ratio_config
from pynput import keyboard
from programms_list import paths

valo = False

key = winreg.OpenKey(
    winreg.HKEY_LOCAL_MACHINE,
    r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
)

cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")

try:
    import wmi
    W = wmi.WMI(namespace="root\\LibreHardwareMonitor")
    
    
except:
    W = None

def action(command: str, value: str):
    resp = None
    if command == "url":
        url(value)
    elif command == "open":
        open_programm(value)
    elif command == "power":
        power(value)
    elif command == "aspect":
        aspect(value)
    elif command == "get":
        if value == "system_info":
            resp = get_system_info()
        elif value == "focus":
            resp = get_focus()
    
    if resp == None:
        return "OK"
    else:
        return resp




def url(value: str):
    try:
        webbrowser.open(value)
        notifications.notify("Web", f"Открыто {value}")
    except:
        pass

def open_programm(value: str):
    try:
        exec(paths[value])
        notifications.notify("Programm", f"Открыто {value}")    
    except Exception as e:
        print(e)
        notifications.notify("Programm", f"{e}")

def power(value: str):
    if value == "off":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    elif value == "reboot":
        subprocess.run(["shutdown", "/r", "/t", "0"])

def aspect(value: str):
    global valo
    try:
        if value == "on":
            valo = True
            aspect_ratio.ratio(True)
            notifications.notify("Aspect Ratio", f"Режим {aspect_ratio_config.ASPECT_W}x{aspect_ratio_config.ASPECT_H}")
    
        elif value == "off":
            valo = False
            aspect_ratio.ratio(False)
            notifications.notify("Aspect Ratio", f"Режим {aspect_ratio_config.DEFAULT_W}x{aspect_ratio_config.DEFAULT_H}")
    except:
        pass

def on_press(key):
    global valo
    try:
        if key == keyboard.Key.f24:
            if valo == True:
                aspect("off")
            elif valo == False:
                aspect("on")
                
            
    except AttributeError:
        pass


def get_system_info():
    global cpu
    data = {}
    
    # CPU
    data["cpu"] = {
        "name": cpu_name.strip(),
        "load": psutil.cpu_percent(interval=0.5),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True)
    }

    # RAM
    ram = psutil.virtual_memory()
    data["ram"] = {
        "used_gb": round(ram.used / 1024**3, 2),
        "total_gb": round(ram.total / 1024**3, 2),
        "percent": ram.percent
    }

    # Диск
    disk = shutil.disk_usage("/")
    data["disk"] = {
        "used_gb": round(disk.used / 1024**3, 2),
        "total_gb": round(disk.total / 1024**3, 2),
        "percent": round(disk.used / disk.total * 100, 1)
    }

    # GPU
    try:
        gpus = GPUtil.getGPUs()

        if gpus:
            gpu = gpus[0]

            data["gpu"] = {
                "name": gpu.name,
                "load": round(gpu.load * 100, 1),
                "memory_used_mb": gpu.memoryUsed,
                "memory_total_mb": gpu.memoryTotal,
                "temperature": gpu.temperature
            }
        else:
            data["gpu"] = None

    except:
        data["gpu"] = None

    # Температуры CPU (LibreHardwareMonitor)
    cpu_temp = None

    if W:
        try:
            sensors = W.Sensor()

            for sensor in sensors:
                if sensor.SensorType == "Temperature":
                    if "CPU Package" in sensor.Name:
                        cpu_temp = sensor.Value
                        break
        except:
            pass

    data["cpu_temperature"] = cpu_temp
    notifications.notify("System", f"Запрошены сведения о системе") 
    return json.dumps(data)


def get_focus():
    try:
        user32 = ctypes.windll.user32

        # HWND активного окна
        hwnd = user32.GetForegroundWindow()

        if not hwnd:
            return b"NO WINDOW"

        # PID процесса
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        process = psutil.Process(pid.value)

        exe = process.name()
        title = process.exe()
        notifications.notify("System", f"Запрошен фокус")
        return f"{exe}|{title}"

    except Exception as e:
        return None