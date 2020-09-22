import os
from flask import Blueprint, render_template, session
from werkzeug.security import generate_password_hash
from flask_mail import Message

from .. import public_host, mail
from ..models.user import User
from ..utils import error, success, Validator
from ..utils.decorators import user_required, payload_required, jsonify_output, catcher

reset_password = Blueprint("reset_password", __name__, url_prefix="/reset")

@reset_password.route("/", methods=["POST"])
@payload_required
@jsonify_output
@catcher
def query_reset(payload):
    """
    Expects 'email' in payload
    Sends an email with a reset link valid for 1 hour
    When email is not configurated, changes the password
    with the 'new_password' provided
    """
    if "user" in session:
        return error("Vous êtes déjà connecté", 400)
    user = User.get_user(email=payload["email"])
    if not user:
        return error("Utilisateur introuvable", 404)
    if mail:
        print(f"Sending validation email to {payload['email']}", flush=True)
        reset_id = os.urandom(12).hex()
        link = f"{public_host}/reset/{user.id}/{reset_id}"
        msg = Message("Demande de changement de mot de passe", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[user.email])
        user.save_reset_id(reset_id)
        msg.html = render_template("reset_password_email.html", link=link)
        mail.send(msg)
    else:
        if "new_password" in payload:
            user.update({"password": Validator.password(payload["new_password"])}, force=True)
            print(f"Password of {user.email} validated automatically", flush=True)
        else:
            return error("Missing 'new_password' in payload", 400)
        user.validate()

    return success()

@reset_password.route("/<user_id>/<reset_id>", methods=["POST"])
@jsonify_output
@payload_required
@catcher
def reset_link(user_id, reset_id, payload):
    """
    Expects 'new_password' in payload
    """
    if "user" in session:
        return error("Vous êtes déjà connecté", 400)
    user = User.get_user(user_id=user_id)
    if not user:
        return error("Utilisateur introuvable", 404)
    if not user.reset_id != reset_id:
        return error("Clé secrète invalide", 400)
    if "new_password" in payload:
        user.update({"password": Validator.password(payload["new_password"])}, force=True)
        print(f"Password of {user.email} validated manually", flush=True)
    else:
        return error("Missing 'new_password' in payload", 400)
    user.validate()

    return success()