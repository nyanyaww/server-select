import queue
import socket
import threading
from select import select

from MessageHandle import MessageHandle
from server_config import get_host_ip

import multiprocessing


class server(object):
    # 客户端传来的数据保存在队列里面
    receive_message_queue = {}
    input_list = []
    output_list = []
    # 使用一个哈希表来保存客户端名字与客户端对象的映射
    client_hash = {}
    # 对于客户端发送的数据进行
    # 1.解析处理
    # 2.保存
    # 3.读取
    message = MessageHandle()

    def __init__(self, port, server_ip=str(get_host_ip())):
        self.PORT = port
        self.SERVER_IP = server_ip
        print(self.SERVER_IP)
        SERVER_INIT = (self.SERVER_IP, self.PORT)
        self.server = socket.socket()
        self.server.bind(SERVER_INIT)
        # 最大监听数为10个
        self.server.listen(10)
        # 设置为非阻塞
        self.server.setblocking(False)
        # 初始化将服务端加入监听列表
        self.input_list.append(self.server)
        print('server is running...')

    def __client_message_receive(self):
        # 开始 select 监听,对input_list中的服务端server进行监听
        self.std_input, self.std_output, self.stderr = select(
            self.input_list, self.output_list, self.input_list)
        # 循环判断是否有客户端连接进来,当有客户端连接进来时select将触发
        for client in self.std_input:
            # 判断当前触发的是不是服务端对象, 当触发的对象是服务端对象时,说明有新客户端连接进来了
            if client == self.server:
                # 接收客户端的连接, 获取客户端对象和客户端地址信息
                self.conn, self.address = self.server.accept()
                print("Client {0} connected! ".format(self.address))
                # 将客户端对象也加入到监听的列表中, 当客户端发送消息时 select 将触发
                self.input_list.append(self.conn)
                # 为连接的客户端单独创建一个消息队列，用来保存客户端发送的消息
                self.receive_message_queue[self.conn] = queue.Queue()
            else:
                # 由于客户端连接进来时服务端接收客户端连接请求，将客户端加入到了监听列表中(input_list)，客户端发送消息将触发
                # 所以判断是否是客户端对象触发
                try:
                    receive_data = client.recv(1024)
                    # 客户端未断开
                    if receive_data:
                        # 打印一下收到的数据
                        print("received {0} from client {1}".format(
                            receive_data, str(self.address)))
                        # 将收到的消息放入到各客户端的消息队列中
                        # 将数据解析成哈希表
                        self.message.parsing = receive_data
                        # 如果解析出来的数据是完整的
                        if self.message.parsing.get('state') == 'data receive success':
                            # 把关键的信息提取出来
                            client_name = self.message.parsing['ip']
                            if not client_name in self.client_hash:
                                self.client_hash[client_name] = client
                            client_command = self.message.parsing.get(
                                'command')
                            client_message = self.message.parsing.get(
                                'message')
                            # 保存到对应名字的json文件夹下
                            self.message.save(
                                client_name, self.message.parsing)
                            self.message.message_handle(
                                client_name, client_command, client_message)
                            server_send_command = 'receive state'
                            server_send_message = 'ok'
                        # 解析出来的数据表明或多或少都有问题
                        else:
                            client_name = client
                            self.client_hash[client_name] = client
                            server_send_command = 'receive state'
                            server_send_message = 'error'
                        # 将数据以一定形式编码成二进制
                        self.message.encoding = (self.message.info_connect(
                            'server', server_send_command, server_send_message), 'ascii')
                        self.receive_message_queue[self.client_hash[client_name]].put(
                            self.message.encoding)
                        # 将回复操作放到output列表中，让select监听
                        if client not in self.output_list:
                            self.output_list.append(client)

                except ConnectionResetError:
                    # 客户端断开连接了，将客户端的监听从input列表中移除
                    self.input_list.remove(client)
                    # 移除客户端对象的消息队列
                    del self.receive_message_queue[client]
                    print("\n[input] Client {0} disconnected".format(
                        self.address))

    def __client_message_send(self):
         # 如果现在没有客户端请求,也没有客户端发送消息时，开始对发送消息列表进行处理
        for client in self.output_list:
            try:
                # 如果消息队列中有消息,从消息队列中获取要发送的消息
                if not self.receive_message_queue[client].empty():
                    # 从该客户端对象的消息队列中获取要发送的消息
                    send_data = self.receive_message_queue[client].get()
                    client.send(send_data)
                else:
                    # 将监听移除等待下一次客户端发送消息
                    self.output_list.remove(client)

            except ConnectionResetError:
                # 客户端连接断开了
                del self.receive_message_queue[client]
                self.output_list.remove(client)
                print("\n[output] Client  {} disconnected".format(
                    str(self.address)))

    def run(self):
        while True:
            self.__client_message_receive()
            self.__client_message_send()


if __name__ == "__main__":
    respberry_server = server(8086)
    respberry_server.run()
