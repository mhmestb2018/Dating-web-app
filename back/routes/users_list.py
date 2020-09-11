from flask import Blueprint, request

from ..utils.decorators import (jsonify_output, validated_required)

users_list = Blueprint("users_list", __name__)

@users_list.route("/users", methods=["GET"])
@jsonify_output
@validated_required
def get_users(user):
    """
    List unmatched users
    """
    payload = request.get_json()
    return [x.public_as(user) for x in user.list_users()]

@users_list.route("/matches", methods=["GET"])
@jsonify_output
@validated_required
def get_matches(user):
    """
    List matches as an array of full json encoded profiles
    """
    return [x.public_as(user) for x in user.matchlist]
