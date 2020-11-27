import socket
import threading
import json
import datetime
import pprint

#custom modules import
from helpers import *

HOST = '127.0.0.1'
PORT = 12345



users = json.load(open('DB.json')) #importing database



def login_handler(client):
	client.send(('Log in... \n\n**Username**').encode('utf-8'))
	usr = client.recv(1024).decode('utf-8')

	client.send(('**Password**').encode('utf-8'))
	pswd = client.recv(1024).decode('utf-8')


	if usr not in users or users[usr]['password'] != pswd:
		client.send(('Invalid credentials..').encode('utf-8'))
		client.close()
		return;

	client.send((f'Successfully Logged In as {usr}').encode('utf-8'))

	users[usr]['isOnline'] = True;


	update_db(users) 

	return usr;


def view_messages_handler(client,user_name,target_friend):

	global users
	users = update_db(users.copy())
	# pprint.pprint(users)
	


	messages_arr = []

	if target_friend in users[user_name]['msgs']:

		for msg in users[user_name]['msgs'][target_friend]:
			if msg[0]=='sent':
				m = f'        You: {msg[1]}'
				messages_arr.append(m)
			else:
				m = f'Your Friend: {msg[1]}'
				messages_arr.append(m)

		msgs = "--------------------------------------------\n" + "\n".join(messages_arr) + "\n--------------------------------------------"
		client.send((msgs).encode('utf-8'))



def chat_handler(user_name,client):

	friends = users[user_name]['friends']

	client.send(('**Your Friends **\n'+'\n'.join(friends)+'\n\nChoose a friend to start messaging:').encode('utf-8'))

	while True:
		target_friend = client.recv(1024).decode('utf-8')

		if target_friend in users:
			
			if users[target_friend]['isOnline'] == True:
				client.send(('Your Friend is online start messaging..\n').encode('utf-8'))
			else:
				client.send(('Your Friend is offline, your messages may be seen later..').encode('utf-8'))
			
			view_messages_handler(client,user_name,target_friend) # View Previous messages

			while True:

				
				client.send(('\nEnter message || "m" to view messages || "q" to exit').encode('utf-8'))
				messg = client.recv(1024).decode('utf-8')
				
				if messg.lower()=="q":
					return

				if messg.lower()=="m":

					view_messages_handler(client,user_name,target_friend)
				else:
					
					update_messages(users, user_name, target_friend, messg)
					update_db(users)
					
					view_messages_handler(client,user_name,target_friend)
			
				
		else:
			client.send(('Enter a valid friend name ...').encode('utf-8'))

def frndreqts_handler(user_name,client):

	friendreqts = users[user_name]['frnd_reqts']

	client.send(('**Your Friends requests **\n'+'\n'.join(friendreqts)+'\n\nChoose a request to accept or remove:').encode('utf-8'))

	target_user = client.recv(1024).decode('utf-8')

	if target_user in friendreqts:
		homeoptions = '''
	 Choose an action:

	 1.accept
	 2.remove
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt = client.recv(1024).decode('utf-8')

		if opt=='1':
			
			users[user_name]['friends'].append(target_user)
			users[user_name]['frnd_reqts'].remove(target_user)
			users[target_user]['notifications'].append(f"{user_name} has accepted your request.")
			
			
		elif opt=='2':
			users[user_name]['frnd_reqts'].remove(target_user)
	update_db(users) 

def friends_handler(user_name,client):
	
	friends = users[user_name]['friends']

	client.send(('**Your Friends **\n'+'\n'.join(friends)+'\n\nChoose a friend:').encode('utf-8'))

	target_user = client.recv(1024).decode('utf-8')

	if target_user in friends:
		homeoptions = f'''
	 Choose an action:

	 1.{target_user}'s timeline
	 2.{target_user}'s friends
	 3.remove
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt = client.recv(1024).decode('utf-8')

		if opt=='1':
			pass #timeline work by anitha
		
		elif opt=='2':
			target_friends = users[target_user]['friends']
			client.send((f"**{target_user}'s Friends **\n"+'\n'.join(target_friends)).encode('utf-8'))
		
		elif opt=='3':
			users[user_name]['friends'].remove(target_user)
			users[target_user]['friends'].remove(user_name)

		
	update_db(users) 

def Notifications_handler(user_name,client):

	Notifications = users[user_name]['notifications']

	client.send(("** Notifications **\n"+'\n'.join(Notifications)).encode('utf-8'))

	update_db(users) 






def register_handler(client):
	client.send(('REgister  \n\n** Enter Email**').encode('utf-8'))
	email = client.recv(1024).decode('utf-8')

	client.send(('\n\n** Enter Username**').encode('utf-8'))
	user_name = client.recv(1024).decode('utf-8')

	client.send(('**Password**').encode('utf-8'))
	pswd = client.recv(1024).decode('utf-8')

	client.send(('**Confirm Password**').encode('utf-8'))
	confirm_pswd = client.recv(1024).decode('utf-8')

	if confirm_pswd!=pswd:
		client.send(('Passwords not match..').encode('utf-8'))
		client.close()
		return None

	users[user_name] = {
        "password": pswd,
        "friends": [],
        "isOnline": False,
        "msgs": {},
        "frnd_reqts": [],
        "timeline": [],
        "feed": [],
        "notifications": []
    }

	client.send((f'Successfully REgister In as {email}').encode('utf-8'))




	update_db(users) 

	return email;


def client_thread(client):

	login_page_options = '''
	**Login/Register Page**
	Choose an action:

	1.REgiter
	2.Login
	'''
	
	client.send(login_page_options.encode('utf-8'))

	opt = client.recv(1024).decode('utf-8')

	if opt=='1':
		register_handler(client) #register
	elif opt=='2':
		user_name = login_handler(client) #login

	

	

	while True:
		home_page_options = '''
	**Home Page**
	Choose an action:

	1. Send Private Message | 5. Upload new post
	2. Search Reg Users     | 6. Notifications
	3. View Chats           | 7. My Profile/TimeLine
	4. Friend Options       | 8. logout
	'''
		client.send(home_page_options.encode('utf-8'))
		data = client.recv(1024).decode('utf-8')

		if data=='1': # private message

			chat_handler(user_name, client)
		
		elif data=='2': # search registered users
			client.send(('Not implemented yet').encode('utf-8'))
			
		elif data=='3': # view chats
			
			friends = users[user_name]['friends']

			client.send(('**Your Friends **\n'+'\n'.join(friends)+'\n\nChoose a friend:').encode('utf-8'))

			target_friend = client.recv(1024).decode('utf-8')

			view_messages_handler(client,user_name,target_friend)

		elif data=='4': # Friend Options
			

			while True:
				
				friend_options = '''
  **Friend-Options Page**
  Choose an action:
  1. view friends 
  2. view friend requests --> acc or rej friend request
  3. exit friend options
								
		'''
				client.send(friend_options.encode('utf-8'))

				opt = client.recv(1024).decode('utf-8')

				if opt=='1':
					friends_handler(user_name,client)
				elif opt =='2':
					frndreqts_handler(user_name,client)
				elif opt == '3':
					break
				else:
					continue


		
			

		elif data=='5': # Upload New post
			client.send(('Not implemented yet').encode('utf-8'))

		elif data=='6': # Notifications
			Notifications_handler(user_name,client)

		elif data=='8': # logout
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