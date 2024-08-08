import random

from repository.user_repository import user_repo
from utils.cli import clear_terminal
from .base import Game


class SoloGame(Game):

    def play(self):
        player = self.select_player()
        if not player:
            self.client_socket.send("[bold yellow]Create a user first[/bold yellow]".encode())
            return None
        ai_score = 0
        player_score = 0
        while True:
            ai_number = random.randint(1, 3)
            menu = (
                "1 - ROCK :video_game: \n"
                "2 - PAPER :video_game:\n"
                "3 - SCISSORS :video_game:\n"
                "Which do you choose?: \n"
            )
            self.client_socket.send(menu.encode())
            player_number = int(self.client_socket.recv(1024).decode())
            if player_number in [1, 2, 3] and ai_number in [1, 2, 3]:
                winner = self.get_winner(ai_number, player_number)
                if winner == player_number:
                    player_score += 1
                    clear_terminal()
                    self.client_socket.send("Congratulations you won :))))".encode())
                else:
                    clear_terminal()
                    self.client_socket.send("You lost ".encode())
                    ai_score += 1
            else:
                clear_terminal()
                self.client_socket.send("You can enter a number between 1-3 to choose ".encode())
                continue

            self.client_socket.send("Wanna play another match?: (yes-no)".encode())
            is_retry = self.client_socket.recv(1024).decode().lower()

            if is_retry == "no":
                break

        player.score += player_score
        user_repo.update(player)

        if player_score > ai_score:
            self.client_socket.send("You won totally".encode())
        elif player_score < ai_score:
            self.client_socket.send("You lost totally".encode())
        else:
            self.client_socket.send("Draw".encode())
