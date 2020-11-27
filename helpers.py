import datetime
import json


def update_db(users):
	parsed = json.dumps(users, indent=4)

	with open('DB.json','w') as file:
		file.write(parsed)
    
	users = json.load(open('DB.json'))

	return users



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
        