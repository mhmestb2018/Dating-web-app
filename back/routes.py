import json, time, os
from flask import current_app as app
from flask import render_template, request, redirect, url_for, session, flash, make_response
from flask_mail import Message
from mariadb import Error as Dberror

from . import db, host
from .matcha import mail
from .models import User
from .utils import salt, generate_token

############ DUMMIES #########################


############ NEW CODE (API) ########################

@app.route("/login/", methods=["POST"])
def login():
    if "user" in session:
        return json.dumps({"error": "Vous êtes déjà connecté"})
    email = request.form["email"]
    found = User.get_user(email=email)
    if found:
        if salt(request.form["password"]) == found.password:
            session["token"] = generate_token(found.email, found.password)
            session["user"] = found.id
            session["first_name"] = found.first_name
            session["last_name"] = found.last_name
            session["email"] = found.email
            #session["picture_url"] = found.picture_url
            if request.form["remember_me"] == "true":
                session.permanent = True
            setattr(found, "token", session["token"])
            delattr(found, "password")
            return found.to_JSON()
        else:
            return json.dumps({"error": "Mot de passe incorrect"})
    return json.dumps({"error": "Utilisateur introuvable"})

@app.route("/logout/", methods=["POST", "GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("token", None)
        session.pop("first_name", None)
        session.pop("last_name", None)
        session.pop("email", None)
        session.pop("picture_url", None)
        # Left to pop stuff (to check and recheck)
        return json.dumps({"pcachin": True})
    return json.dumps({"error": "Vous n'êtes pas connecté"})

@app.route("/signin/", methods=["POST"])
def signin():
    if "user" in session:
        return json.dumps({"error": "Vous êtes déjà connecté"})
    hashed_password = salt(request.form["password"])
    # try:
    new = User.create_user(request.form["first_name"], request.form["last_name"], request.form["email"], hashed_password)
    # except Dberror as e:
        # return json.dumps({"error": f"While creating user: {e}"})

    validation_id = os.urandom(12).hex()
    link = f"{host}/validation/{validation_id}"
    msg = Message("Confirmation d'inscription", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[new.email])
    msg.html = render_template("validation_email.html", link=link)
    mail.send(msg)
    
    return json.dumps({"pcachin": True})

@app.route("/my_profile/", methods=["POST"])
def my_profile():
    if not "email" in session:
        return json.dumps({"error": "Vous n'êtes pas connecté"})
    found = User.get_user(email=session["email"])
    delattr(found, "password")
    return found.to_JSON()

@app.route("/user/<user_id>/", methods=["POST"])
def user_profile(user_id):
    if not "email" in session:
        return json.dumps({"error": "Vous n'êtes pas connecté"})
    found = User.get_user(user_id=user_id)
    return json.dumps(found.public)

############ OLD CODE (UI) ########################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin/", methods=["POST", "GET"])
def signin_page():
    if "user" in session:
        flash(f"Vous êtes déjà connecté !", "info")
        return redirect(url_for("profile"))
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        # password = request.form["password"]
        if User.query.filter_by(email=email).first():
            flash("Vous avez déjà un compte")
            return redirect(url_for("login"))
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        flash(f"Compte créé, merci de vous connecter")
        return redirect(url_for("login"))

    return render_template("signin.html")

@app.route("/login_page/", methods=["POST", "GET"])
def login_page():
    if "user" in session:
        flash("Vous êtes déjà connecté !", "info")
        return redirect(url_for("profile"))
    if request.method == "POST":
        email = request.form["email"]
        found = User.query.filter_by(email=email).first()
        if found:
            session["user"] = found.id
            session["name"] = found.name
            session["email"] = found.email
            # session["password"] = found.password
            session["user_picture"] = found.picture_url
        
            session.permanent = True
        else:
            flash("Ce compte n'existe pas")
            return render_template("login.html")
        # Left to check password

        flash(f"Bienvenue {found.name}")
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout_page/")
def logout_page():
    if "user" in session:
        flash(f"{session['name']} déconnecté", "info")
        logout()
    return redirect(url_for("login"))

@app.route("/users_page/<user>/")
def users_page(user):
    return render_template("profile.html", name=user)

@app.route("/profile/", methods=["POST", "GET"])
def profile():
    if "user" in session:
        if request.method == "POST":
            found = User.query.filter_by(id=session["user"]).first()
            if "email" in request.form:
                found.email = request.form["email"]
                flash(f"Email {request.form['email']} enregistré", "info")
            db.session.commit()
        return render_template("profile_edit.html", name=session["name"], email=session["email"])
    flash("Vous n'êtes pas connecté", "info")
    return redirect(url_for("login"))
