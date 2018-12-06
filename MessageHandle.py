import server_config
from datetime import datetime
import os
import json

__test_command = '0020'
__test_message = 'the message is used for test'


class MessageHandle(object):
	data_from_device = b''
	send_data = ''
	data_format = 'ascii'
	message_dict = {}

	def __init__(self):
		pass

	@staticmethod
	def __bytes2str(bytes_: bytes):
		try:
			return str(bytes_, encoding='utf-8')
		except Exception:
			return str(bytes_, encoding='gbk')

	@staticmethod
	def __str2bytes(string_: str):
		return bytes(string_, encoding='utf8')

	@property
	def parsing(self):
		"""
		文本的解析,把bytes转化为str 并且返回解析后的结果
		0 - 数据头
		1 - ip号
		2 - 长度校验
		3 - 时间戳
		4 - 命令
		5 - 文本信息
		6 - 数据尾
		"""
		self.message_dict.clear()
		data = self.__bytes2str(self.data_from_device)
		self.message_dict.setdefault('source', data)
		data_list = data.split(server_config.separator)
		if len(data_list) == 7:
			if data_list[0] == 'SA' and data_list[6] == 'END':
				if int(data_list[2]) == len(data_list[4] + data_list[5]):
					self.message_dict.setdefault('ip', data_list[1])
					self.message_dict.setdefault('command', data_list[4])
					self.message_dict.setdefault('message', data_list[5])
					self.message_dict.setdefault('state', 'data receive success')
				else:
					self.message_dict.setdefault('state', 'data receive incomplete')
			else:
				self.message_dict.setdefault('state', 'data receive format error')
		else:
			self.message_dict.setdefault('state', 'data receive incomplete')
		return self.message_dict

	@parsing.setter
	def parsing(self, data_from_device):
		"""
		把二进制转为字符串
		"""
		self.data_from_device = data_from_device

	@property
	def encoding(self):
		"""
		文本的编码,把文本编码成16进制或者ascii,返回值是bytes
		"""
		send_message_list = []
		if self.data_format == '16' or self.data_format == 16:
			for each_str in self.send_data:
				temp = hex(ord(each_str))
				send_message_list.append(self.__str2bytes(temp))
		elif self.data_format == 'ascii':
			for each_str in self.send_data:
				send_message_list.append(self.__str2bytes(each_str))
		msg = b''.join(send_message_list)
		return msg

	@encoding.setter
	def encoding(self, encoding_info: tuple):
		self.send_data, self.data_format = encoding_info

	def save(self, path, data):
		"""
		:param path: 存储的文件夹名
		:param data: 存储数据
		:return: None
		"""
		root = os.getcwd()
		path = root + '/' + path
		now_time_list = self.local_time().split('_')
		date_time = '{0}_{1}_{2}'.format(now_time_list[0], now_time_list[1], now_time_list[2])
		day_time = '{0}_{1}_{2}_{3}'.format(now_time_list[3], now_time_list[4], now_time_list[5], now_time_list[6])
		temp_dict = {}
		temp_dict.setdefault(day_time, data)

		if not os.path.exists(path):
			os.makedirs(path)
		file_name = path + '/' + "{}.json".format(date_time)
		# 保存数据之前如果旧数据存在则读取旧数据
		if os.path.exists(file_name):
			with open(file_name, 'r') as f:
				old_data = json.load(f)
				temp_dict.update(old_data)
		with open(file_name, 'w') as f:
			json.dump(temp_dict, f, indent=4, ensure_ascii=False)

	@staticmethod
	def load(path, file_name):
		root = os.getcwd()
		path = root + '/' + path
		file_name = path + '/' + "{}.json".format(file_name)
		with open(file_name, 'r') as f:
			return json.load(f)

	def info_connect(self, device, command, message):
		byte_num = str(len(command) + len(message))
		info = "{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}".format(
				server_config.separator, server_config.data_head,
				device, byte_num, self.local_time(),
				command, message, server_config.data_tail)
		return info

	@staticmethod
	def local_time():
		now = datetime.now()
		return now.strftime('%Y_%m_%d_%H_%M_%S_%f')
	
	def message_handle(self, device_name, command, message):
		"""
		接受设备名，命令以及信息
		return 返回给设备的数据
		"""
		if device_name == 'door':
			if command == 'door_in':
				pass
		else:
			pass

if __name__ == '__main__':
	test_message = MessageHandle()
	message_from_device = test_message.info_connect(server_config.ip_server, __test_command, __test_message)
	# print(message_from_device)

	test_message.parsing = message_from_device.encode('utf-8')

	test_dict = (test_message.load('10.12.161.5', '2018_11_02'))
	for each in test_dict.values():
		for per in each.items():
			print(per)
