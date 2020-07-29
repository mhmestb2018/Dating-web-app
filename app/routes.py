import json
from flask import current_app as app
from flask import render_template, request, redirect, url_for, session, flash, make_response

from . import db
from .models import User
from .test_routes import *

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

@app.route("/login/", methods=["POST", "GET"])
def login():
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

@app.route("/logout/")
def logout():
    if "user" in session:
        flash(f"{session['name']} déconnecté", "info")
        session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/users/<user>/")
def users(user):
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
