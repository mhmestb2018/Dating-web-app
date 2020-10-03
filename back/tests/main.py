import requests, time, datetime
from constants import url, user1, user2
from utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)

def wait_startup():
    response = None
    i = 0
    while response is None and i < 30:
        try:
            response = user1["session"].get({"url"})
        except:
            print("Not able to reach backend yet, waiting 3 seconds...", flush=True)
            time.sleep(3)
        i += 1
    assert response.status_code == 200

def test_clean_failed_attempts():
    login(user1)
    delete(user1)
    logout(user1)
    login(user2)
    delete(user2)
    logout(user2)
    print("SUCCESS")

def test_create():
    create(user1)
    create(user2)

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
        "session": requests.Session() 
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
        if k not in ["pictures", "last_seen", "lat", "lon", "score"]:
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

def test_matches():
    login(user1)
    login(user2)
    response = like(user1, user2)
    # print(response, response.text)
    assert response.status_code == 403
    response = update(user1, {"pictures": ["/test123", "456"]})
    # print(response, response.text)
    assert response.status_code == 200
    response = update(user2, {"pictures": ["/test2"]})
    # print(response, response.text)
    assert response.status_code == 200

    response = like(user1, user2)
    # print(response, response.text)
    assert response.status_code == 200
    assert response.json()["match"] == False
    response = like(user2, user1)
    # print(response, response.text)
    assert response.status_code == 200
    assert response.json()["match"] == True

    response = user1["session"].get(f"{url}/matches")
    # print(response, response.text)
    assert response.status_code == 200
    assert len(response.json()["users"]) == 1

    response = unlike(user2, user1)
    # print(response, response.text)
    assert response.status_code == 200
    assert response.json()["match"] == False
    response = user1["session"].get(f"{url}/matches")
    # print(response, response.text)
    assert response.status_code == 200
    assert len(response.json()["users"]) == 0
    unlike(user1, user2)

    like(user1, user2)
    print(like(user2, user1).json(), flush=True)
    response = user1["session"].get(f"{url}/users")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 0
    
    unlike(user1, user2)
    unlike(user2, user1)

    logout(user1)
    logout(user2)

def test_blocks():
    login(user1)
    login(user2)

    response = user1["session"].get(f"{url}/users")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 1

    response = block(user2, user1)
    assert response.status_code == 200
    response = user1["session"].get(f"{url}/users")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 0

    response = block(user2, user1)
    assert response.status_code == 400

    response = unblock(user2, user1)
    assert response.status_code == 200
    response = user1["session"].get(f"{url}/users")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 1

    response = unblock(user2, user1)
    assert response.status_code == 400

    logout(user1)
    logout(user2)

def test_liked_by():
    login(user1)
    login(user2)

    response = user1["session"].get(f"{url}/liked_by")
    print(response, response.text)
    assert response.status_code == 200
    assert len(response.json()["users"]) == 0

    response = like(user1, user2)
    print(response, response.text)
    assert response.status_code == 200

    response = user2["session"].get(f"{url}/liked_by")
    print(response, response.text)
    assert response.status_code == 200
    assert len(response.json()["users"]) == 1
    
    like(user1, user2)
    like(user2, user1)

    response = user2["session"].get(f"{url}/liked_by")
    print(response, response.text)
    assert response.status_code == 200
    assert len(response.json()["users"]) == 1
    
    unlike(user1, user2)
    unlike(user2, user1)

    logout(user1)
    logout(user2)

def test_last_seen():
    login(user2)
    time.sleep(2)
    t1 = datetime.datetime.now()

    login(user1)
    # 'Tue, 29 Sep 2020 00:00:00 GMT'
    assert datetime.datetime.strptime(get_public_profile(user1, user2)["last_seen"], "%a, %d %b %Y %H:%M:%S GMT") < t1
    time.sleep(2)
    get_profile(user2)
    assert datetime.datetime.strptime(get_public_profile(user1, user2)["last_seen"], "%a, %d %b %Y %H:%M:%S GMT") > t1

    logout(user1)
    logout(user2)

def test_report():
    login(user1)
    delete(user1)
    create(user1)
    login(user1)
    response = update(user1, {"pictures": ["/test123", "456"]})
    assert response.status_code == 200
    login(user1)
    login(user2)
    response = report(user2, user1)
    assert response.status_code == 200
    response = report(user2, user1)
    assert response.status_code == 400
    response = like(user1, user2)
    assert response.status_code == 403

def test_delete():
    login(user1)
    response = delete(user1)
    logout(user1)
    assert response.status_code == 200
    login(user2)
    response = delete(user2)
    logout(user2)
    assert response.status_code == 200

def test_profile_not_connected():
    response = user1["session"].get(f"{url}/profile")
    assert response.status_code != 500

def test_tags():
    create(user1)
    create(user2)
    login(user1)
    response = update(user1, {"pictures": ["/test123", "456"]})
    login(user2)
    response = update(user2, {"pictures": ["/test123", "456"]})

    # Check tags are empty
    response = user1["session"].get(f"{url}/tags")
    print(response.json(), flush=True)
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == []

    # Check user tags are empty
    response = user1["session"].get(f"{url}/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == []

    # Check tags can be added
    response = update(user1, {"tags": ["pipe", "cigares"]})
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["pipe", "cigares"]

    # Check tags list is ok
    response = user1["session"].get(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["pipe", "cigares"]

    # Check relative list is ok
    response = user1["session"].post(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == []

    # Check tags can be partially deleted
    response = update(user1, {"tags": ["cigares"]})
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["cigares"]

    # Check tags list is ok
    response = user1["session"].get(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["cigares"]

    # Check relative list is ok
    response = user1["session"].post(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == []

    # Check relative list is ok for other user
    response = user2["session"].post(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["cigares"]

    # Check invalid tag does trigger error and has no side effects
    response = update(user1, {"tags": [""]})
    assert response.status_code == 400
    response = user1["session"].get(f"{url}/profile")
    data = response.json()
    assert data["tags"] == ["cigares"]

    delete(user1)
    delete(user2)
    logout(user1)
    logout(user2)
