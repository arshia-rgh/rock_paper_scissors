import random
from enum import Enum
from typing import Optional
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


class BaseOption(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class MainMenuOption(Enum):
    START = 1
    CREATE = 2
    LEADERBOARD = 3
    EXIT = 4


class StartMenuOption(Enum):
    AI = 1
    PLAYER = 2
    BACK = 3


def main_menu() -> int:
    print("*****************************")
    print("*****[green]Welcome to our game[/green]*****")
    print("Please enter what do you want to do: ")
    print("1 - Start the game")
    print("2 - Create new player")
    print("3 - Check leaderboard")
    print("4 - Exit")
    option = int(input("Enter your option number: "))
    return option


def start_game_menu() -> int:
    print("Welcome --")
    print(":warning: [bold red] Note that you need to have at least one player to play any mode[/bold red] :warning:")
    print("1 - VS AI")
    print("2 - VS PLAYER")
    print("3 - Back to main")
    option = int(input("Enter your option number: "))
    return option


def create_player_menu():
    print("Please enter your name: ")
    name = input("Your Name 🙎🏻‍♂️ :  ")
    user = User(name)

    user.save_to_db()
    print(f"Player [blue]{user.name}[/blue] successfully added ! ")


def leaderboard_menu():
    users = User.list_db
    table = Table("Player", "Score")
    for user in users:
        table.add_row(user.name, str(user.score))
    print(table)


def select_player() -> Optional[User]:
    users = User.list_db
    print("Please select the player you want to plays as: ")
    if users:

        for i, user in enumerate(users, start=1):
            print(f"{i} - {user.name}")
        chosen_name = input("selected name: (Should write the name not the number)")
        for user in users:
            if user.name == chosen_name:
                clear_terminal()
                print(f"{chosen_name} player selected")
                return user
        clear_terminal()
        print("Wrong player")

        select_player()

    print("There is no players ... ! ")
    return None


def get_winner(p1_number: int, p2_number: int) -> Optional[int]:
    if p1_number == 1:
        if p2_number == 3:
            return p1_number
        elif p2_number == 2:
            return p2_number
        return None

    elif p1_number == 2:
        if p2_number == 1:
            return p1_number
        elif p2_number == 3:
            return p2_number
        return None

    else:
        if p2_number == 1:
            return p2_number
        elif p2_number == 2:
            return p1_number
        return None


def play__game_ai():
    player = select_player()
    if not player:
        print("[bold yellow]Create a user first[/bold yellow]")
        return None
    ai_score = 0
    player_score = 0
    while True:
        ai_number = random.randint(1, 3)
        print("1 - ROCK :video_game:")
        print("2 - PAPER :video_game:")
        print("3 - SCISSORS :video_game:")
        player_number = int(input("Which do you chose?: "))
        if player_number in [1, 2, 3] and ai_number in [1, 2, 3]:
            winner = get_winner(ai_number, player_number)
            if winner == player_number:
                player_score += 1
                clear_terminal()
                print("Congratulations you won :))))")
            else:
                clear_terminal()
                print("You lost ")
                ai_score += 1
        else:
            clear_terminal()
            print("You can enter number between 1-3 to chose ")
            continue

        is_retry = input("Wanna play another match?: (yes-no)").lower()

        if is_retry == "no":
            break

    player.score += player_score

    if player_score > ai_score:
        print("You won totally")
    elif player_score < ai_score:
        print("You lost totally")
    else:
        print("Draw")


def play__game_player():
    print("How many players want to play ?: (MIN [bold red]2PLAYERS[/bold red])")
    players_number = int(input("Select a number: "))
    if players_number < 2:
        clear_terminal()
        print("You need at least 2 player :)) [You cant play with yourself] 🤓")

        play__game_player()

    selected_players = []
    for i in range(players_number):
        player = select_player()
        if not player:
            print("[bold yellow]Create a user first[/bold yellow]")
            return None
        selected_players.append(player)


def main():
    while True:
        clear_terminal()
        selected = main_menu()
        clear_terminal()
        if selected == MainMenuOption.START.value:
            selected_mode = start_game_menu()
            clear_terminal()
            if selected_mode == StartMenuOption.AI.value:
                play__game_ai()
                print("Please enter to redirect to the [bold red]main menu[/bold red] ... ")
                input()
            elif selected_mode == StartMenuOption.PLAYER.value:
                play__game_player()
                input()

            else:
                continue
        elif selected == MainMenuOption.CREATE.value:
            create_player_menu()
            print("Please enter to redirect to the [bold red]main menu[/bold red] ... ")
            input()
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
