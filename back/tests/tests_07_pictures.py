import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report, reset)

def test_upload():
    reset(user1, picture=False)
    login(user1)
    response = user1["session"].post(f"{url}/add_picture", files={'file': open('./medium_pcachin.jpg', 'rb')})
    assert response.status_code == 201
    print("201 OK", flush=True)
    profile = response.json()
    pic_true_url = profile["pictures"][-1]
    assert os.path.exists(os.path.join("/data", pic_true_url.split('/')[-1]))
    pic_url = f"http://app:5000/pictures/{pic_true_url.split('/')[-1]}"
    response = user1["session"].get(pic_url)
    assert response.status_code == 200
    print("200 OK", flush=True)
    assert pic_true_url in profile["pictures"]
    print("In profile OK", pic_true_url, flush=True)
    response = user1["session"].delete(pic_url)
    assert response.status_code == 200
    print("200 OK delete", flush=True)
    profile = response.json()
    assert pic_true_url not in profile["pictures"]
    print("Not in profile OK", flush=True)
    assert not os.path.exists(os.path.join("/data", pic_true_url.split('/')[-1]))
    print("Picture deleted OK", flush=True)
    logout(user1)
