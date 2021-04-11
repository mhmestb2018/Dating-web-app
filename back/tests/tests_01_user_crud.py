import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)

def test_base_content():
    tmp = {
        "bio": "",
        "email": "tesfdfddt1@gmail.com",
        "first_name": "rogdffder",
        "last_name": "UPDATEDdfdfffd",
        "orientation": "bisexual",
        "pictures": [],
        # "score": 0.0,
        "age": 21,
        "sex": "m",
        "lat": 42.0,
        "lon": -1.01,
        "password": "blabla123456",
        "session": requests.Session(),
        "lat": 45.763420,
        "lon": 4.834277
    }
    import copy
    check = copy.deepcopy(tmp)
    del check["session"]
    del check["password"]
    create(tmp)
    login(tmp)
    r = update(tmp, check)
    check["banned"] = 0
    check["validated"] = 1
    check["tags"] = []
    assert r.status_code == 200
    profile = get_profile(tmp)
    check["id"] = profile["id"]
    for k in profile:
        print(k)
        if k not in ["pictures", "last_seen", "lat", "lon", "score", "room"]:
            if check[k] != profile[k]:
                print(check, profile)
            assert check[k] == profile[k]
    delete(tmp)
    logout(tmp)

def test_key_error():
    login(user1)
    import copy
    tmp = copy.deepcopy(user1)
    del tmp["session"]
    r = update(user1, tmp)
    assert r.status_code == 400
    logout(user1)

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
    print(response, response.text)
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
        'password': "biu",
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
    data = response.json()
    assert data["first_name"] == user2["first_name"]

def test_logout():
    assert logout(user1).status_code == 200
    assert logout(user2).status_code == 200

def test_update():
    login(user1)
    res = update(user1, {'first_name': 'Joel'})
    assert res.status_code == 200
    assert res.json()["first_name"] == 'Joel'
    user1["first_name"] = 'Joel'
    assert get_profile(user1)["first_name"] == 'Joel'
    logout(user1)

def test_password_lost():
    response = user1["session"].post(f"{url}/reset", data={'email' : user1["email"]})
    # print(response, response.text)
    assert response.status_code == 200
    reset_id = response.json()["reset_id"]
    user1["password"] = '1O1For€verBb'
    response = user1["session"].post(f"{url}/reset/{user1['id']}/{reset_id}", data={'new_password': user1["password"]})
    # print(response, response.text)
    assert response.status_code == 200
    response = login(user1)
    # print(response, response.text)
    assert response.status_code == 200
    logout(user1)
