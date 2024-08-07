import socket
import threading

import typer
from rich import print

from config import SocketConfig
from utils.cli import clear_terminal


def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except Exception as e:
            print(f"error {e}")
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SocketConfig.HOST_IP, SocketConfig.HOST_PORT))

    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    while True:
        try:
            message = input()
            clear_terminal()
            client_socket.send(message.encode())
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == '__main__':
    typer.run(main)
