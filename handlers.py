import random
import string
import difflib
from helpers import *



def upload_new_post_handler(client,user_name):
	client.send(('Enter your status : ').encode('utf-8'))
	status, cookies = recvData(client, 1024)

	client.send(('<--Choose Visibility-->\n1.Public\n2.Private\n3.Strictly Private\n').encode('utf-8'))
	opt, cookies = recvData(client, 1024)

	if opt=='1':
		visibility = 'public'
	elif opt=='2':
		visibility = 'private'
	else:
		visibility = 'strictly_private'
	
	time_stamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')
	post = [user_name, status, time_stamp, visibility]

	users[user_name]['posts'].append(post.copy())

	post.append("not_seen")
	if visibility=='public' or visibility=='private':
		for friend in users[user_name]['friends']:
			users[friend]['feed'].append(post)
			users[friend]['notifications'].append(f'{user_name} has shared a new post..')

	client.send(('Status updated successfully ..!').encode('utf-8'))
	update_db(users)


def newsfeed_handler(user_name,client):

	newsfeed = users[user_name]['feed']

	arr = []
	
	for index,item in enumerate(newsfeed):
		usr,pst,t,vb,st = item

		if st=="not_seen":
			users[user_name]['feed'][index][4] = "seen"
			arr.append("\033[1m"+usr+"\033[0m"+"\n"+"\n"+pst+"\n--------------------------------------------\n")
	
	if len(newsfeed)-len(arr) >= 2:
		for index,item in enumerate(newsfeed):
			usr,pst,t,vb,st = item

			if st=="seen":
				arr.append("\033[1m"+usr+"\033[0m"+"\n"+"\n"+pst+"\n--------------------------------------------\n")
	


	client.send(("<-- Newsfeed -->\n--------------------------------------------\n" + "\n".join(arr[::-1])).encode('utf-8'))



	update_db(users)

def view_messages_handler(client,user_name,target_friend,type):

	global users
	users = update_db(users.copy())
	
	messages_arr = []

	if target_friend in users[user_name]['msgs']:

		for index,msg in enumerate(users[user_name]['msgs'][target_friend]):
			if msg[0]=='sent' and type=="all":
				m = f'        You: {msg[1]}'
				messages_arr.append(m)
			elif msg[0]=='recieved':

				if msg[3]=='not_seen':
					users[user_name]['msgs'][target_friend][index][3] = 'seen'
				
				m = f'Your Friend: {msg[1]}'
				messages_arr.append(m)


		msgs = "--------------------------------------------\n" + "\n".join(messages_arr) + "\n--------------------------------------------"
		client.send((msgs).encode('utf-8'))

	users = update_db(users.copy())


