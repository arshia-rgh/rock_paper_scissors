import random
import time
from typing import Optional

from rich import print
from rich.console import Console
from rich.table import Table

from database.models import User
from user_repository import user_repo
from utils.cli import clear_terminal


def main_menu(client_socket) -> int:
    menu = (
        "*****************************\n"
        "*****[green]Welcome to our game[/green]*****\n"
        "Please enter what do you want to do: \n"
        "1 - Start the game\n"
        "2 - Create new player\n"
        "3 - Check leaderboard\n"
        "4 - Exit\n"
        "Enter your option number: \n"
    )
    client_socket.send(menu.encode())
    option = int(client_socket.recv(1024).decode())
    return option


def start_game_menu(client_socket) -> int:
    menu = (
        "Welcome --\n"
        ":warning: [bold red] Note that you need to have at least one player to play any mode[/bold red] :warning:\n"
        "1 - VS AI\n"
        "2 - VS PLAYER\n"
        "3 - Back to main\n"
        "Enter your option number: \n"
    )
    client_socket.send(menu.encode())
    option = int(client_socket.recv(1024).decode())
    return option


def create_player_menu(client_socket):
    client_socket.send("Please enter your name: \n".encode())
    client_socket.send("Your Name 🏻‍♂️ : ".encode())
    name = client_socket.recv(1024).decode()
    if not name:
        clear_terminal()
        client_socket.send("Name must contain at least one character\n".encode())

        create_player_menu(client_socket)

    user = user_repo.create(User(name=name))

    if isinstance(user, Exception):
        client_socket.send(f"Error creating user: {user}".encode())
    else:
        client_socket.send(f"Player [blue]{user.name}[/blue] successfully added ! ".encode())


def leaderboard_menu(client_socket):
    users = user_repo.get_all()
    table = Table("Player", "Score")
    for user in users:
        table.add_row(user.name, str(user.score))
    console = Console()
    with console.capture() as capture:
        console.print(table)
    table_str = capture.get()
    client_socket.send(table_str.encode())


def select_player(client_socket) -> Optional[User]:
    users = user_repo.get_all()
    client_socket.send("Please select the player you want to plays as: (Tap enter to see the players....)\n".encode())
    if users:

        for i, user in enumerate(users, start=1):
            client_socket.send(f"{i} - {user.name} \n".encode())
        chosen_name = client_socket.recv(1024).decode()
        for user in users:
            if user.name == chosen_name:
                clear_terminal()
                client_socket.send(f" 🙎‍♂️ {chosen_name} player selected 🙎‍♂️ ".encode())
                return user
        clear_terminal()
        client_socket.send("Wrong player".encode())

        select_player(client_socket)

    client_socket.send("There is no players ... !".encode())
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


def play__game_ai(client_socket):
    player = select_player(client_socket)
    if not player:
        client_socket.send("[bold yellow]Create a user first[/bold yellow]".encode())
        return None
    ai_score = 0
    player_score = 0
    while True:
        ai_number = random.randint(1, 3)
        menu = (
            "1 - ROCK :video_game: \n"
            "2 - PAPER :video_game:\n"
            "3 - SCISSORS :video_game:\n"
            "Which do you chose?: \n"
        )
        client_socket.send(menu.encode())
        player_number = int(client_socket.recv(1024).decode())
        if player_number in [1, 2, 3] and ai_number in [1, 2, 3]:
            winner = get_winner(ai_number, player_number)
            if winner == player_number:
                player_score += 1
                clear_terminal()
                client_socket.send("Congratulations you won :))))".encode())
            else:
                clear_terminal()
                client_socket.send("You lost ".encode())
                ai_score += 1
        else:
            clear_terminal()
            client_socket.send("You can enter number between 1-3 to chose ".encode())
            continue

        client_socket.send("Wanna play another match?: (yes-no)".encode())
        is_retry = client_socket.recv(1024).decode().lower()

        if is_retry == "no":
            break

    player.score += player_score
    user_repo.update(player)

    if player_score > ai_score:
        client_socket.send("You won totally".encode())

    elif player_score < ai_score:
        client_socket.send("You lost totally".encode())
    else:
        client_socket.send("Draw".encode())


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
    sorted_by_score_players = dict(sorted(selected_players.items(), key=lambda x: x[1], reverse=True))
    total_winner = next(iter(sorted_by_score_players.items()))[0]
    print(f"Total winner is {total_winner.name}")
    for player, score in selected_players.items():
        player.score += score
        user_repo.update(player)
