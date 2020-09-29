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
    return {"users": [x for x in user.list_users()]}

@users_list.route("/matches", methods=["GET"])
@jsonify_output
@validated_required
def get_matches(user):
    """
    List matches as an array of full json encoded profiles
    """
    return {"matches": [x for x in user.matchlist]}

@users_list.route("/liked_by", methods=["GET"])
@jsonify_output
@validated_required
def get_liked_by(user):
    """
    List matches as an array of full json encoded profiles
    """
    return {"users": [x for x in user.liked_by_list]}
