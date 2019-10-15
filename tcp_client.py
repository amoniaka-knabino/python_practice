import socket
import re
# 50 strings
# fetch $link

find_link = re.compile(r'"[a-zA-Z]*"')
find_flag = re.compile(r'PYTHON_\w+=')

def recv_n_bytes(sock, n):
    recv_count = 0
    data = b''
    while recv_count < n:
        currect_data = sock.recv(n)
        recv_count += len(currect_data)
        data += currect_data
    return data

def recv_n_bytes_by_one(sock, n):
    recv_count = 0
    data = b''
    while(recv_count < n):
        currect_byte = sock.recv(1)
        data += currect_byte

def parse_page(sock, link):
    global history
    global cathed_flags
    global queue_links
    history.append(link)
    command = b"fetch " + link + b"\r\n"
    #print(command)
    sock.sendall(command)
    n_str = ''
    while(True):
        currect_byte = sock.recv(1)
        if currect_byte == b'\n':
            break
        else:
            n_str += currect_byte.decode('ascii')
    n = int(n_str)
    #print(n)
    data = recv_n_bytes(sock, n).decode('ascii')
    links = find_link.findall(data)
    current_flags = find_flag.findall(data)

    for x in links:
        if x in history or x in links:
            continue
        queue_links.append(x[1:-1])
    for x in current_flags:
        if x in cathed_flags:
            continue
        cathed_flags.append(x)

    #print(links)
    #print(current_flags)

host, port = "10.96.16.6", 13000

sock = socket.socket()
sock.connect((host, port))

queue_links = []
cathed_flags = []
history = []

i = 0
while (i < len(queue_links)):
    parse_page(sock, queue_links[i].encode('ascii'))
    print(len(cathed_flags), i, len(queue_links))
    i += 1
for x in cathed_flags:
    print(x)
