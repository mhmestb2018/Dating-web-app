from flask import Blueprint

from ..models.user import User
from ..utils import success
from ..utils.decorators import user_required, jsonify_output

debug = Blueprint('debug', __name__, url_prefix='/debug')

@debug.route("/beblocked1", methods=["GET"])
@jsonify_output
@user_required
def beblocked(user):
    """
    Block the logged user with user 1
    """
    User.get_user(user_id=1).block(user)
    return success()

@debug.route("/beliked1", methods=["GET"])
@jsonify_output
@user_required
def beliked(user):
    """
    Likes the logged user with user 1
    """
    User.get_user(user_id=1).like(user)
    return success()
