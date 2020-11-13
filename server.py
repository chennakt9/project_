import socket
import threading
import json
import datetime

HOST = '127.0.0.1'
PORT = 12345



users = json.load(open('DB.json'))



def update_db():
	parsed = json.dumps(users, indent=4)

	with open('DB.json','w') as file:
		file.write(parsed)



def login_handler(client):
	client.send(('Log in... \n\n**Username**').encode('utf-8'))
	usr = client.recv(1024).decode('utf-8')

	client.send(('**Password**').encode('utf-8'))
	pswd = client.recv(1024).decode('utf-8')


	if usr not in users or users[usr]['password'] != pswd:
		client.send(('Invalid credentials..').encode('utf-8'))
		client.close()
		return None

	client.send((f'Successfully Logged In as {usr}').encode('utf-8'))

	users[usr]['isOnline'] = True;


	update_db() 

	return usr;


def chat_handler(user_name,client):

	friends = users[user_name]['friends']

	client.send(('**Online Users**\n'+'\n'.join(friends)+'\n\nChoose a friend to start messaging:').encode('utf-8'))

	while True:
		target_friend = client.recv(1024).decode('utf-8')

		if target_friend in users:
			
			if users[target_friend]['isOnline'] == True:
				client.send(('Client is online start messaging..').encode('utf-8'))
			else:
				client.send(('Client is offline messages may be seen later'))
			while True:
				client.send(('Enter message:').encode('utf-8'))
				messg = client.recv(1024).decode('utf-8')

				if target_friend not in users[user_name]['msgs']:
					users[user_name]['msgs'][target_friend] = [['sent', messg, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')]]
				else:
					users[user_name]['msgs'][target_friend].append(['sent', messg, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')])

				if user_name not in users[target_friend]['msgs']:
					users[target_friend]['msgs'][user_name] = [['recieved', messg, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f'), 'not_seen']]
				else:
					users[target_friend]['msgs'][user_name].append(['recieved', messg, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f'), 'not_seen'])

				update_db()

				all_msgs = [msg[1] for msg in users[user_name]['msgs'][target_friend]]

				client.send(('\n'.join(all_msgs)).encode('utf-8'))









def client_thread(client):

		
	user_name = login_handler(client) #login

	options = '''
	Choose an action:

	1. Send Private Message | 5. Upload new post
	2. Search Reg Users     | 6. Logout
	3. View Chats           | 
	4. Friend Options       | 
	'''

	client.send(options.encode('utf-8'))

	while True:
		data = client.recv(1024).decode('utf-8')

		if data=='1': # private message
			chat_handler(user_name, client)
		
		elif data=='2': # search registered users
			client.send(('Not implemented yet').encode('uft-8'))
		
		elif data=='3': # view chats
			client.send(('Not implemented yet').encode('uft-8'))

		elif data=='4': # Friend Options
			client.send(('Not implemented yet').encode('uft-8'))

		elif data=='5': # Upload New post
			client.send(('Not implemented yet').encode('uft-8'))

		elif data=='6': # logout
			clients[user_name]['isOnline'] = False
			client.send(bytes('Logged out successfully !!'))
			client.close()









		
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)
print(f'Waiting for clients on :{PORT}')

while True:
	client, addr = server.accept()
	print(f'Connected with {addr[0]}:{addr[1]}')
	t1 = threading.Thread(target=client_thread,
        args=(client,)
    )

	t1.start()

	# t1.join()




server.close()	