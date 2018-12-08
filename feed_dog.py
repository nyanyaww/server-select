import socket
from server_config import get_host_ip
from time import sleep
from MessageHandle import MessageHandle

host = str(get_host_ip())
port = 8086

device = 'dog'

message = MessageHandle()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    device_ip = device
    while True:
        sleep(10)
        device_command = 'feed dog'
        device_messagae = 'ok'
        send_from_client = message.info_connect(
            device_ip, device_command, device_messagae)
        message.encoding = (send_from_client, 'ascii')
        s.send(message.encoding)
        data = s.recv(1024)
        print('this is your input!\n{0}'.format(message.encoding))
        print('-'*60)
        print('this is from server!\n{0}'.format(data))
        print('-'*60)
