import json
from flask import current_app as app
from flask import render_template, request, redirect, url_for, session, flash, make_response

from . import db
from .models import User
from .test_routes import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        if name is not None and name is not "":
            session["user"] = name
            #if cookies accepted:
            session.permanent = True

            found = User.query.filter_by(name=name).first()
            if found:
                session["email"] = found.email
            else:
                user = User(name, "")
                db.session.add(user)
                db.session.commit()


            flash(f"Welcome {name}")
            return redirect(url_for("profile"))
    if "user" in session:
        flash("Vous êtes déjà connecté !", "info")
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout/")
def logout():
    if "user" in session:
        flash(f"{session['user']} déconnecté", "info")
        session.pop("user", None)
        session.pop("email", None)
    return redirect(url_for("login"))

@app.route("/users/<user>/")
def users(user):
    return render_template("profile.html", user=user)

@app.route("/profile/", methods=["POST", "GET"])
def profile():
    if "user" in session:
        email = None
        if request.method == "POST":
            found = User.query.filter_by(name=session["user"]).first()
            if "email" in request.form and request.form["email"] is not "":
                found.email = request.form["email"]
                db.session.commit()
                email = found.email
                flash("Email enregistré", "info")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("profile_edit.html", user=session["user"], email=email)
    flash("Vous n'êtes pas connecté", "info")
    return redirect(url_for("login"))
