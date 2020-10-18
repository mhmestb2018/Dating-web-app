import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report, reset)


def test_messages():
    test_content = "Coucou"
    reset(user1)
    reset(user2)
    login(user1)
    login(user2)
    response = user1["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    users_list = response.json()["users"]
    assert len(users_list) == 0

    like(user1, user2)
    like(user2, user1)
    response = user2["session"].post(f"{url}/new_message", json={"user": user1["id"], "content": test_content})
    assert response.status_code == 201

    response = user1["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    users_list = response.json()["users"]
    assert len(users_list) == 1

    response = user2["session"].post(f"{url}/new_message", json={"user": user1["id"], "content": "autre test"})
    assert response.status_code == 201

    last_message = response.json()["message"]

    
    response = user1["session"].post(f"{url}/messages", json={"user": user2["id"]})
    assert response.status_code == 200
    messages_list = response.json()["messages"]
    assert len(messages_list) == 2
    assert messages_list[0]["content"] == test_content

    print("LAST: ", last_message)
    print("LIST:", messages_list, flush=True)
    assert last_message["date"] == messages_list[-1]["date"] and last_message["content"] == messages_list[-1]["content"]
