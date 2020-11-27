import os
from flask import Blueprint, session, request

from .. import socketio
from ..models.notification import Notification
from ..models.user import User
from ..utils import error, success
from ..utils.decorators import user_required, payload_required, jsonify_output, catcher

notifications = Blueprint("notifications", __name__)

@notifications.route("/notifications", methods=["GET"])
@jsonify_output
@user_required
def get_notifications(user):
    notifs_list = Notification.list(user.id)
    unread_count = sum(1 if x.unread else 0 for x in notifs_list)
    return {"notifications": [x.dict for x in notifs_list], "unread": unread_count}

@notifications.route("/notifications", methods=["PUT"])
@jsonify_output
@user_required
def read_notifications(user):
    Notification.read(user.id)
    return success()
