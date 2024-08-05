import random
import time
from typing import Optional
from constants import *
import typer
from rich import print
from rich.table import Table

from utils.cli import clear_terminal
from user_repository import user_repo
from database.models import User


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
    if not name:
        clear_terminal()
        print("Name must contain at least one character")

        create_player_menu()

    user = user_repo.create(User(name=name))
    if isinstance(user, Exception):
        print(f"Error creating user: {user}")
    else:
        print(f"Player [blue]{user.name}[/blue] successfully added ! ")


def leaderboard_menu():
    users = user_repo.get_all()
    table = Table("Player", "Score")
    for user in users:
        table.add_row(user.name, str(user.score))
    print(table)


def select_player() -> Optional[User]:
    users = user_repo.get_all()
    print("Please select the player you want to plays as: ")
    if users:

        for i, user in enumerate(users, start=1):
            print(f"{i} - {user.name}")
        chosen_name = input("selected name: (Should write the name not the number)")
        for user in users:
            if user.name == chosen_name:
                clear_terminal()
                print(f" 🙎‍♂️ {chosen_name} player selected 🙎‍♂️ ")
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
    user_repo.update(player)

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

    selected_players = {}
    for i in range(players_number):
        player = select_player()
        if not player:
            print("[bold yellow]Create a user first[/bold yellow]")
            return None
        selected_players[player] = 0

    while True:
        player_1 = random.choice(list(selected_players.keys()))
        player_2 = random.choice(list(selected_players.keys()))
        while player_1 == player_2:
            player_2 = random.choice(list(selected_players.keys()))

        print(f"[bold red]{player_1.name}[/bold red] and [bold red]{player_2.name}[/bold red] will play for the first "
              f"round ")
        print("The game will be start in 3s ...")
        time.sleep(3)
        clear_terminal()
        print("1 - ROCK :video_game:")
        print("2 - PAPER :video_game:")
        print("3 - SCISSORS :video_game:")
        player_1_choice = int(input(f"What is your choice: -👉{player_1.name}👈-\n"))
        clear_terminal()
        player_2_choice = int(input(f"What is your choice: -👉{player_2.name}👈-\n"))

        if player_1_choice in [1, 2, 3] and player_2_choice in [1, 2, 3]:
            winner = get_winner(player_1_choice, player_2_choice)
            if winner == player_1_choice:
                print(f"{player_1.name} won ! ")
                selected_players[player_1] += 1
            else:
                print(f"{player_2.name} won ! ")
                selected_players[player_2] += 1
        else:
            print("You can enter number between 1-3 to chose ")
            continue

        is_retry = input("Wanna play another match?: (yes-no)").lower()

        if is_retry == "no":
            break
    sorted_by_score_players = dict(sorted(selected_players.items(), key=lambda x: x[1]))
    total_winner = next(iter(sorted_by_score_players.items()))[0]
    print(f"Total winner is {total_winner.name}")
    for player, score in selected_players.items():
        player.score += score
        user_repo.update(player)


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
                print("Please enter to redirect to the [bold red]main menu[/bold red] ... ")
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
