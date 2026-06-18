import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 2020
ADDR = (IP, PORT)
DEFAULT_BUFFER_SIZE = 1024
DEFAULT_DECODE_FORMAT = "utf-8"

SIZE_PREFIX_LEN = 4