import socket
import threading
from server_config import get_host_ip
 
 
class tcp_serv(object):
    def serv_start(self):
        # 创建套接字
        serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        # 设置ip 及 Port
        # 设置端口复用
        serv_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_soc.bind((str(get_host_ip), 8086))
 
        # 主动变为被动
        serv_soc.listen(120)  # 最大接收客户端数量为120
        while True:
            client_soc, client_adr = serv_soc.accept()  # 接收客户端
            print("---------------客户端接入---------------")
            client = threading.Thread(target=self.client_conn, args=(client_soc,))  # 数据为元组
            client.start()
        serv_soc.close()  # 服务端关闭
 
    def client_conn(self, client_soc):
        """客户端 处理数据"""
        while True:
            rev_msg = client_soc.recv(1024).decode('utf-8')  # 接收的字节数 进行转码
            print("这是客户端发的数据%s" % rev_msg)
            if rev_msg:
                # 向客户端发送数据
                client_soc.send(rev_msg.encode('utf-8'))
                # 数据收发完成 关闭
            else:
                # 无数据，客户端断开
                print("客户断开链接 >>>>>")
                client_soc.close()
                break
 
 
def main():
    serv = tcp_serv()
    serv.serv_start()  # 执行
 
 
if __name__ == '__main__':
    main()