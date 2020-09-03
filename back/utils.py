import hashlib, time, types, json
from flask import session

from .models.user import User

def error(msg):
    return json.dumps({"error": msg})

def success():
    return json.dumps({"pcachin": True})

# def generate_token(user):
#     m = hashlib.sha256()
#     m.update(f"{user.password}{user.email}{time.time()}".encode('utf-8'))
#     return str(m.digest())

def user_required(fun):
    """
    User_required decorator:
        1. Check for authentification cookie
        2. Fetch user in db
        3. Prepend the User to the function call
    """

    def wrapper(*args, **kwargs):
        if not "user" in session:
            return error("Vous n'êtes pas connecté")
        found = User.get_user(user_id=session["user"])
        if not found:
            return error("Votre compte a été supprimé")
        delattr(found, "password")
        return fun(*args, **kwargs, user=found)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    # To carry the name over and be able to register more than one route with this decorator
    wrapper.__name__ = fun.__name__
    return wrapper