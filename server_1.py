import socket
import threading
import json
import sys
import datetime





#custom modules import
from helpers import *
from handlers import *


 
for cookie in list(session): ##Removing Expired Cookies
	curr_datetime = datetime.datetime.now()
	cookie_datetime = datetime.datetime.strptime(session[cookie]['expires_on'], '%d-%m-%Y %H:%M:%S.%f')

	if cookie_datetime<curr_datetime:
		del session[cookie]
		update_session(session)





def client_thread(client):

	while True:

		global users
		users = json.load(open('DB.json')) #importing database
		
		global session
		session = json.load(open('SESSION.json')) #importing session management database

		print("session in server 1 : ", session)

		login_page_options = '''
		<==== Login/Register Page ====>
		Choose an action:

		1.Register
		2.Login
		'''
		
		client.send(login_page_options.encode('utf-8'))

		opt, cookies = recvData(client, 1024)

		if opt=='1':
			register_handler(client) #register
		elif opt=='2':

			isLoggedIn = False

			for cookie in cookies:
				if cookie in session:
					isLoggedIn = True
					break
			
			if isLoggedIn==True:
				user_name = session[cookie]['user']
				client.send((f'Successfully Logged In as {user_name}').encode('utf-8'))
				break
			else:

				user_name = login_handler(client) #login

				if user_name is not None:
					break
				else:
					continue

	
	while True:
		home_page_options = '''
	<==== Home Page ====>
	Choose an action:

	1. Send Private Message | 6. Upload new post
	2. Search Reg Users     | 7. Notifications
	3. View Chats           | 8. My Profile/TimeLine
	4. Friend Options       | 9. logout
	5. Newsfeed
	'''
		client.send(home_page_options.encode('utf-8'))

		data, cookies = recvData(client, 1024)



		if data=='1': # private message
			

			users[user_name]['isOnline'] = True;
			users = update_db(users)

			chat_handler(user_name, client)
		
		elif data=='2': # search registered users
			search_handler(user_name,client)			
		elif data=='3': # view chats
			
			friends = users[user_name]['friends']

			client.send(('**Your Friends **\n'+'\n'.join(friends)+'\n\nChoose a friend:').encode('utf-8'))

			target_friend, cookies = recvData(client, 1024)

			while True:

				view_messages_handler(client,user_name,target_friend)
				client.send(('Enter "q" to exit').encode('utf-8'))
				opt, cookies = recvData(client, 1024)

				if opt=="q":
					break

		elif data=='4': # Friend Options
			

			while True:
				
				friend_options = '''
  <--Friend-Options Page-->
  Choose an action:
  1. view friends 
  2. view friend requests --> acc or rej friend request
  3. exit friend options
								
		'''
				client.send(friend_options.encode('utf-8'))

				opt, cookies = recvData(client, 1024)

				if opt=='1':
					yourfriends_handler(user_name,client)
				elif opt =='2':
					frndreqts_handler(user_name,client)
				elif opt == '3':
					break
				else:
					continue


		elif data=='6': # Upload New post
			upload_new_post_handler(client,user_name)

		elif data=='7': # Notifications

			while True:
				notifications_handler(user_name,client)

				client.send(('Enter "q" to exit').encode('utf-8'))
				opt, cookies = recvData(client, 1024)

				if opt=="q":
					break
		
		elif data =='8': #My Profile/My Timeline
			view_timeline_handler(user_name,client,"own")

		elif data=='5':
			newsfeed_handler(user_name,client)
		
		elif data=='9': # logout

			users[user_name]['isOnline'] = False
			
			update_db(users) #Update users DB

			cookie = ''
			for ck in session:
				if session[ck]['user']==user_name:
					cookie = ck
					break
			
			# print(cookie,session)

			del session[cookie]
			update_session(session)   # update server side session after logout

			if user_name=="test1":
				file = 'cookie_file_1.json'
			elif user_name =="test2":
				file = 'cookie_file_2.json'
			elif user_name =="test3":
				file = 'cookie_file_3.json'

			cookies = json.load(open(file))   # update client side cookies after logout
			del cookies[cookie]    
			parsed = json.dumps(cookies, indent=4)    
			with open(file,'w') as file:
				file.write(parsed)

			client.send(('Logged out successfully !!').encode('utf-8'))
			client.close()
			break






if len(sys.argv)==1:
	HOST = '127.0.0.1'
	PORT = 12345
if len(sys.argv)==2:
	HOST = sys.argv[1]
	PORT = 12345

if len(sys.argv)==3:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])

		
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
