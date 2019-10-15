#!/usr/bin/env python3

import socket, select

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', 12345))
        server.listen()

        connections = [server]

        while True:
            (ready, _, _) = select.select(connections, [], [], 1.0) #выбираем откуда у сервера можно читать (можно сделать accept)
            for sock in ready:
                if sock is server:
                    (client, addr) = sock.accept()
                    connections.append(client)
                    print(f"New client: {addr}")
                    continue

                data = sock.recv(1024)

                if not data:
                    print(f"Disconnect {sock.getpeername()}")
                    connections.remove(sock)
                    continue

                for conn in connections:
                    if conn not in [server, sock]:
                        try:
                            conn.sendall(data)
                        except Exception:
                            pass