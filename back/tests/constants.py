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
    "age": 21,
    "sex": None,
    "validated": 1,
    "password": "blabla123456",
    "banned": 0,
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
    "age": 24,
    "sex": None,
    "validated": 1,
    "password": "blabla234567",
    "banned": 0,
    "session": requests.Session() 
}
