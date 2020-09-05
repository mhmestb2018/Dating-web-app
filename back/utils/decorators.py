import types
from flask import session, request

from ..models.user import User
from .misc import error

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

def payload_required(fun):
    """
    Payload can either be form data or json payload
    Payload_required decorator:
        1. Check if form data provided
        2. Otherwise load JSON data
        3. If payload not empty, add the payload to function parameters
    """

    def wrapper(*args, **kwargs):
        payload = request.form
        if len(payload) is 0:
            payload = request.get_json()
        
        if len(payload) is 0:
            return error("This endpoint requires a payload")
        return fun(*args, **kwargs, payload=payload)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    # To carry the name over and be able to register more than one route with this decorator
    wrapper.__name__ = fun.__name__
    return wrapper