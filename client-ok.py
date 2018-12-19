# -*- coding: utf-8 -*-
import socket
import select
import threading
from src.server_config import get_host_ip


def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((str(get_host_ip()), 8086))
    # 创建线程锁，防止主线程socket被close了，子线程还在recv而引发的异常
    socket_lock = threading.Lock()

    def read_thread_method():
        while True: 
            if not sock:  # 如果socket关闭，退出
                break
            # 使用select监听客户端（这里客户端需要不停接收服务端的数据，所以监听客户端）
            # 第一个参数是要监听读事件列表，因为是客户端，我们只监听创建的一个socket就ok
            # 第二个参数是要监听写事件列表，
            # 第三个参数是要监听异常事件列表，
            # 最后一个参数是监听超时时间，默认永不超时。如果设置了超时时间，过了超时时间线程就不会阻塞在select方法上，会继续向下执行
            # 返回参数 分别对应监听到的读事件列表，写事件列表，异常事件列表
            rs, _, _ = select.select([sock], [], [], 10)
            for r in rs:  # 我们这里只监听读事件，所以只管读的返回句柄数组
                socket_lock.acquire()  # 在读取之前先加锁，锁定socket对象（sock是主线程和子线程的共享资源，锁定了sock就能保证子线程在使用sock时，主线程无法对sock进行操作）
                if not sock:  # 这里需要判断下，因为有可能在select后到加锁之间socket被关闭了
                    socket_lock.release()
                    break
                data = r.recv(1024)  # 读数据，按自己的方式读
                socket_lock.release()  # 读取完成之后解锁，释放资源
                if not data:
                    print ('server close')
                else:
                    print (data)
                    print()

    # 创建一个线程去读取数据
    read_thread = threading.Thread(target=read_thread_method)
    read_thread.setDaemon(True)
    read_thread.start()

    while True:
        m = input('>>')
        sock.send(m.encode('utf-8'))

    # 清理socket，同样道理，这里需要锁定和解锁
    socket_lock.acquire()
    sock.close()
    sock = None
    socket_lock.release()

if __name__ == "__main__":
    start_client()