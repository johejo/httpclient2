import socket
import sys
import requests
from urllib.parse import urlparse


def main():
    argv = sys.argv
    buf_size = 1024

    url = argv[1]
    hr = requests.head(url)
    if hr.status_code != 200:
        print("ERROR", file=sys.stderr)
        exit(1)
    length = int(hr.headers['content-length'])

    # print(hr.headers)

    url = urlparse(argv[1])
    num = int(argv[2])

    chunk_size = int(length / num)
    reminder = int(length % num)

    sock = []

    address = (socket.gethostbyname(url.hostname), url.port)

    for s in range(num):
        s = socket.create_connection(address)
        sock.append(s)

    begin = 0
    data = []
    i = 0

    for s in sock:
        if i == num - 1:
            end = begin + chunk_size - 1 + reminder
        else:
            end = begin + chunk_size - 1

        msg = set_message(url, begin, end)
        begin += chunk_size
        s.sendall(msg.encode())

    for s in sock:
        total = 0

        sf = s.makefile('b')
        index = read_header(sf, chunk_size)

        tmp = bytearray()
        while True:
            if chunk_size - total < buf_size:
                if i == num - 1:
                    read_size = chunk_size - total + reminder
                else:
                    read_size = chunk_size - total
            else:
                read_size = buf_size

            r = sf.read(read_size)
            tmp += r

            # print(r)
            total += len(r)
            if total >= chunk_size:
                break

        data.insert(index, tmp)
        i += 1
        s.close()

    x = bytes()
    for d in data:
        x += d

    filename = url.path[url.path.rfind('/') + 1:]
    f = open('{0}'.format(filename), 'wb')
    f.write(x)
    f.close()
    # print(x.decode(), end='')


def set_message(url, n, m):
    return 'GET {0} HTTP/1.1\r\nHost: {1}\r\nRange: bytes={2}-{3}\r\n\r\n'.format(url.path, url.netloc, n, m)


def get_order(r, chunk_size):
    r = r[r.find('bytes ') + len('bytes '):]
    r = r[:r.find('\r\n\r\n')]

    x = ''
    for i in r:
        if i == '-':
            break

        x += i

    return int(int(x) / chunk_size)


def read_header(sf, chunk_size):
    index = 0
    while True:
        l = sf.readline().decode()
        # print(l)
        if 'HTTP 200 OK' in l:
            exit(1)
        if 'content-range' in l or 'Content-Range' in l:
            index = get_order(l, chunk_size)

        if l == '\r\n':
            break

    return index


if __name__ == '__main__':
    main()
