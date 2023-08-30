import asyncio
import socket
from types import TracebackType
from typing import Optional, Type

class ConnectedSocket:

    def __init__(self, server_socket) -> None:
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        print('Entering the context manager, waiting for connection')
        loop = asyncio.get_running_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print('Accepted a connection ')
        return self._connection

    async def __aexit__(self, 
                        exe_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]
                        ):
        print('Exiting context manager')
        if self._connection:
            self._connection.close()
            print('Closed connection')

async def main():
    loop = asyncio.get_running_loop()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    address = ('127.0.0.1', 5000)
    server_socket.bind(address)
    server_socket.listen()

    async with ConnectedSocket(server_socket) as cs:
        data = await loop.sock_recv(cs, 1024)
        print(data)


asyncio.run(main())

