from flask import Blueprint

from ..utils import success
from ..utils.decorators import jsonify_output

healthcheck = Blueprint('healthcheck', __name__)

@healthcheck.route("/", methods=["POST", "GET"])
@jsonify_output
def is_alive(user_id, user, payload):
    return success()
