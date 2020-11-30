import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report, reset)

def test_socketio_messages():
    reset(user1)
    reset(user2)

def test_socketio_notifications():
    reset(user1)
    reset(user2)