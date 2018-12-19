import socket
from src.server_config import get_host_ip
import time
from src.MessageHandle import MessageHandle
import random

host = str(get_host_ip())
port = 8086

device_list = {
	0: {
		'door': {
			0: 'door_out',
			1: 'door_in',

		}
	},
	1: {
		'window': {
			0: '????',
		}
	},
	2: {
		'light': {
			0: 'L1',
			1: 'L2',
			2: 'L3',
		}
	},
	3: {
		'curtain': {
			0: 'motor_control',
			1: 'curtain_check'
		}
	},
	4: {
		'temperature': {
			0: 'yz_set'
		}
	},
	5: {
		'phone': {
			0: 'check'
		}
	},
}

message = MessageHandle()

if __name__ == '__main__':
	temp = ('unknown', ',,,,')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	count = random.randint(0, len(device_list) - 1)
	s.connect((host, port))
	while True:
		time.sleep(3)
		device = device_list[count]
		device_ip = list(device.keys())[0]
		device_command = list(list(device.values())[0].values())
		device_command = device_command[random.randint(0, len(device_command) - 1)]
		send_from_client = message.info_connect(device_ip, device_command, str(time.time()))
		print(device_ip, device_command)
		message.encoding = (send_from_client, 'ascii')
		s.send(message.encoding)
		s.send(message.encoding)
		data = s.recv(1024)
		print(data)
		# s.close()
		
