import types, datetime
from flask import session, request, jsonify, make_response
from flask_cors import cross_origin

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
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),flush=True)
        found.update({"last_seen": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}, force=True)
        return fun(*args, **kwargs, user=found)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    wrapper.__name__ = fun.__name__
    return wrapper

def validated_required(fun):
    """
    User_required decorator:
        1. Check for authentification cookie
        2. Fetch user in db
        3. Prepend the User to the function call
    """

    @user_required
    def wrapper(*args, **kwargs):
        if kwargs["user"].validated is not 1:
            return error("Votre email n'a pas été validé", 403)
        return fun(*args, **kwargs)

    if type(fun) is not types.FunctionType:
        raise ValueError()
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
        print("Payload:", payload, flush=True)
        if not payload or len(payload) is 0:
            return error("This endpoint requires a payload", 400)
        return fun(*args, **kwargs, payload=payload)

    if type(fun) is not types.FunctionType:
        raise ValueError()
    wrapper.__name__ = fun.__name__
    return wrapper

def jsonify_output(fun):
    """
    jsonify_output decorator:
        1. jsonify the return value of the function
    """

    @cross_origin()
    def wrapper(*args, **kwargs):
        ret = fun(*args, **kwargs)
        code = 200
        if isinstance(ret, tuple):
            code = ret[1]
            ret = ret[0]
        return jsonify(ret), code
        

    if type(fun) is not types.FunctionType:
        raise ValueError()
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
    wrapper.__name__ = fun.__name__
    return wrapper