from typing import Optional

from database.models import User
from repository.user_repository import user_repo
from utils.cli import clear_terminal


class Game:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def get_winner(self, p1_number: int, p2_number: int) -> Optional[int]:
        win_conditions = {
            1: {2: 2, 3: 1},
            2: {1: 2, 3: 3},
            3: {1: 1, 2: 3},
        }
        # if p1_number == 1:
        #     if p2_number == 3:
        #         return p1_number
        #     elif p2_number == 2:
        #         return p2_number
        #     return None
        #
        # elif p1_number == 2:
        #     if p2_number == 1:
        #         return p1_number
        #     elif p2_number == 3:
        #         return p2_number
        #     return None
        #
        # else:
        #     if p2_number == 1:
        #         return p2_number
        #     elif p2_number == 2:
        #         return p1_number
        #     return None

        return win_conditions.get(p1_number, {}).get(p2_number)

    def select_player(self, *args) -> Optional[User]:
        users = user_repo.get_all()
        self.client_socket.send(
            "Please select the player you want to play as: (ENTER THE NAME NOT NUMBER)\n".encode())
        if users:
            for i, user in enumerate(users, start=1):
                self.client_socket.send(f"{i} - {user.name} \n".encode())
            chosen_name = self.client_socket.recv(1024).decode()
            for user in users:
                if user.name == chosen_name:
                    clear_terminal()
                    self.client_socket.send(f" 🙎‍♂️ {chosen_name} player selected 🙎‍♂️ ".encode())
                    return user
            clear_terminal()
            self.client_socket.send("Wrong player".encode())
            return self.select_player()

        self.client_socket.send("There are no players ... !".encode())
        return None
