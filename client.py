import socket
import sys
import requests
from urllib.parse import urlparse


def main():
    argv = sys.argv
    buf_size = 1024
    default_url = 'http://165.242.111.77:80/index.html'
    default_num = 6

    if len(argv) >= 2:
        url = urlparse(argv[1])
    else:
        url = urlparse(default_url)

    if len(argv) >= 3:
        num = int(argv[2])
    else:
        num = default_num

    hr = requests.head(url.scheme+'://'+url.netloc+url.path)
    if hr.status_code != 200:
        print("ERROR STATUS CODE {0}".format(hr.status_code), file=sys.stderr)
        exit(1)
    length = int(hr.headers['content-length'])

    # if len(argv) >= 4:
    #     chunk_size = int(argv[3])
    #     reminder = int(length % chunk_size)
    #     # num = int(length // chunk_size)
    # else:
    #     chunk_size = int(length / num)
    #     reminder = int(length % num)
    chunk_size = int(length / num)
    reminder = int(length % num)

    filename = url.path[url.path.rfind('/') + 1:]
    f = open('{0}'.format(filename), 'wb')
    f.close()

    sock = []

    if url.port is None:
        port = '80'
    else:
        port = url.port

    address = (socket.gethostbyname(url.hostname), port)

    begin = 0
    data = [bytearray() for i in range(num)]
    i = 0

    for s in range(num):
        s = socket.create_connection(address)
        sock.append(s)
        if i == num - 1:
            end = begin + chunk_size - 1 + reminder
        else:
            end = begin + chunk_size - 1

        msg = set_message(url, begin, end)
        begin += chunk_size
        s.sendall(msg.encode())
        i += 1

    i = 0
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

        data[index] = tmp
        if data[index] is not None:
            f = open('{0}'.format(filename), 'ab')
            f.write(data[index])
            f.close()

        i += 1

    for s in sock:
        s.close()


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