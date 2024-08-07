import socket

from config import SocketConfig

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SocketConfig.HOST_IP, SocketConfig.HOST_PORT))
