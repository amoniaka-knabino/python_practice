#!/usr/bin/env

import socket, threading, os, sys, signal, multiprocessing

ADDRESS = (('0.0.0.0', 12345))

        

def handle(client, addr):
    with client:
        while True:
            data = client.recv(1024) #blocking
            if data:
                client.sendall(data)
            else:
                print(f'{addr} disconnected')
                break


if __name__ == '__main__':
    if 'fork' not in dir(os):
        sys.exit()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to reuse address (reopen halfclose socket while binding)


    with server:
        server.bind(ADDRESS)
        server.listen(socket.SOMAXCONN)
        alive = set()
        while True:
            (client, addr) = server.accept() #blocking # addr - client addr
            print(f'Got connection from {addr}')
            proc = multiprocessing.Process(target=lambda: ( server.close(), handle(client, addr)))
            proc.daemon = True
            proc.start()

            alive.add(proc)
            client.close()

            for p in list(alive): 
                if not p.is_alive:
                    p.join()
                    alive.remove(p)