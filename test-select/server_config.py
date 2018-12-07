import socket

data_head = 'SA'
separator = '//'
data_tail = 'END'

command_message_dict = {
	'door':    {
		'door_out': '0001',
		'door_in':  '0002',

	},
	'window':  {
		'': '',
	},
	'lamp':    {
		'L1': '2001',
		'L2': '2002',
		'L3': '2003',
	},
	'curtain': {
		'motor_operator': '3001',
		'curtain_check':  '3002'
	}
}


def get_host_ip():
	"""
	获取本机的ip地址
	:return: 本机的ip
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

	return ip


ip_server = get_host_ip()


class StateInfo(object):
	@staticmethod
	def data_format_error():
		"""
		:return: 数据格式错误
		"""
		return {
			'code':    '0000',
			'message': 'data format error'
		}

	@staticmethod
	def data_receive_fail():
		"""
		:return: 数据接收不完整
		"""
		return {
			'code':    '1111',
			'message': 'data receive incomplete',
		}

	@staticmethod
	def data_receive_success():
		"""
		:return: 数据接收成功
		"""
		return {
			'code':    '2222',
			'message': 'data receive success',
		}

	@staticmethod
	def unknown_bug():
		"""
		:return: 未知bug
		"""
		return {
			'code':    '3333',
			'message': 'unknown bug',
		}

	@staticmethod
	def door_out(command_code: str, message: str):
		return {
			'code':    command_code,
			'message': message
		}


if __name__ == '__main__':
	print(ip_server)
