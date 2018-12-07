from socket import *
from sys import argv, exit
import threading
import time
from server_config import get_host_ip
sclient = socket(AF_INET, SOCK_STREAM)
sclient.bind((str(get_host_ip), 8086))
sclient.listen(5)

usersock = {}


def do(sock, user):
    while True:
        data = sock.recv(1024)
        if data == 'q':
            del usersock[user]
            sock.close()
            break
        else:
            for i in usersock.iterkeys():
                if i <> user:
                    usersock[i].send('%s say : %s   |  %s' % (
                        user, data, time.strftime('%Y/%m/%d %x', time.localtime())))


while True:
    clients, addr = sclient.accept()
    print '%s---%s ----connecting' % addr
    username = clients.recv(1024)
    if usersock.has_key(username):
        clients.send('hasok')
        clients.close()
    else:
        clients.send('ok')
        print '%s online ' % username
        usersock[username] = clients
        t = threading.Thread(target=do, args=(clients, username))
        t.start()
