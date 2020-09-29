import requests

url = "http://app:5000"

user1 = {
    "bio": "",
    "email": "test1@gmail.com",
    "first_name": "roger",
    "id": 1,
    "last_name": "UPDATED",
    "orientation": "bisexual",
    "pictures": [],
    "score": 0.0,
    "sex": None,
    "validated": 1,
    "password": "blabla123456",
    "session": requests.Session() 
}

user2 = {
    "bio": "",
    "email": "test2@gmail.com",
    "first_name": "steven",
    "id": 2,
    "last_name": "seagal",
    "orientation": "bisexual",
    "pictures": [],
    "score": 0.0,
    "sex": None,
    "validated": 1,
    "password": "blabla234567",
    "session": requests.Session() 
}
