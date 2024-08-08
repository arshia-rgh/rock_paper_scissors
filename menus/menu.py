from rich.console import Console
from rich.table import Table

from database.models import User
from repository.user_repository import user_repo


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
