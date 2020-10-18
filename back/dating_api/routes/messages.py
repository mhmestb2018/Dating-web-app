import os
from flask import Blueprint, session, request

from .. import socketio
from ..models.message import Message
from ..models.user import User
from ..utils import error, success
from ..utils.decorators import user_required, payload_required, jsonify_output, catcher

messages = Blueprint("messages", __name__)

@messages.route("/conversations", methods=["GET"])
@jsonify_output
@user_required
def get_conversations(user):
    return {"users": user.conversations}

@messages.route("/messages", methods=["POST"])
@jsonify_output
@payload_required
@user_required
@catcher
def get_messages(user, payload):
    return {'messages': [m.dict for m in Message.list(user.id, payload["user"])]}

@messages.route("/new_message", methods=["POST"])
@jsonify_output
@payload_required
@user_required
@catcher
def send_message(user, payload):
    msg = Message(user.id, payload["user"], payload["content"])
    return success({"message": msg.dict}, 201)
