import os


def clear_terminal() -> None:

    os.system('clear' if os.name == 'posix' else 'cls')
