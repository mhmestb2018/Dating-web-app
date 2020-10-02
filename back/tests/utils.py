from constants import url

def signup(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = user["session"].post(f"{url}/signup", data=payload)
    print(response.text)
    tmp = response.json()
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
    data = response.json()
    response = validate(user, data["validation_id"])
    assert response.status_code == 200
    login(user)
    user['id'] = get_profile(user)["id"]
    logout(user)

def delete(user):
    response = user["session"].delete(f"{url}/profile")
    print(response)
    return response

def logout(user):
    response = user["session"].post(f"{url}/logout")
    print(response)
    return response


def update(user, data):
    response = user["session"].put(f"{url}/profile", json=data)
    return response

def get_profile(user):
    response = user["session"].get(f"{url}/profile")
    return response.json()

def get_public_profile(user_from, user_to):
    response = user_from["session"].get(f"{url}/users/{user_to['id']}")
    return response.json()

def like(user_from, user_to):
    return user_from["session"].post(f"{url}/users/{user_to['id']}", json={'like': True})

def report(user_from, user_to):
    return user_from["session"].post(f"{url}/users/{user_to['id']}", json={'report': True})

def unlike(user_from, user_to):
    return user_from["session"].post(f"{url}/users/{user_to['id']}", json={'like': False})

def block(user_from, user_to):
    return user_from["session"].post(f"{url}/users/{user_to['id']}", json={'block': True})

def unblock(user_from, user_to):
    return user_from["session"].post(f"{url}/users/{user_to['id']}", json={'block': False})

def report(user_from, user_to):
    return user_from["session"].post(f"{url}/users/{user_to['id']}", json={'report': True})
