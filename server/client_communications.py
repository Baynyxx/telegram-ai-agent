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