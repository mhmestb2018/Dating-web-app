import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report, reset)


def test_messages():
    test_content = "Coucou"
    reset(user1)
    reset(user2)

    # Check conversations list empty at start
    response = user1["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    users_list = response.json()["conversations"]
    assert len(users_list) == 0

    # MISSING TEST (match required not implemented yet):
    #   Check 403 on new_message before/between likes 

    # mutual like to allow messages
    like(user1, user2)
    like(user2, user1)

    # user2 send to user1
    response = user2["session"].post(f"{url}/new_message", json={"user": user1["id"], "content": test_content})
    assert response.status_code == 201

    # user 1 get 1 conversation with one unread message
    response = user1["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    users_list = response.json()["conversations"]
    assert len(users_list) == 1
    assert users_list[0]["unread"] == 1

    # user 2 sees it too but has 0 unread (as he is the sender)
    response = user2["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    users_list = response.json()["conversations"]
    assert len(users_list) == 1
    assert users_list[0]["unread"] == 0

    # user2 send to user1, again
    response = user2["session"].post(f"{url}/new_message", json={"user": user1["id"], "content": "autre test"})
    assert response.status_code == 201

    # set user2 last message aside for later
    last_message = response.json()["message"]

    # check user1 now sees 2 unreads
    response = user1["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    users_list = response.json()["conversations"]
    assert len(users_list) == 1
    assert users_list[0]["unread"] == 2

    # user 1 should be able to fetch 2 messages, wich should be UNREAD
    response = user1["session"].post(f"{url}/messages", json={"user": user2["id"]})
    assert response.status_code == 200
    messages_list = response.json()["messages"]
    assert len(messages_list) == 2
    assert messages_list[0]["content"] == test_content
    assert messages_list[0]["unread"] == True

    # user 1 should be able to fetch 2 messages, wich should now be READ
    response = user1["session"].post(f"{url}/messages", json={"user": user2["id"]})
    assert response.status_code == 200
    messages_list = response.json()["messages"]
    assert len(messages_list) == 2
    assert messages_list[0]["content"] == test_content
    assert messages_list[0]["unread"] == False

    # user1 has no unread messages anymore
    response = user1["session"].get(f"{url}/conversations")
    assert response.status_code == 200
    conversations_list = response.json()["conversations"]
    assert len(conversations_list) == 1
    print(conversations_list)
    assert conversations_list[0]["unread"] == 0

    # checking messages ordering
    assert last_message["date"] == messages_list[-1]["date"] and last_message["content"] == messages_list[-1]["content"]
