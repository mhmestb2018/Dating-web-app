import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)

def test_tags():
    create(user1, checks=False)
    create(user2, checks=False)
    login(user1)
    response = update(user1, {"pictures": ["/test123", "456"]})
    login(user2)
    response = update(user2, {"pictures": ["/test123", "456"]})

    # Check tags are empty
    response = user1["session"].get(f"{url}/tags")
    # print(response.json(), flush=True)
    assert response.status_code == 200
    data = response.json()
    assert "cigares" not in data["tags"] and "pipe" not in data["tags"]

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
    print(data, flush=True)
    assert "cigares" in data["tags"] and "pipe" in data["tags"]

    # Check relative list is ok
    response = user1["session"].post(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert "cigares" not in data["tags"] and "pipe" not in data["tags"]

    # Check tags can be partially deleted
    response = update(user1, {"tags": ["cigares"]})
    assert response.status_code == 200
    data = response.json()
    assert "cigares" in data["tags"] and "pipe" not in data["tags"]

    # Check tags list is ok
    response = user1["session"].get(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert "cigares" in data["tags"] and "pipe" not in data["tags"]

    # Check relative list is ok
    response = user1["session"].post(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert "cigares" not in data["tags"] and "pipe" not in data["tags"]

    # Check relative list is ok for other user
    response = user2["session"].post(f"{url}/tags")
    assert response.status_code == 200
    data = response.json()
    assert "cigares" in data["tags"] and "pipe" not in data["tags"]

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
