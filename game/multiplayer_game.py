import time
from typing import Optional

from database.models import User
from repository.user_repository import user_repo
from utils.cli import clear_terminal
from .base import Game


class MultiplayerGame(Game):
    def __init__(self, client_socket, clients):
        self.client_socket = client_socket
        self.clients = clients

    def select_player(self) -> Optional[User]:
        users = user_repo.get_all()
        self.client_socket.send(
            "Please select the player you want to play as: (Tap enter to see the players....)\n".encode())
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

    def play(self):
        self.client_socket.send("How many players want to play ?: (MIN [bold red]2PLAYERS[/bold red])\n".encode())
        players_number = int(self.client_socket.recv(1024).decode())
        if players_number < 2:
            clear_terminal()
            self.client_socket.send("You need at least 2 players :)) [You can't play with yourself] 🤓\n".encode())
            return self.play()

        selected_players = {}
        for i in range(players_number):
            player = self.select_player()
            if not player:
                self.client_socket.send("[bold yellow]Create a user first[/bold yellow]\n".encode())
                return None
            selected_players[player] = 0

        while True:
            player_1 = random.choice(list(selected_players.keys()))
            player_2 = random.choice(list(selected_players.keys()))
            while player_1 == player_2:
                player_2 = random.choice(list(selected_players.keys()))

            self.client_socket.send(
                f"[bold red]{player_1.name}[/bold red] and [bold red]{player_2.name}[/bold red] will play for the first "
                f"round\n ".encode())
            self.client_socket.send("The game will start in 3s ...\n".encode())
            time.sleep(3)
            clear_terminal()
            self.client_socket.send(
                "1 - ROCK :video_game:\n2 - PAPER :video_game:\n3 - SCISSORS :video_game:\n".encode())

            player_1_socket = self.clients[0]
            player_1_socket.send(f"What is your choice: -👉{player_1.name}👈-\n".encode())
            player_1_choice = int(self.client_socket.recv(1024).decode())
            clear_terminal()

            player_2_socket = self.clients[1]
            player_2_socket.send(f"What is your choice: -👉{player_2.name}👈-\n".encode())
            player_2_choice = int(self.client_socket.recv(1024).decode())

            if player_1_choice in [1, 2, 3] and player_2_choice in [1, 2, 3]:
                winner = self.get_winner(player_1_choice, player_2_choice)
                if winner == player_1_choice:
                    self.client_socket.send(f"{player_1.name} won ! \n".encode())
                    selected_players[player_1] += 1
                else:
                    self.client_socket.send(f"{player_2.name} won ! \n".encode())
                    selected_players[player_2] += 1
            else:
                self.client_socket.send("You can enter a number between 1-3 to choose \n".encode())
                continue
            self.client_socket.send("Wanna play another match?: (yes-no)\n".encode())
            is_retry = self.client_socket.recv(1024).decode().lower()

            if is_retry == "no":
                break

        sorted_by_score_players = dict(sorted(selected_players.items(), key=lambda x: x[1], reverse=True))
        total_winner = next(iter(sorted_by_score_players.items()))[0]
        self.client_socket.send(f"Total winner is {total_winner.name}".encode())
        for player, score in selected_players.items():
            player.score += score
            user_repo.update(player)
