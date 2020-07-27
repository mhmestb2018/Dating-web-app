#! /usr/bin/env python3

import json
from flask import current_app as app
from flask import render_template, request, redirect, url_for, session, flash

# configuration used to connect to MariaDB


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        if user is not None and user is not "":
            session["user"] = user
            #if cookies accepted:
            session.permanent = True
            flash(f"Welcome {user}")
            return redirect(url_for("profile"))
    if "user" in session:
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("Vous êtes déconnecté", "info")
    return redirect(url_for("login"))


@app.route("/uri/")
def CoucouRoute():
    return app.config['SQLALCHEMY_DATABASE_URI']

def profile_page(user):
    return render_template("base.html", title=f"{user}", body=f"<p>Bonjour {user}</p>")

@app.route("/users/<user>/")
def users(user):
    return profile_page(user)

@app.route("/profile/")
def profile():
    if "user" in session:
        return profile_page(session["user"])
    return redirect(url_for("index"))


@app.route('/testadd/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False
        )
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    return make_response(f"{new_user} successfully created!")

@app.route("/dbtest")
def dbtest():
    import os
    import mariadb
    config = {
        'host': 'db',
        'port': 3306,
        'user': os.environ['MYSQL_USER'],
        'password': os.environ['MYSQL_PASSWORD'],
        'database': 'matcha',
    }

    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute("select * from users")
    # get headers
    header = [item[0] for item in cur.description]
    # get all matches
    res = cur.fetchall()
    # jsonify
    json_data = []
    for item in res:
        json_data.append(dict(zip(header, item)))
    # DUMP !
    return json.dumps(json_data)
