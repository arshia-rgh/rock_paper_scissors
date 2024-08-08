from rich.console import Console
from rich.table import Table

from database.models import User
from repository.user_repository import user_repo


class Menu:
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def main_menu(self) -> int:
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
        self.client_socket.send(menu.encode())
        option = int(self.client_socket.recv(1024).decode())
        return option

    def create_player_menu(self):
        self.client_socket.send("Please enter your name: \n".encode())
        self.client_socket.send("Your Name 🏻‍♂️ : ".encode())
        name = self.client_socket.recv(1024).decode()
        if not name:
            self.client_socket.send("Name must contain at least one character\n".encode())
            self.create_player_menu()
            return

        user = user_repo.create(User(name=name))

        if isinstance(user, Exception):
            self.client_socket.send(f"Error creating user: {user}".encode())
        else:
            self.client_socket.send(f"Player [blue]{user.name}[/blue] successfully added ! ".encode())

    def leaderboard_menu(self):
        users = user_repo.get_all()
        table = Table("Player", "Score")
        for user in users:
            table.add_row(user.name, str(user.score))
        console = Console()
        with console.capture() as capture:
            console.print(table)
        table_str = capture.get()
        self.client_socket.send(table_str.encode())
