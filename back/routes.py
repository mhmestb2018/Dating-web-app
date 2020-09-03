import time, os
from flask import current_app as app, jsonify
from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from mariadb import Error as Dberror

from . import db, host
from .matcha import mail
from .models.user import User
from .utils import user_required, error, success

############ NEW CODE (API) ########################

@app.route("/login", methods=["POST"])
def login():
    """
    Expects an 'email' and 'password' form field as well as
    a 'remember_me' boolean (expected at 'true' to be set) 
    """
    if "user" in session:
        return error("Vous êtes déjà connecté")
    user = User.get_user(email=request.form["email"])
    if not user:
        return error("Utilisateur introuvable")
    if not check_password_hash(user.password, request.form["password"]):
        return error("Mot de passe incorrect")
    session["user"] = user.id
    if request.form["remember_me"] == "true":
        session.permanent = True
    delattr(user, "password")
    return user.jsonify()

@app.route("/logout", methods=["POST", "GET"])
def logout():
    """
    reset the cookie
    """
    if "user" not in session:
        return error("Vous êtes déjà déconnecté")
    session.pop("user", None)
    return success()

@app.route("/signin", methods=["POST"])
def signin():
    """
    Register a new user.
    Expects 'first_name', 'last_name', 'email' and 'password' form fields.
    This function will send a confirmation email if mail is configured.
    Assert success by fetching user in database.
    returns profile data
    """
    if "user" in session:
        return error("Vous êtes déjà connecté")
    hashed_password = generate_password_hash(request.form["password"])
    # try:
    new = User.create_user(request.form["first_name"], request.form["last_name"], request.form["email"], hashed_password)
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})

    if mail:
        validation_id = os.urandom(12).hex()
        link = f"{host}/validation/{validation_id}"
        msg = Message("Confirmation d'inscription", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[new.email])
        msg.html = render_template("validation_email.html", link=link)
        mail.send(msg)
    
    found = User.get_user(email=request.form["email"])
    if not found:
        return error("Failed to create user")
    print(found, flush=True)
    return success()

@app.route("/update", methods=["POST"])
@user_required
def update_user(user):
    """
    Use all profided form fields to update a user.
    This function first checks that every requested field is editable.
    It then update the user and returns updated profile data. 
    """
    # try:
    user.update(request.form)
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})
    return user.jsonify()

@app.route("/delete", methods=["POST"])
@user_required
def delete_user(user):
    """
    Delete an user and redirect to lougout endpoint
    """
    # try:
    user.delete()
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})
    return redirect(url_for("logout"))

@app.route("/my_profile", methods=["POST"])
@user_required
def my_profile(user):
    """
    Returns full profile data of the currently logged user
    """
    return user.jsonify()

@app.route("/user/<user_id>", methods=["POST"])
@user_required
def user_profile(user_id, user):
    """
    Returns public profile data of requested user_id
    """
    found = User.get_user(user_id=user_id)
    if not found:
        return error("Utilisateur introuvable")
    return jsonify(found.public)
