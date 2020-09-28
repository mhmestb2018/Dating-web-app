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

def signup(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = user["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    tmp = json.loads(response.text)
    return response

def login(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'remember_me': True
    }
    response = user["session"].post(f"{url}/login", data=payload)
    print(response)
    return response

def validate(user, validation_id):
    response = user["session"].post(f"{url}/validate/{validation_id}")
    print(response)
    return response

def create(user, checks=True):
    response = signup(user)
    assert response.status_code == 201
    data = json.loads(response.text)
    response = validate(user, data["validation_id"])
    assert response.status_code == 200

def delete(user):
    response = user["session"].delete(f"{url}/profile")
    print(response)
    return response

def logout(user):
    response = user["session"].post(f"{url}/logout")
    print(response)
    return response

def test_create():
    create(user1)
    create(user2)

def test_recreate():
    response = signup(user1)
    assert response.status_code == 409

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

def update(user, data):
    response = user["session"].put(f"{url}/profile", data=data)
    return response

def test_login():
    response = login(user1)
    assert response.status_code == 200
    response = login(user2)
    assert response.status_code == 200
    data = json.loads(response.text)
    assert data["first_name"] == user2["first_name"]

def test_logout():
    assert logout(user1).status_code == 200
    assert logout(user2).status_code == 200

def test_update():
    login(user1)
    res = update(user1, {'first_name': 'Joel'})
    assert res.status_code == 200
    res = json.loads(res.text)
    assert res["first_name"] == 'Joel'
    user1["first_name"] = 'Joel'
    logout(user1)

def test_delete():
    login(user1)
    response = delete(user1)
    assert response.status_code == 200
    login(user2)
    response = delete(user2)
    assert response.status_code == 200

