import json, requests, os

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

def test_pytest():
    print("SUCCESS")

def send_post_request(url, user, args={}):
    response = user["session"].post(url, data=json.dumps(args))
    print(response.text)
    return response

def signin_user(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = send_post_request(url=f"{url}/signup", user=user, args=payload)
    assert response.status_code == 201

def login_user(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'remember_me': True
    }
    response = send_post_request(url=f"{url}/login", user=user, args=payload)
    assert response.status_code == 200

def test_create_user():
    signin_user(user1)
    signin_user(user2)

def test_login_user():
    login_user(user1)
    login_user(user2)

