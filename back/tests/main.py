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

def signup(user, value=201):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = user["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == value
    tmp = json.loads(response.text)
    if "validation_id" in tmp:
        return tmp["validation_id"]
    return None

def login(user, value=200):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'remember_me': True
    }
    response = user["session"].post(f"{url}/login", data=payload)
    print(response)
    assert response.status_code == value
    return json.loads(response.text)

def validate(user, validation_id, value=200):
    response = user["session"].post(f"{url}/validate/{validation_id}")
    print(response)
    assert response.status_code == value

def create(user):
    validation_id = signup(user)
    validate(user, validation_id)

def delete(user, value=200):
    response = user["session"].delete(f"{url}/profile")
    print(response)
    assert response.status_code == value

def logout(user, value=200):
    response = user["session"].post(f"{url}/logout")
    print(response)
    assert response.status_code == value

def test_create():
    create(user1)
    create(user2)

def test_recreate():
    signup(user1, value=409)

def test_bad_create():
    payload = {
        'email': "testets@flhsldfn.fr",
        'password': user1["password"],
        'first_name': "",
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400

    payload = {
        'email': "testets@.fr",
        'password': user1["password"],
        'first_name': "henri",
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400

    payload = {
        'email': "@flhsldfn.fr",
        'password': user1["password"],
        'first_name': "henri",
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400

    payload = {
        'email': "testetsflhsldfn.fr",
        'password': user1["password"],
        'first_name': "henri",
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400

    payload = {
        'email': "testets@flhsldfn",
        'password': user1["password"],
        'first_name': "henri",
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400

    payload = {
        'email': "testets@flhsldfn.fr",
        'password': "biuhg",
        'first_name': "henri",
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400

    payload = {
        'email': "testets@flhsldfn.fr",
        'password': user1["password"],
        'last_name': user1["last_name"]
    }
    response = user1["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    assert response.status_code == 400


def test_login():
    login(user1)
    login(user2)

def test_logout():
    logout(user1)
    logout(user2)
    login(user1)
    login(user2)


def test_delete():
    delete(user1)
    delete(user2)

