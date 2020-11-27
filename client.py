import socket
import getpass
import threading
from pprint import pprint

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))



while True:
	undcd_data, addr = client.recvfrom(1024)


	data = undcd_data.decode('utf-8')



	print(data)

	
	if data == 'done':
		break;

	reply = ''
	
	if 'Choose' in data or 'Enter' in data or 'Search' in data:
		reply = input("waiting for input : ")
		print()
	elif 'Username' in data:
		reply = input("enter username : ")
		print()
	elif 'Password' in data:
		reply = getpass.getpass('enter password : ')
		print()



	client.send(bytes(reply,'utf-8'))

client.close()
