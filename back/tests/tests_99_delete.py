import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)

def test_delete():
    create(user1, checks=False)
    login(user1)
    response = delete(user1)
    logout(user1)
    assert response.status_code == 200
    create(user2, checks=False)
    login(user2)
    response = delete(user2)
    logout(user2)
    assert response.status_code == 200
