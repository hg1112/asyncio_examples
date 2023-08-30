import asyncio
import socket
import time


async def accept_client(server_socket):
    loop = asyncio.get_running_loop()
    while True:
        client_connection, client_address = await loop.sock_accept(server_socket)
        client_connection.setblocking(False)
        print(f"Received client {client_address}")

        ## bug w.r.t error handling 
        asyncio.create_task(read_client(loop, client_connection))

async def read_client(loop: asyncio.AbstractEventLoop, client_connection) -> None:
    buffer = b''
    data = await loop.sock_recv(client_connection, 1024)
    if not data:
        buffer += data
    print(f"Got data {data}")
    result = await loop.sock_sendall(client_connection, buffer)
    return result

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    address = ('127.0.0.1', 5000)
    server_socket.bind(address)
    server_socket.listen()

    await accept_client(server_socket)

asyncio.run(main())
