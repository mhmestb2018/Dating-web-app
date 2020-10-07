import requests, time, datetime, random, os
from .constants import url, user1, user2
from .utils import (signup, login, validate, create, update, delete,
                    logout, get_profile, get_public_profile, like, unlike, block, unblock,
                    report)

users = []
def test_populate():
    def create_user(user):
        orientations = ["hetero", "bi", "asexual", "homo"]
        print(user["location"]["street"])
        user = {
            "bio": "J'aime manger des pommes",
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "orientation": orientations[random.randint(0, len(orientations) - 1)],
            "pictures": [user["picture"]["large"], user["picture"]["medium"], user["picture"]["thumbnail"]],
            "sex": user["gender"],
            "lon": float(user["location"]["coordinates"]["longitude"]),
            "lat": float(user["location"]["coordinates"]["longitude"]),
            "age": user["dob"]["age"],
            "tags": list(filter(None, user["location"]["street"]["name"].split(" "))),
            "email": user["email"],
            "password": user["login"]["password"],
            "session": requests.Session()
        }
        print(user)
        response = signup(user)
        assert response.status_code == 201
        response = validate(user, response.json()["validation_id"])
        assert response.status_code == 200
        login(user)
        user['id'] = get_profile(user)["id"]
        response = update(user, {
            "bio": user["bio"],
            "orientation": user["orientation"],
            "pictures": user["pictures"],
            "sex": user["sex"],
            "lon": user["lon"],
            "lat": user["lat"],
            "age": user["age"],
            "tags": user["tags"],})
        print(response.json())
        assert response.status_code == 200
        users.append(user)
        return user
    data = []
    tries = 0

    create(user1, checks=False)
    login(user1)
    if len(user1["session"].get(f"{url}/users").json()["users"]) < 10:
        while len(data) == 0 and tries < 2:
            try:
                tries += 1
                data = requests.get('https://randomuser.me/api/?format=json?nat=fr?page=1&results=23&seed=pcachin').json()
            except:
                print("error while fetching random users, retrying...")
                time.sleep(1)
        for u in data["results"]:
            create_user(u)

def test_clean_populate():
    if "POPULATE_DB" not in os.environ or os.environ["POPULATE_DB"] not in ["True", "true"]:
        for u in users:
            login(u)
            delete(u)
    assert 1 == 1
    delete(user1)
