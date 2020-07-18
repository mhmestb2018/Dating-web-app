#! /usr/bin/env python3

from flask import Flask


app = Flask(__name__)


@app.route("/")
def Coucou():
    return "Coucou moi"

@app.route("/route")
def CoucouRoute():
    return "Encore moi"


if __name__ == "__main__":
    app.run() 