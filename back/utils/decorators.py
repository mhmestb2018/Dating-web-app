import types
from flask import session, request, jsonify, make_response

from ..models.user import User
from .misc import error
from .errors import InvalidData

def user_required(fun):
    """
    User_required decorator:
        1. Check for authentification cookie
        2. Fetch user in db
        3. Prepend the User to the function call
    """

    def wrapper(*args, **kwargs):
        if not "user" in session:
            return error("Vous n'êtes pas connecté", 403)
        found = User.get_user(user_id=session["user"])
        if not found:
            return error("Votre compte a été supprimé", 403)
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
        if not payload or len(payload) is 0:
            payload = request.get_json()
        
        if not payload or len(payload) is 0:
            return error("This endpoint requires a payload", 400)
        return fun(*args, **kwargs, payload=payload)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    # To carry the name over and be able to register more than one route with this decorator
    wrapper.__name__ = fun.__name__
    return wrapper

def jsonify_output(fun):
    """
    jsonify_output decorator:
        1. jsonify the return value of the function
    """

    def wrapper(*args, **kwargs):
        ret = fun(*args, **kwargs)
        code = 200
        if isinstance(ret, tuple):
            code = ret[1]
            ret = ret[0]
        return jsonify(ret), code
        

    if type(fun) is not types.FunctionType:
        raise ValueError()
    # To carry the name over and be able to register more than one route with this decorator
    wrapper.__name__ = fun.__name__
    return wrapper

def catcher(fun):
    """
    catcher decorator:
        1. catches all custom exceptions
    """

    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except InvalidData as e:
            return error(f"{e}", 400)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    # To carry the name over and be able to register more than one route with this decorator
    wrapper.__name__ = fun.__name__
    return wrapper