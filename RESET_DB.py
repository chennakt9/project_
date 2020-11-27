import json



users = dict(
    test1 = dict(password = "pass1", friends = list(["test2","test3","test4"]) , isOnline =  False , msgs = dict(), frnd_reqts = list() ,  timeline = list() , feed = list() , notifications = list()),
    test2 = dict(password = "pass2", friends = list(["test1"]) , isOnline =  False , msgs = dict(), frnd_reqts = list() ,  timeline = list() , feed = list() , notifications = list()),
    test3 = dict(password = "pass3", friends = list(["test1"]) , isOnline =  False , msgs = dict(), frnd_reqts = list() ,  timeline = list() , feed = list() , notifications = list()),
    test4 = dict(password = "pass4", friends = list(["test1"]) , isOnline =  False , msgs = dict(), frnd_reqts = list() ,  timeline = list() , feed = list() , notifications = list())
)


def update_db():
	parsed = json.dumps(users, indent=4)

	with open('DB.json','w') as file:
		file.write(parsed)


update_db()