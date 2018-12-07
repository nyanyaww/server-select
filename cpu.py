# coding:utf-8
from socket import *
from multiprocessing import Process

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8080))
server.listen(5)


def talk(conn, client_addr):
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            conn.send(msg.upper())
        except Exception:
            break


if __name__ == '__main__':  # windows下start进程一定要写到这下面
    while True:
        conn, client_addr = server.accept()
        p = Process(target=talk, args=(conn, client_addr))
        p.start()

