import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = ("127.0.0.1", 5000)
server_socket.bind(address)

server_socket.listen()
connections = []

try:
    while True:
        connection, client_address = server_socket.accept()
        print(f"Received a connection from client at {client_address}")
        connections.append(connection)
        for connection in connections:
            buffer = b''
            while buffer[-2:] != b'\r\n':
                data = connection.recv(2)
                if not data:
                    break
                else:
        
                    print(f"Got data from client : {data}")
                buffer += data
            print(f"All data : {buffer}")
            connection.sendall(b'Received data -' + buffer)
finally:
    server_socket.close()
