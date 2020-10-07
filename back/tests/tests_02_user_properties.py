import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)


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
