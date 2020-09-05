import time, os
from flask import current_app as app, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from flask_mail import Message
from mariadb import Error as Dberror

from . import db, host
from .matcha import mail
from .models.user import User
from .utils.decorators import user_required, payload_required, jsonify_output
from .utils import error, success

############ NEW CODE (API) ########################

@app.route("/login", methods=["POST"])
@jsonify_output
@payload_required
def login(payload):
    """
    Expects 'email' and 'password' in payload as well as
    a 'remember_me' boolean (expected at 'true' to be set) 
    """
    if "user" in session:
        return error("Vous êtes déjà connecté")
    user = User.get_user(email=payload["email"])
    if not user:
        return error("Utilisateur introuvable")
    if not user.check_password(payload["password"]):
        return error("Mot de passe incorrect")
    session["user"] = user.id
    if payload["remember_me"] == "true":
        session.permanent = True
    delattr(user, "password")
    return user.dict

@app.route("/logout", methods=["POST", "GET"])
@jsonify_output
def logout():
    """
    reset the cookie
    """
    if "user" not in session:
        return error("Vous êtes déjà déconnecté")
    session.pop("user", None)
    return success()

@app.route("/signin", methods=["POST"])
@jsonify_output
@payload_required
def signin(payload):
    """
    Register a new user.
    Expects 'first_name', 'last_name', 'email' and 'password' in payload.
    This function will send a confirmation email if mail is configured.
    Assert success by fetching user in database.
    returns validation_id for mail validation
    """
    if "user" in session:
        return error("Vous êtes déjà connecté")
    if User.get_user(email=payload["email"]) is not None:
        return error("L'utilisateur existe déjà")
    hashed_password = generate_password_hash(payload["password"])
    # try:
    new = User.create_user(payload["first_name"], payload["last_name"], payload["email"], hashed_password)
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})

    validation_id = False
    if mail:
        validation_id = os.urandom(12).hex()
        link = f"{host}/validation/{validation_id}"
        msg = Message("Confirmation d'inscription", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[new.email])
        msg.html = render_template("validation_email.html", link=link)
        mail.send(msg)
    
    found = User.get_user(email=payload["email"])
    if not found:
        return error("Failed to create user")
    print(found, flush=True)
    return {"validation_id": validation_id}

@app.route("/update", methods=["POST"])
@jsonify_output
@user_required
@payload_required
def update_user(user, payload):
    """
    Use all provided fields in payload to update a user.
    This function first checks that every requested field is editable.
    It then update the user and returns updated profile data. 
    """
    # try:
    user.update(payload)
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})
    return user.dict

@app.route("/delete", methods=["POST"])
@jsonify_output
@user_required
def delete_user(user):
    """
    Delete an user and redirect to lougout endpoint
    """
    # try:
    user.delete()
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})
    session.pop("user", None)
    return success()

@app.route("/my_profile", methods=["POST"])
@jsonify_output
@user_required
def my_profile(user):
    """
    Returns full profile data of the currently logged user
    """
    return user.dict

@app.route("/user/<user_id>", methods=["POST"])
@jsonify_output
@user_required
def user_profile(user_id, user):
    """
    Returns public profile data of requested user_id
    """
    found = User.get_user(user_id=user_id)
    if not found:
        return error("Utilisateur introuvable")
    return found.public
