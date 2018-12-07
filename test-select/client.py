
from socket import *
from sys import argv, exit
from getopt import getopt, GetoptError
import threading
import time
thr = []
csock = socket(AF_INET, SOCK_STREAM)
csock.connect(('localhost', 7500))


def dosend(sock, user):
    while True:
        data = raw_input('%s : >' % user)
        if data == 'q':
            sock.close()
            print '%s loginout ' % user
            break
        else:
            sock.send(data)


def dorecv(sock):
    while True:
        data = sock.recv(1024)
        print data


def h():
    print '-u user'


try:
    opt, arg = getopt(argv[1:], 'u:', [])
except GetoptError, e:
    h()
    exit(1)
for o, u in opt:
    username = u
if username == '':
    h()
    exit(1)
csock.send(username)
res = csock.recv(1024)
if res == 'hasok':
    print '%s has logined in ' % username
    csock.close()
elif res == 'ok':
    print '%s success logined in ' % username
    t = threading.Thread(target=dosend, args=(csock, username))
    thr.append(t)
    t = threading.Thread(target=dorecv, args=(csock,))
    thr.append(t)
    for i in range(len(thr)):
        thr[i].start()
    thr[0].join()