def chat_handler(user_name,client):

	global users
	users = json.load(open('DB.json')) #importing database

	friends = users[user_name]['friends']

	friends_and_status = []

	for fr in friends:
		if users[fr]['isOnline']==True:
			friends_and_status.append(fr + " ------ " + "Online")
		else:
			friends_and_status.append(fr + " ------ " + "Offline")
	
	client.send(('<--Your Friends -->\n'+'\n'.join(friends_and_status)+'\n\nChoose a friend to start messaging:').encode('utf-8'))

	while True:
		target_friend, cookies = recvData(client, 1024)
		
		if target_friend in users:
			
			if users[target_friend]['isOnline'] == True:
				client.send(('Your Friend is online start messaging..\n').encode('utf-8'))
			else:
				client.send(('Your Friend is offline, your messages may be seen later..').encode('utf-8'))
			
			view_messages_handler(client,user_name,target_friend,"all") # View Previous messages

			msg_flag = False
			while True:

				
				client.send(('\nEnter message || "m" to view messages || "q" to exit').encode('utf-8'))
				messg, cookies = recvData(client, 1024)
				
				if messg.lower()=="q":
					
					users[user_name]['isOnline'] = False;
					users = update_db(users)
					return

				if messg.lower()=="m":

					view_messages_handler(client,user_name,target_friend,"all")
				else:
					
					update_messages(users, user_name, target_friend, messg)
					update_db(users)
					
					view_messages_handler(client,user_name,target_friend,"all")

					if msg_flag == False:
						users[target_friend]['notifications'].append([f'You have new message/s from {user_name}', datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')])
						msg_flag = True
					update_db(users)
			
				
		else:
			client.send(('Enter a valid friend name ...').encode('utf-8'))

def frndreqts_handler(user_name,client):

	friendreqts = users[user_name]['frnd_reqts']

	client.send(('<--Your Friends requests -->\n'+'\n'.join(friendreqts)+'\n\nChoose a request to accept or remove:').encode('utf-8'))

	target_user, cookies = recvData(client, 1024)

	if target_user in friendreqts:
		homeoptions = '''
	 Choose an action:

	 1.accept
	 2.remove
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt, cookies = recvData(client, 1024)

		if opt=='1':
			
			users[user_name]['friends'].append(target_user)
			users[user_name]['frnd_reqts'].remove(target_user)

			users[target_user]['notifications'].append([f"{user_name} has accepted your request.", datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')])

			users[target_user]['friends'].append(user_name)
			users[target_user]['notifications'].append([f"{user_name} has accepted your request.", datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')])
			client.send((f"You and {target_user} are now friends").encode('utf-8'))
			
		elif opt=='2':
			users[user_name]['frnd_reqts'].remove(target_user)

	update_db(users) 

def search_handler(user_name,client):

	registered_users= list(users.keys())
	friends = users[user_name]['friends']

	client.send(('<--Search any registered Users -->\n').encode('utf-8'))
	first_search, cookies = recvData(client, 1024)
	

	if first_search not in registered_users:
		
			matched_users=difflib.get_close_matches(first_search, registered_users,5)
			if len(matched_users) == 0:
				client.send(('user not found').encode('utf-8'))
			else:
				client.send(('**Your search suggestion **\n'+'\n'.join(matched_users)+'\n\nChoose a suggestion || "q" to exit').encode('utf-8'))
				subsequent_search, cookies = recvData(client, 1024)

				if subsequent_search=="q":
					return;

				elif subsequent_search in registered_users:
					if subsequent_search in friends: 
						friends_handler(user_name,subsequent_search,client)
					elif first_search == user_name:
						you_handler(subsequent_search,client)
					else:
						nonfriends_handler(user_name,subsequent_search,client)
			

	else:
		if first_search in friends: 
			friends_handler(user_name,first_search,client)
		elif first_search == user_name:
			you_handler(first_search,client)
		else:
			nonfriends_handler(user_name,first_search,client)
		
	update_db(users)

	

def nonfriends_handler(user_name,first_search,client):
	
		homeoptions = f'''

		{first_search}'s profile

	 1. timeline
	 2. friends
	 3. Add as friend
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt, cookies = recvData(client, 1024)
		if opt=='1':
			view_timeline_handler(first_search,client,'others')
			#some comment
		
		elif opt=='2':
			target_friends = users[first_search]['friends']
			client.send((f"**{first_search}'s Friends **\n"+'\n'.join(target_friends)).encode('utf-8'))

		elif opt == "3":
			
			users[first_search]['frnd_reqts'].append(user_name)
			client.send((f'Your request sucessfully sent  to: {first_search}').encode('utf-8'))
			users[first_search]['notifications'].append([f"{user_name} sent you a friend request.", datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')])
	
	

def friends_handler(user_name,first_search,client):

		homeoptions = f'''

		{first_search}'s profile

	 1. timeline
	 2. friends 
	 3. remove
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt, cookies = recvData(client, 1024)

		if opt=='1':
			view_timeline_handler(first_search,client,'others')
			#some comment
		
		elif opt=='2':
			target_friends = users[first_search]['friends']
			client.send((f"**{first_search}'s Friends **\n"+'\n'.join(target_friends)).encode('utf-8'))
		
		elif opt=='3':
			users[user_name]['friends'].remove(first_search)
			users[first_search]['friends'].remove(user_name)
			client.send((f"You are no longer friends with {target_user}").encode('utf-8'))

		

def you_handler(first_search,client):
	
		homeoptions = f'''

		{first_search}'s(You) profile

	 1. timeline
	 2. friends 
	 
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt, cookies = recvData(client, 1024)

		if opt=='1':
			view_timeline_handler(first_search,client,'own')
			#some comment
		
		elif opt=='2':
			target_friends = users[first_search]['friends']
			client.send((f"**{first_search}'s Friends **\n"+'\n'.join(target_friends)).encode('utf-8'))


def view_timeline_handler(user_name,client,type):

	timeline = users[user_name]['posts']

	arr =[]
	if type=="other":

		for i in timeline:

			if i[2]=='public' or  i[2]=='private':

				strng = "   ".join(i)
				arr.append(strng)
	
	elif type=="own":

		for i in timeline:

			if i[2]=='public' or  i[2]=='private' or i[2]=='strictly_private':

				strng = "   ".join(i)
				arr.append(strng)

	
	prof = " view profile details \n--------------------------------------------\n" + "\n".join(arr) + "\n--------------------------------------------"
	client.send((prof).encode('utf-8'))


def yourfriends_handler(user_name,client):
	
	friends = users[user_name]['friends']

	client.send(('**Your Friends **\n'+'\n'.join(friends)+'\n\nChoose a friend:').encode('utf-8'))

	target_user, cookies = recvData(client, 1024)

	if target_user in friends:
		homeoptions = f'''

		{target_user}'s profile

	 1. timeline
	 2. friends 
	 3. remove
	 '''
		client.send(homeoptions.encode('utf-8'))

		opt, cookies = recvData(client, 1024)

		if opt=='1':
			view_timeline_handler(target_user,client,'others')
			#some comment
		
		elif opt=='2':
			target_friends = users[target_user]['friends']
			client.send((f"**{target_user}'s Friends **\n"+'\n'.join(target_friends)).encode('utf-8'))
		
		elif opt=='3':
			users[user_name]['friends'].remove(target_user)
			users[target_user]['friends'].remove(user_name)
			client.send((f"You are no longer friends with {target_user}").encode('utf-8'))

		
	update_db(users) 

 


def notifications_handler(user_name,client):

	Notifications = users[user_name]['notifications']

	arr = []
	
	for nf,t in Notifications:
		arr.append(nf+"            "+t)
	
		
	client.send(("<-- Notifications -->\n--------------------------------------------\n" + "\n".join(arr[::-1]) + "\n--------------------------------------------").encode('utf-8'))



	update_db(users) 



def register_handler(client):
	client.send(('REgister  \n\n** Enter Email**').encode('utf-8'))
	email, cookies = recvData(client, 1024)

	client.send(('\n\n** Enter Username**').encode('utf-8'))
	user_name, cookies = recvData(client, 1024)

	client.send(('**Password**').encode('utf-8'))
	pswd, cookies = recvData(client, 1024)

	client.send(('**Confirm Password**').encode('utf-8'))
	confirm_pswd, cookies = recvData(client, 1024)

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
		"posts": [],
		"feed": [],
		"notifications": []
	}


	client.send((f'Successfully Registered In as {email}').encode('utf-8'))




	update_db(users) 

	return email;


def login_handler(client):
	global users
	global session

	
	client.send(('Log in... \n\n**Username**').encode('utf-8'))
	
	usr, cookies = recvData(client, 1024)

	client.send(('**Password**').encode('utf-8'))
	pswd, cookies = recvData(client, 1024)


	if usr not in users or users[usr]['password'] != pswd:
		client.send(('Invalid credentials..').encode('utf-8'))
		return None;

	client.send((f'Successfully Logged In as {usr}').encode('utf-8'))

	


	new_cookie = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
	set_cookie(client,session,usr,new_cookie)
	

	
	users = update_db(users) 
	session = update_session(session)

	return usr;

