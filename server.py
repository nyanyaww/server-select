import socket
from src.server_config import get_host_ip
from src.MessageHandle import MessageHandle
import multiprocessing


class Server(object):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 获取本机联网的ip
	ip_server = str(get_host_ip())
	port = 8086
	server.bind((ip_server, port))
	server.listen(10)
	print('server is running...')

	def __init__(self):
		self.client_hash_map = {}
		pass

	def deal_client(self, client: socket.socket):
		message = MessageHandle()
		device_name = 'unknown'
		while True:
			# 接收数据
			data = client.recv(1024)
			# 监听到数据发送过来
			if data:
				# 把数据解析成字典
				message.parsing = data
				# 只有当第一次解析数据的时候才把设备名更新
				if 'ip' in message.parsing and device_name == 'unknown':
					device_name = message.parsing['ip']
				message.save(device_name, message.parsing)
				self.client_hash_map[device_name] = client
				send_from_server = message.info_connect('server', '9999', 'data receive success!')
				message.encoding = (send_from_server, 'ascii')
				for each in self.client_hash_map:
					self.client_hash_map[each].send(message.encoding)
				print(message.encoding)
			# print(message.encoding)
			else:
				# 断开的时候删除设备名的键值对
				self.client_hash_map.pop(device_name)
				client.close()
				break

	def run(self):
		while True:
			device, address = self.server.accept()
			print("client [{}] is connected!".format(address))
			client = multiprocessing.Process(target=self.deal_client, args=(device,))
			client.start()
			device.close()
			# client.join()


def main():
	echo_server = Server()
	echo_server.run()


if __name__ == '__main__':
	main()
