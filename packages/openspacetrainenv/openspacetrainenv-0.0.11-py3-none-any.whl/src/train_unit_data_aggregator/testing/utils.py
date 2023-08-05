import socket
from contextlib import closing


def find_free_port():
    """
    Request the OS to find a free port in order to avoid connecting to an already occupied port.
    """

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
