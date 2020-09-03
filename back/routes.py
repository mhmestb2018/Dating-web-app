import json, time, os
from flask import current_app as app
from flask import render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from mariadb import Error as Dberror

from . import db, host
from .matcha import mail
from .models import User
from .utils import user_required, error, success

############ DUMMIES #########################


############ NEW CODE (API) ########################

@app.route("/login/", methods=["POST"])
def login():
    if "user" in session:
        return error("Vous êtes déjà connecté")
    user = User.get_user(email=request.form["email"])
    if not user:
        return error("Utilisateur introuvable")
    if not check_password_hash(user.password, request.form["password"]):
        return error("Mot de passe incorrect")
    # session["token"] = generate_token(user)
    session["user"] = user.id
    if request.form["remember_me"] == "true":
        session.permanent = True
    # setattr(user, "token", session["token"])
    delattr(user, "password")
    return user.to_JSON()

@app.route("/logout/", methods=["POST", "GET"])
def logout():
    if "user" not in session:
        return error("Vous êtes déjà déconnecté")
    session.pop("user", None)
    # session.pop("token", None)
    return success()

@app.route("/signin/", methods=["POST"])
def signin():
    if "user" in session:
        return error("Vous êtes déjà connecté")
    hashed_password = generate_password_hash(request.form["password"])
    # try:
    new = User.create_user(request.form["first_name"], request.form["last_name"], request.form["email"], hashed_password)
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})

    validation_id = os.urandom(12).hex()
    link = f"{host}/validation/{validation_id}"
    msg = Message("Confirmation d'inscription", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[new.email])
    msg.html = render_template("validation_email.html", link=link)
    mail.send(msg)
    
    return success()

@app.route("/my_profile/", methods=["POST"])
@user_required
def my_profile(user):
    return user.to_JSON()

@app.route("/user/<user_id>/", methods=["POST"])
@user_required
def user_profile(user_id, user):
    found = User.get_user(user_id=user_id)
    if not found:
        return error("Utilisateur introuvable")
    return json.dumps(found.public)
