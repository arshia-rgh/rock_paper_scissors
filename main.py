from enum import Enum

import typer
from rich import print
from rich.table import Table

from utils.cli import clear_terminal


class User:
    list_db = []

    def __init__(self, name: str, score: int = 0):
        self.name = name
        self.score = score

    def increase_score(self):
        self.score += 1

    def save_to_db(self):
        self.list_db.append(self)

    def __repr__(self):
        return f"User({self.name})"


class MainMenuOption(Enum):
    START = 1
    CREATE = 2
    LEADERBOARD = 3
    EXIT = 4


class StartMenuOption(Enum):
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
    print("Please enter your name: ")
    name = input("Your Name: :pause_button:")
    user = User(name)

    user.save_to_db()
    print(f"Player [blue]{user.name}[/blue] successfully added ! ")


def leaderboard_menu():
    users = User.list_db
    table = Table("Player", "Score")
    for user in users:
        table.add_row(user.name, user.score)
    print(table)


def play__game_player():
    pass


def select_player():
    users = User.list_db
    print("Please select the player you want to plays as: ")
    if users:

        for user in users:
            i = 1
            text = f"{1} - {user.name}"
            print(text)
            i += 1
        chosen_name = input("selected name: (Should write the name not the number)")
        if isinstance(chosen_name, str) and chosen_name in User.list_db:
            print(f"{chosen_name} player selected")
            return chosen_name

        return "Wrong player"

    return "There is no players ... ! "


def play__game_ai():
    player = select_player()


def main():
    while True:
        clear_terminal()
        selected = main_menu()
        clear_terminal()
        if selected == MainMenuOption.START.value:
            selected_mode = start_game_menu()
            if selected_mode == StartMenuOption.AI.value:
                pass
            elif selected_mode == StartMenuOption.PLAYER.value:
                pass

            else:
                continue
        elif selected == MainMenuOption.CREATE.value:
            create_player_menu()
            print("Please enter to redirect to the [bold red]main menu[/bold red] ... ")
            input("")
            continue
        elif selected == MainMenuOption.LEADERBOARD.value:
            leaderboard_menu()
            print("Please enter to redirect to the [bold red]main menu[/bold red] ... ")
            input()
            continue
        else:
            print("Goodbye :red_heart-emoji:")
            break


if __name__ == '__main__':
    typer.run(main)
