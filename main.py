from enum import Enum

import typer
from rich import print

from utils.cli import clear_terminal


class User:
    dict_db = {}

    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score

    def increase_score(self):
        self.score += 1

    def save_to_db(self):
        self.dict_db[self.name] = self.score


class MainMenuOption(Enum):
    START = 1
    CREATE = 2
    LEADERBOARD = 3
    EXIT = 4


class ModeMenuOption(Enum):
    AI = 1
    PLAYER = 2
    BACK = 3


def main_menu():
    print("*****************************")
    print("*****[green]Welcome to our game[/green]*****")
    print("Please enter what do you want to do: ")
    print("1 - Start the game")
    print("2 - Create new player")
    print("3 - Check leaderboard")
    print("4 - Exit")
    option = int(input("Enter your option number: "))
    return option


def start_game_menu():
    print("Welcome --")
    print(":warning: [bold red] Note that you need to have at least one player to play any mode[/bold red] :warning:")
    print("1 - VS AI")
    print("2 - VS PLAYER")
    print("3 - Back to main")
    option = int(input("Enter your option number: "))
    return option


def create_player_menu():
    print("Please chose the game mode you want: ")


def main():
    while True:
        clear_terminal()
        selected = main_menu()
        if selected == MainMenuOption.START.value:
            selected_mode = start_game_menu()
            pass
        elif selected == MainMenuOption.CREATE.value:
            pass
        elif selected == MainMenuOption.LEADERBOARD.value:
            pass
        else:
            print("Goodbye :)")


if __name__ == '__main__':
    typer.run(main)
