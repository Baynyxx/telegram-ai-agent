import os
import socket
import webbrowser
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
ALLOWED_IP = os.getenv("ALLOWED_IP")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Сервер запущен на порту {PORT}")
    print(f"Разрешённый IP: {ALLOWED_IP}")

    while True:
        conn, addr = server.accept()

        client_ip = addr[0]

        if client_ip != ALLOWED_IP:
            print(f"Отклонено подключение от {client_ip}")
            conn.close()
            continue

        print(f"Подключение от {client_ip}")

        with conn:
            data = b""

            while True:
                chunk = conn.recv(1024)

                if not chunk:
                    break

                data += chunk

                if b"\n" in data:
                    break

            message = data.decode("utf-8").strip()

            count = message.count(":")
            if count == 1:
                parts = message.split(":", 2)
                token, command = parts
            elif count == 2:
                parts = message.split(":", 2)
                token, command, value = parts
            elif count >= 2:
                parts = message.split(":", 2)
                token, command, value = parts
            else:
                print("error")

            if command == "url":
                webbrowser.open(value)

            elif command == "open":
                print("Потом допилю")

            elif command == "power":
                if value == "off":
                    print("Выключение")
                elif value == "reboot":
                    print("Перезагрузка")