import os
from flask import Blueprint, render_template, session
from werkzeug.security import generate_password_hash
from flask_mail import Message

from .. import public_host, mail
from ..models.user import User
from ..utils import error, success, Validator
from ..utils.decorators import payload_required, jsonify_output, catcher

reset_password = Blueprint("reset_password", __name__, url_prefix="/reset")

@reset_password.route("", methods=["POST"]) # com
@payload_required
@jsonify_output
@catcher
def query_reset(payload):
    """
    Expects 'email' in payload
    Sends an email with a reset link valid for 1 hour
    When email is not configurated, return the reset_id
    used for link generation
    """
    if "user" in session:
        return error("Vous êtes déjà connecté", 400)
    user = User.get_user(email=payload["email"])
    if not user:
        return error("Utilisateur introuvable", 404)
    reset_id = os.urandom(12).hex()
    user.save_reset_id(reset_id)
    if mail:
        print(f"Sending validation email to {payload['email']}", flush=True)
        link = f"{public_host}/reset/{user.id}/{reset_id}"
        msg = Message("Demande de changement de mot de passe", sender=("Matcha Headquarters", os.environ['FLASK_GMAIL']), recipients=[user.email])
        msg.html = render_template("reset_password_email.html", link=link)
        mail.send(msg)
    else:
        return success({'reset_id': reset_id})
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
        passwd = Validator.password(payload["new_password"])
        user.update({"password": generate_password_hash(passwd)}, force=True)
        print(f"Password of {user.email} validated manually", flush=True)
    else:
        return error("Missing 'new_password' in payload", 400)
    user.clear_resets()

    return success()
    