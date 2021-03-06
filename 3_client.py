import socket
import getpass
import threading
import json
import time
from pprint import pprint
import ast
import sys
import datetime



cookies = json.load(open('cookie_file_3.json'))

for cookie in list(cookies):  ##Removing Expired Cookies

	curr_datetime = datetime.datetime.now()
	cookie_datetime = datetime.datetime.strptime(cookies[cookie]['expires_on'], '%d-%m-%Y %H:%M:%S.%f')

	if cookie_datetime<curr_datetime:
		del cookies[cookie]    
		parsed = json.dumps(cookies, indent=4)    
		with open('cookie_file_3.json','w') as file:
			file.write(parsed)



if len(sys.argv)==1:
	HOST = '127.0.0.1'
	PORT = 12345

if len(sys.argv)==2:
	HOST = sys.argv[1]
	PORT = 12345

if len(sys.argv)==3:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))



while True:
	undcd_data, addr = client.recvfrom(1024)


	data = undcd_data.decode('utf-8')



	print(data)

	
	if not data:
		break;

	reply = ''
	

	if 'Choose' in data or 'Enter' in data or 'Search' in data or 'profile' in data :

		reply = input("waiting for input : ")
		print()
	elif 'Username' in data:
		reply = input("enter username : ")
		print()
	elif 'Password' in data:
		reply = getpass.getpass('enter password : ')
		print()

		

	if reply!="":
		client_data = (reply + "|" + str(cookies)).encode('utf-8')
		client.send(client_data)

client.close()
