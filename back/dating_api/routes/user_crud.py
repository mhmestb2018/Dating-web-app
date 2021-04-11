import os
from flask import Blueprint, render_template, session
from werkzeug.security import generate_password_hash
from flask_mail import Message

from .. import public_host, mail
from ..models.user import User
from ..utils import error, success
from ..utils.decorators import user_required, payload_required, jsonify_output, catcher

user_crud = Blueprint("user_crud", __name__)

@user_crud.route("/login", methods=["POST"])
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
        return error("Mot de passe incorrect", 400)
    if not "lat" in payload or not "lon" in payload:
        return error("Position manquante", 400)
    session["user"] = user.id
    user.update({"lat": payload["lat"], "lon": payload["lon"]})
    if payload["remember_me"] == True:
        session.permanent = True
    delattr(user, "password")
    return success(user.dict)

@user_crud.route("/logout", methods=["POST"])
@jsonify_output
def logout():
    """
    reset the cookie
    """
    if "user" not in session:
        return error("Vous êtes déjà déconnecté", 400)
    session.pop("user", None)
    return success()

@user_crud.route("/signup", methods=["POST"])
@jsonify_output
@payload_required
# @catcher
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
    if not "email" in payload or not "first_name" in payload or not "last_name" in payload or not "password" in payload:
        return error("Saisie incomplète", 400)
    try:
        user_exists = User.get_user(email=payload["email"]) is not None
    except Exception as e:
        return error(f"{e}", 400)

    if user_exists:
        return error("L'utilisateur existe déjà", 409)
    if len(payload["password"]) < 4: ######## Was for randomuser.me, TO REMOVE / REPLACE ###############################################################
        return error("Mot de passe trop court", 400)

    hashed_password = generate_password_hash(payload["password"])

    validation_id = os.urandom(12).hex()

    try:
        user = User.create_user(payload["first_name"], payload["last_name"], payload["email"], hashed_password, validation_id)
    except Exception as e:
        return error(f"Failed to create user: {e}", 400)

    if mail:
        print(f"Sending validation email to {payload['email']}", flush=True)
        link = f"{public_host}/validate/{validation_id}"
        msg = Message("Confirmation d'inscription", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[user.email])
        msg.html = render_template("validation_email.html", link=link)
        mail.send(msg)
    else:
        return success({"validation_id": validation_id}, 201)
    if not User.get_user(email=payload["email"]):
        return error("Failed to create user")
    return success(status=201)

@user_crud.route("/profile", methods=["PUT"])
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

@user_crud.route("/validate/<validation_id>", methods=["POST"])
@jsonify_output
@catcher
def validate_user(validation_id):
    """
    Validate an user given a validation_id
    """
    if User.validate(validation_id):
        return success()
    return error("Invalid validation link", 404)

@user_crud.route("/profile", methods=["DELETE"])
@jsonify_output
@user_required
def delete_user(user):
    """
    Delete an user and return his public profile
    """
    user.delete()
    session.pop("user", None)
    return success(user.public)

@user_crud.route("/profile", methods=["GET"])
@jsonify_output
@user_required
def profile(user):
    """
    Returns full profile data of the currently logged user
    """
    return success(user.dict)
