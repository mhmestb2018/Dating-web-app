import time, os
from flask import current_app as app, render_template, request, session
from werkzeug.security import generate_password_hash
from flask_mail import Message
from mariadb import Error as Dberror

from . import db, host
from .matcha import mail
from .models.user import User
from .utils import error, success
from .utils.decorators import user_required, payload_required, jsonify_output, catcher

# https://www.restapitutorial.com/lessons/httpmethods.html

@app.route("/login", methods=["POST"])
@jsonify_output
@payload_required
@catcher
def login(payload):
    """
    Expects 'email' and 'password' in payload as well as
    a 'remember_me' boolean (expected at 'true' to be set) 
    """
    if "user" in session:
        return error("Vous êtes déjà connecté", 400)
    user = User.get_user(email=payload["email"])
    if not user:
        return error("Utilisateur introuvable", 404)
    if not user.check_password(payload["password"]):
        return error("Mot de passe incorrect")
    session["user"] = user.id
    if payload["remember_me"] == "true":
        session.permanent = True
    delattr(user, "password")
    return success(user.dict)

@app.route("/logout", methods=["POST"])
@jsonify_output
def logout():
    """
    reset the cookie
    """
    if "user" not in session:
        return error("Vous êtes déjà déconnecté", 400)
    session.pop("user", None)
    return success()

@app.route("/signup", methods=["POST"])
@jsonify_output
@payload_required
@catcher
def signup(payload):
    """
    Register a new user.
    Expects 'first_name', 'last_name', 'email' and 'password' in payload.
    This function will send a confirmation email if mail is configured.
    Assert success by fetching user in database.
    returns validation_id for mail validation
    """
    if "user" in session:
        return error("Vous êtes déjà connecté", 400)
    if User.get_user(email=payload["email"]) is not None:
        return error("L'utilisateur existe déjà", 409)
    hashed_password = generate_password_hash(payload["password"])

    new = User.create_user(payload["first_name"], payload["last_name"], payload["email"], hashed_password)

    validation_id = False
    if mail:
        validation_id = os.urandom(12).hex()
        link = f"{host}/validation/{validation_id}"
        msg = Message("Confirmation d'inscription", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[new.email])
        msg.html = render_template("validation_email.html", link=link)
        mail.send(msg)
    
    if not User.get_user(email=payload["email"]):
        return error("Failed to create user")
    return success({"validation_id": validation_id}, 201)

@app.route("/profile", methods=["PUT"])
@jsonify_output
@user_required
@payload_required
@catcher
def update_user(user, payload):
    """
    Use all provided fields in payload to update a user.
    This function first checks that every requested field is editable.
    It then update the user and returns updated profile data. 
    """
    user.update(payload)
    return success(user.dict)

@app.route("/profile", methods=["DELETE"])
@jsonify_output
@user_required
def delete_user(user):
    """
    Delete an user and return his public profile
    """
    user.delete()
    session.pop("user", None)
    return success(user.public)

@app.route("/profile", methods=["GET"])
@jsonify_output
@user_required
def profile(user):
    """
    Returns full profile data of the currently logged user
    """
    return success(user.dict)

@app.route("/user/<user_id>", methods=["GET"])
@jsonify_output
@user_required
def user_profile(user_id, user):
    """
    Returns public profile data of requested user_id
    """
    found = User.get_user(user_id=user_id)
    if not found:
        return error("Utilisateur introuvable", 404)
    return success(found.public)


@app.route("/user/<user_id>", methods=["POST"])
@jsonify_output
@user_required
@payload_required
def like_user(user_id, user, payload):
    """
    Likes and matches
    """
    if "block" in payload:
        if payload["block"]:
            user.block(user_id)  ##### Left to write user.block
        else:
            user.unblock(user_id)  ##### Left to write user.unblock
        return success()
    elif "like" in payload:
        match = False
        if payload["like"]:
            match = user.like(user_id)  ##### Left to write user.like
        else:
            user.dislike(user_id)  ##### Left to write user.dislike
        return ({"match": match})
    return error("Aucune action demandée", 400)

@app.route("/users", methods=["GET"])
@jsonify_output
@user_required
@payload_required
def get_users(user_id, user, payload):
    """
    Likes and matches
    """
    if "like" in payload:
        match = False
        if payload["like"]:
            match = user.like(user_id)  ##### Left to write user.like
        else:
            user.dislike(user_id)  ##### Left to write user.dislike
    return ({"match": match})
