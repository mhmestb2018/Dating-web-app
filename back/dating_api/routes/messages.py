import os
from flask import Blueprint, session, request

from .. import socketio
from ..models.user import User
from ..utils import error, success
from ..utils.decorators import user_required, payload_required, jsonify_output, catcher

messages = Blueprint("messages", __name__)

@messages.route("/login", methods=["POST"])
@jsonify_output
@payload_required
@catcher
def login(payload):
    pass
