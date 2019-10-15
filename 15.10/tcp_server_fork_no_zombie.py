#!/usr/bin/env

import socket, threading, os, sys, signal

ADDRESS = (('0.0.0.0', 12345))

def handle_child(signal, _):
    got = True
    while got:
        try:
            got = os.waitpid(0, os.WNOHANG)
        except:
            got = False
        

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

    signal.signal(signal.SIGCLD, ) #дописать

    with server:
        server.bind(ADDRESS)
        server.listen(socket.SOMAXCONN)

        while True:
            try:
                (client, addr) = server.accept() #blocking # addr - client addr
                print(f'Got connection from {addr}')

                #th = threading.Thread(target=lambda:handle(client, addr))

                pid = os.fork()
                if pid:
                    #parent
                    client.close()
                else:
                    #child
                    server.close()
                    handle(client, addr)
                    break
            except InterruptedError:
                pass
            