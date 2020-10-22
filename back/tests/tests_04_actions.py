import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report, reset)

def test_profile_not_connected():
    response = user1["session"].get(f"{url}/profile")
    assert response.status_code != 500

def test_matches():
    reset(user1, picture=False)
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
    like(user2, user1)
    response = user1["session"].post(f"{url}/users")
    assert response.status_code == 200
    print(len(response.json()["users"]), flush=True)
    assert len(response.json()["users"]) == 0 or len(response.json()["users"]) > 20 # populate side-effect tape
    
    unlike(user1, user2)
    unlike(user2, user1)

    logout(user1)
    logout(user2)

def test_blocks():
    reset(user1)
    reset(user2)
    login(user1)
    login(user2)

    # check list is empty at start
    response = user1["session"].get(f"{url}/blocked")
    assert response.status_code == 200
    users_count = len(response.json()["users"])
    assert users_count == 0

    # check database is not empty and count other users
    response = user1["session"].post(f"{url}/users")
    assert response.status_code == 200
    full_count = len(response.json()["users"])
    assert full_count > 0

    # user2 blocks user1 and sees one less user
    response = block(user2, user1)
    assert response.status_code == 200
    response = user1["session"].post(f"{url}/users")
    assert response.status_code == 200
    new_users_count = len(response.json()["users"])
    assert new_users_count == full_count - 1
    
    # user2 should see 1 user in /blocked, which should not be self
    response = user2["session"].get(f"{url}/blocked")
    assert response.status_code == 200
    blocked_count = len(response.json()["users"])
    print(blocked_count)
    assert blocked_count == 1
    assert response.json()["users"][0]["id"] != user2["id"]

    # user 2 cannot block user1 twice
    response = block(user2, user1)
    assert response.status_code == 400

    # user2 unblocks user1
    response = unblock(user2, user1)
    assert response.status_code == 200
    response = user1["session"].post(f"{url}/users")
    assert response.status_code == 200
    # print(f"{len(response.json()['users'])}/{users_count}", response.json(), flush=True)
    assert len(response.json()["users"]) == full_count

    # user2 cannot unblock user1 twice
    response = unblock(user2, user1)
    assert response.status_code == 400

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
    delete(user1)
    create(user1)
    login(user1)
    response = update(user1, {"pictures": ["/test123", "456"]})
