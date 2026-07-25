import os
import socket
from dotenv import load_dotenv
load_dotenv()

CONNECTION_IP = os.getenv("CONNECTION_IP")
CONNECTION_PORT = int(os.getenv("CONNECTION_PORT"))
CONNECTION_TOKEN = os.getenv("CONNECTION_TOKEN")

async def url(link: str):
    message = f"{CONNECTION_TOKEN}:url:{link}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CONNECTION_IP, CONNECTION_PORT))
            sock.sendall((message + "\n").encode("utf-8"))
            return("Ok")
    except Exception as e:
        print(e)
        return("Error")


async def open_programm(link: str):
    message = f"{CONNECTION_TOKEN}:open:{link}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CONNECTION_IP, CONNECTION_PORT))
            sock.sendall((message + "\n").encode("utf-8"))
            return("Ok")
    except Exception as e:
        print(e)
        return("Error")


async def power(link: str):
    message = f"{CONNECTION_TOKEN}:power:{link}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CONNECTION_IP, CONNECTION_PORT))
            sock.sendall((message + "\n").encode("utf-8"))
            return("Ok")
    except Exception as e:
        print(e)
        return("Error")

async def ratio(link: str):
    message = f"{CONNECTION_TOKEN}:aspect:{link}"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CONNECTION_IP, CONNECTION_PORT))
            sock.sendall((message + "\n").encode("utf-8"))
            return("Ok")
    except Exception as e:
        print(e)
        return("Error")

async def get_system_info():
    message = f"{CONNECTION_TOKEN}:get:system_info"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CONNECTION_IP, CONNECTION_PORT))
            sock.sendall((message + "\n").encode("utf-8"))

            data = sock.recv(2048)
            response = data.decode("utf-8")
            if response == "OK":
                return "System info error"
            else:
                return response
    except Exception as e:
        print(e)
        return("System info error")

async def get_focus():
    message = f"{CONNECTION_TOKEN}:get:focus"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CONNECTION_IP, CONNECTION_PORT))
            sock.sendall((message + "\n").encode("utf-8"))

            data = sock.recv(2048)
            response = data.decode("utf-8")
            if response == "OK":
                return "System focus error"
            else:
                return response
    except Exception as e:
        print(e)
        return("System focus error")