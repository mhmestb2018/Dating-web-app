import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report, reset)

def test_notifications():
    reset(user1)
    reset(user2)

    # Check conversations list empty at start
    response = user1["session"].get(f"{url}/notifications")
    assert response.status_code == 200
    notifs_list = response.json()["notifications"]
    assert len(notifs_list) == 0

    # mutual like to allow messages
    like(user1, user2)
    like(user2, user1)

    # user2 send to user1
    response = user2["session"].post(f"{url}/new_message", json={"user": user1["id"], "content": "pcachin"})
    assert response.status_code == 201
    response = user1["session"].get(f"{url}/notifications")
    notifs_list = response.json()["notifications"]
    print(notifs_list)
    assert len(notifs_list) == 2
    assert notifs_list[0]["type"] == "message"
    assert notifs_list[1]["type"] == "match"
    assert response.json()["unread"] == 2
    assert notifs_list[0]["unread"] == True
    assert notifs_list[1]["unread"] == True


    response = user1["session"].put(f"{url}/notifications")
    response = user1["session"].get(f"{url}/notifications")
    notifs_list = response.json()["notifications"]
    assert len(notifs_list) == 2
    assert response.json()["unread"] == 0
    assert notifs_list[0]["unread"] == False
    assert notifs_list[1]["unread"] == False

    user2_id = user2["session"].get(f"{url}/profile").json()['id']
    profile = user1["session"].get(f"{url}/users/{user2_id}")
    response = user2["session"].get(f"{url}/notifications")
    notifs_list = response.json()["notifications"]
    assert len(notifs_list) == 2
    assert notifs_list[0]["type"] == "visit"
    assert notifs_list[1]["type"] == "like"
    