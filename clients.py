import socket
import select


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', 12345))
        server.listen()

        connections = [server]
        while True:
            (ready, _, _) = select.select(connections, [], [], 1.0)
            for sock in ready:
                (client, addr) = sock.accept()
                connections.append(client)
                print(f'New client: {addr}')
                continue

            data = sock.recv(1024)
            if not data:
                print(f'Disconnected {sock.getpeername}')
                connections.remove(sock)
                continue

            for conn in connections:
                if conn not in [server, sock]:
                    try:
                        conn.sendall(data)
                    except Exception:
                        pass


# import socket
# import multiprocessing
#
#
# ADDRESS = (('0.0.0.0', 12345))
# # socket.setblocing(False)
# # socket.settimeout(value)
#
# def handle(client, addr):
#     with client:
#         while True:
#             data = client.recv(1024)
#             if data:
#                 client.sendall(data)
#             else:
#                 print(f'{addr} disconnected')
#                 break
#
#
# if __name__ == "__main__":
#
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
#     with server:
#         server.bind(ADDRESS)
#         server.listen(socket.SOMAXCONN)
#
#         alive = set()
#
#         while True:
#             (client, addr) = server.accept()
#             print(f'Got connevted from {addr}')
#             proc = multiprocessing.Process(target=lambda: (
#                 server.close(),
#                 handle(client, addr)
#             ))
#             proc.daemon = True
#             proc.start()
#
#             alive.add(proc)
#             client.close()
#
#             for p in list(alive):
#                 if not p.is_alive():
#                     p.join()
#                     alive.remove(p)