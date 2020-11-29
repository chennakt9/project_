import datetime
import json
import ast
import time


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
	
	session = json.load(open('DB.json'))

	return session


def set_cookie(client,session,usr,new_cookie):
	time_stamp = (datetime.datetime.now()+ datetime.timedelta(days=5)).strftime('%d-%m-%Y %H:%M:%S.%f')
	session[new_cookie] = {"user":usr,"expires_on": time_stamp}
	update_session(session) 
	cookie_data = "set_cookie" + "|" + new_cookie + "|" + str({"expires_on":time_stamp})
	client.send(cookie_data.encode('utf-8'))



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
