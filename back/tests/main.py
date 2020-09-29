import json, requests, time

from utils import *

def test_pytest():
    # time.sleep(20)
    print("SUCCESS")

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
    assert get_profile(user1)["first_name"] == 'Joel'
    logout(user1)

def test_password_lost():
    response = user1["session"].post(f"{url}/reset", data={'email' : user1["email"]})
    print(response, response.text)
    assert response.status_code == 200
    reset_id = json.loads(response.text)["reset_id"]
    user1["password"] = '1O1For€verBb'
    response = user1["session"].post(f"{url}/reset/{user1['id']}/{reset_id}", data={'new_password': user1["password"]})
    print(response, response.text)
    assert response.status_code == 200
    response = login(user1)
    print(response, response.text)
    assert response.status_code == 200
    logout(user1)

def get_curr_user():
    login(user1)
    response = user1.get(f"{url}/profile")
    print(response, response.text)
    data = json.loads(response.text)
    assert data["first_name"] == user1["first_name"]
    logout(user1)

    response = user1.get(f"{url}/profile")
    print(response, response.text)
    assert response.status_code == 400

def get_public_profile():
    login(user1)
    response = user1.get(f"{url}/{user2['id']}")
    print(response, response.text)
    data = json.loads(response.text)
    assert data["first_name"] == user2["first_name"]
    assert 'email' not in data






def test_delete():
    login(user1)
    response = delete(user1)
    assert response.status_code == 200
    login(user2)
    response = delete(user2)
    assert response.status_code == 200
