import json



users = {
    "test1": {
        "password": "pass1",
        "isOnline": True,
        "msgs": {
            
        },
        "frnd_reqts": [],
        "friends": [
            "test2",
            "test3",
            "test4"
        ],
        "timeline": []
    },
    "test2": {
        "password": "pass2",
        "isOnline": True,
        "msgs": {
            
        },
        "frnd_reqts": [],
        "friends": [
            "test1"
        ],
        "timeline": []
    },
    "test3": {
        "password": "pass3",
        "isOnline": True,
        "msgs": {
            
        },
        "frnd_reqts": [],
        "friends": [
            "test1"
        ],
        "timeline": []
    },
    "test4": {
        "password": "pass4",
        "isOnline": False,
        "msgs": {
            
        },
        "frnd_reqts": [],
        "friends": [
            "test1"
        ],
        "timeline": []
    }
}


def update_db():
	parsed = json.dumps(users, indent=4)

	with open('DB.json','w') as file:
		file.write(parsed)


update_db()