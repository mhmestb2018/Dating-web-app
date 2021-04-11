from .constants import url

def signup(user):
    payload = {
        'email': user["email"],
        'password': user["password"],
        'first_name': user["first_name"],
        'last_name': user["last_name"]
    }
    response = user["session"].post(f"{url}/signup", data=payload)
    # print(response.text)
    tmp = response.json()
    return response

def login(users):
    if type(users) is not list:
        users = [users]
    reponse = None
    for u in users:
        payload = {
            'email': u["email"],
            'password': u["password"],
            'remember_me': True,
            "lat": u["lat"],
            "lon": u["lon"]
        }
        response = u["session"].post(f"{url}/login", data=payload)
    # print(response)
    return response

def validate(user, validation_id):
    response = user["session"].post(f"{url}/validate/{validation_id}")
    # print(response)
    return response

def reset(users, picture=True):
    if type(users) is not list:
        users = [users]
    for u in users:
        login(u)
        delete(u)
        logout(u)
        create(u, checks=False, picture=picture)
        login(u)

def create(user, checks=True, picture=False):
    response = signup(user)
    print(response)
    if checks:
        assert response.status_code == 201
    data = response.json()
    if "validation_id" in response.json() or checks:
        response = validate(user, data["validation_id"])
        if checks:
            assert response.status_code == 200
        login(user)
        user['id'] = get_profile(user)["id"]
    if picture:
        update(user, {"pictures": ["/test123", "456"]})
    logout(user)

def delete(user):
    response = user["session"].delete(f"{url}/profile")
    # print(response)
    return response

def logout(users):
    if type(users) is not list:
        users = [users]
    for u in users:
        response = u["session"].post(f"{url}/logout")
    # print(response)
    return response

def clear(users):
    if type(users) is not list:
        users = [users]
    for u in users:
        login(u)
        delete(u)
        logout(u)


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
