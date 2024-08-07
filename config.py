import os
import socket

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")


class SocketConfig:
    HOST_IP = os.getenv("HOST_IP", socket.gethostbyname(socket.gethostname()))
    HOST_PORT = os.getenv("HOST_PORT", 12345)
