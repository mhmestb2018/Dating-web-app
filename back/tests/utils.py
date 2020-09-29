import json

from constants import url, user1, user2

def signup(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = user["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    tmp = json.loads(response.text)
    return response

def login(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'remember_me': True
    }
    response = user["session"].post(f"{url}/login", data=payload)
    print(response)
    return response

def validate(user, validation_id):
    response = user["session"].post(f"{url}/validate/{validation_id}")
    print(response)
    return response

def create(user, checks=True):
    response = signup(user)
    assert response.status_code == 201
    data = json.loads(response.text)
    response = validate(user, data["validation_id"])
    assert response.status_code == 200

def delete(user):
    response = user["session"].delete(f"{url}/profile")
    print(response)
    return response

def logout(user):
    response = user["session"].post(f"{url}/logout")
    print(response)
    return response


def update(user, data):
    response = user["session"].put(f"{url}/profile", data=data)
    return response

def get_profile(user):
    response = user["session"].get(f"{url}/profile")
    return json.loads(response.text)
