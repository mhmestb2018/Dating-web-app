import json, requests, time

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
    # time.sleep(20)
    print("SUCCESS")

def signup_user(user, value=201):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = user["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == value
    return json.loads(response.text)["validation_id"]

def login_user(user, value=200):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'remember_me': True
    }
    response = user["session"].post(f"{url}/login", data=payload)
    print(response)
    assert response.status_code == value
    return json.loads(response.text)

def validate_user(user, validation_id, value=200):
    response = user["session"].post(f"{url}/validate/{validation_id}")
    print(response)
    assert response.status_code == value

def create_user(user):
    validation_id = signup_user(user)
    validate_user(user, validation_id)

def delete_user(user, value=200):
    response = user["session"].delete(f"{url}/profile")
    print(response)
    assert response.status_code == value

def logout_user(user, value=200):
    response = user["session"].post(f"{url}/logout")
    print(response)
    assert response.status_code == value

def test_create_user():
    create_user(user1)
    create_user(user2)

def test_login_user():
    login_user(user1)
    login_user(user2)

def test_logout_user():
    logout_user(user1)
    logout_user(user2)
    login_user(user1)
    login_user(user2)

def test_delete_user():
    delete_user(user1)
    delete_user(user2)

