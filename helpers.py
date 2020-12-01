import datetime
import json
import ast



users = json.load(open('DB.json')) #importing database
session = json.load(open('SESSION.json')) #importing session management database


def update_db(users):
	parsed = json.dumps(users, indent=4)

	with open('DB.json','w') as file:
		file.write(parsed)
	
	users = json.load(open('DB.json'))

	return users

def update_session(session):
	parsed = json.dumps(session, indent=4)

	with open('SESSION.json','w') as file:
		file.write(parsed)
	
	session = json.load(open('SESSION.json'))

	return session


def set_cookie(client,session,usr,new_cookie):
	time_stamp = (datetime.datetime.now()+ datetime.timedelta(days=5)).strftime('%d-%m-%Y %H:%M:%S.%f')
	session[new_cookie] = {"user":usr,"expires_on": time_stamp}
	update_session(session)

	cookies = json.load(open('cookie_file_1.json'))   # update client side cookies after login
	cookies[new_cookie] = {"expires_on":time_stamp}
	parsed = json.dumps(cookies, indent=4)    
	with open('cookie_file_1.json','w') as file:
		file.write(parsed)
			




def update_messages(users, sender, reciever, messg):
	

	sent_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')

	msg = ['sent', messg, sent_time]
	if reciever not in users[sender]['msgs']:
		users[sender]['msgs'][reciever] = [ msg ]
	else:
		users[sender]['msgs'][reciever].append( msg )


	recv_time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')

	msg = ['recieved', messg, recv_time, 'not_seen']
	if sender not in users[reciever]['msgs']:
		users[reciever]['msgs'][sender] = [ msg ]
	else:
		users[reciever]['msgs'][sender].append( msg )


def recvData (client, size):

	data, cookies = client.recv(1024).decode('utf-8').split("|")


	client_data = (data,ast.literal_eval(cookies))


	return client_data
