import socket
import threading

import typer

from settings.config import SocketConfig
from constants import *
from main import *


def handle_client(client_socket):
    while True:
        try:
            selected = main_menu(client_socket)
            if selected == MainMenuOption.START.value:
                selected_mode = start_game_menu(client_socket)
                if selected_mode == StartMenuOption.AI.value:
                    play__game_ai(client_socket)
                elif selected_mode == StartMenuOption.PLAYER.value:
                    # TODO Implement play__game_player with socket
                    pass
            elif selected == MainMenuOption.CREATE.value:
                create_player_menu(client_socket)
            elif selected == MainMenuOption.LEADERBOARD.value:
                leaderboard_menu(client_socket)
            else:
                client_socket.send("Goodbye :red_heart-emoji:".encode())
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((SocketConfig.HOST_IP, SocketConfig.HOST_PORT))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    typer.run(main)
