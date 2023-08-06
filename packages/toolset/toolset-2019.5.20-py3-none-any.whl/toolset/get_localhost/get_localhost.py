from socket import socket, AF_INET, SOCK_DGRAM


def get_localhost():
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
