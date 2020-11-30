import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)

random.seed(42)

def test_pytest():
    assert 1 == 1

def test_wait_startup():
    response = None
    i = 0
    while response is None and i < 10:
        try:
            print("Waiting for server to warm up...", flush=True)
            response = user1["session"].get(url, timeout=0.1)
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

from .tests_01_user_crud import *
from .tests_02_user_properties import *
from .tests_03_lists import *
from .tests_04_actions import *
from .tests_05_tags import *
from .tests_06_populate import *
from .tests_07_pictures import *
from .tests_08_search import *
from .tests_09_messages import *
from .tests_10_notifications import *
from .tests_11_socketio import *
from .tests_99_delete import *
