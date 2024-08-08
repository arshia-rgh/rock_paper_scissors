from enum import Enum


class BaseOption(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class MainMenuOption(Enum):
    START = 1
    CREATE = 2
    LEADERBOARD = 3
    EXIT = 4
