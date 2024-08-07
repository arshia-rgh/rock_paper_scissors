import socket
from config import SocketConfig

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SocketConfig.HOST_IP, SocketConfig.HOST_PORT))
