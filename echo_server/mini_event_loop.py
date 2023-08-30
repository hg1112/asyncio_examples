import socket

# Example -1 : Extremely CPU intensive
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# address = ("127.0.0.1", 5000)
# server_socket.bind(address)

# server_socket.listen()
# server_socket.setblocking(False)
# connections = []

# try:
#     while True:
#         try:
#             connection, client_address = server_socket.accept()
#             connection.setblocking(False)
#             print(f"Received a connection from client at {client_address}")
#             connections.append(connection)
#         except BlockingIOError:
#             pass
#         for connection in connections:
#             try:
#                 buffer = b''
#                 while buffer[-2:] != b'\r\n':
#                     data = connection.recv(2)
#                     if not data:
#                         break
#                     else:
#                         print(f"Got data from client : {data}")
#                     buffer += data
#                 print(f"All data from {connection} : {buffer}")
#                 connection.sendall(b'Received data -' + buffer)
#             except BlockingIOError:
#                 pass
# finally:
#     server_socket.close()


# Example 2 : mini event loop
import selectors
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = ("127.0.0.1", 5000)
server_socket.bind(address)
server_socket.setblocking(False)
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print("No events occured yet , moving on ...")

    for event, _ in events:
        event_socket = event.fileobj
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"Received a connection from {connection}")
            selector.register(connection, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print(f"Got data : {data}")
            event_socket.send(b'recv ack -' + data)



