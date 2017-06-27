import socket
import sys
import requests
from urllib.parse import urlparse


def main():
    argv = sys.argv
    buf_size = 1024

    url = argv[1]
    hr = requests.head(url)
    length = int(hr.headers['Content-Length'])

    # print(hr.headers)

    url = urlparse(argv[1])
    port = int(argv[2])
    num = int(argv[3])

    chunk_size = int(length / num)
    reminder = int(length % num)

    sock = []

    address = (socket.gethostbyname(url.netloc), port)

    # s = socket.create_connection(address)
    # msg = set_message(url, 0, 100)
    # s.sendall(msg.encode())
    # r = s.recv(buf_size).decode()
    # print(r)
    # n = get_order(r, num, length, chunk_size)
    # print(n)
    # s.close()

    for s in range(num):
        s = socket.create_connection(address)
        sock.append(s)

    begin = 0
    data = []
    index = 0

    for s in sock:
        msg = set_message(url, begin, begin + chunk_size - 1)
        begin += chunk_size
        s.sendall(msg.encode())
        total = 0
        c = ''
        while True:
            r = s.recv(buf_size)
            r = r.decode()
            if total == 0:
                index = get_order(r, chunk_size)
                tmp = r[r.find('\r\n\r\n') + len('\r\n\r\n'):]
            else:
                tmp = r

            c += tmp
            total += buf_size
            if total >= chunk_size:
                break

        data.insert(index, c)
        # print(c)

    text = ''
    for x in data:
        text += x

    print(text)


def set_message(url, n, m):
    return 'GET {0} HTTP/1.1\r\nHost: {1}\r\nRange: bytes={2}-{3}\r\n\r\n'.format(url.path, url.netloc, n, m)


def get_begin(r):
    r = r[r.find('bytes ') + len('bytes '):]
    r = r[:r.find('\r\n\r\n')]

    x = ''
    for i in r:
        if i == '-':
            break

        x += i

    return int(x)


def get_order(r, chunk_size):
    begin = get_begin(r)
    return int(begin / chunk_size)


if __name__ == '__main__':
    main()
