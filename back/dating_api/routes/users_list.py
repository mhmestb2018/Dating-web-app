from flask import Blueprint, request

from ..utils.decorators import (jsonify_output, validated_required, payload_required)

users_list = Blueprint("users_list", __name__)

@users_list.route("/users", methods=["POST"])
@jsonify_output
@validated_required
def get_users(user):
    """
    List users according to search parameters as an array of full json encoded profiles
    Possible search parameters:
    {
        "age": {
            "min": 18,
            "max": 99
        },
        "score": {
            "min": 0,
            "max": 100
        },
        "distance": 15,
        "tags": ["artist", "420"]
    }
    """
    payload = request.get_json()
    return {"users": user.search(payload)}

@users_list.route("/matches", methods=["GET"])
@jsonify_output
@validated_required
def get_matches(user):
    """
    List matches as an array of full json encoded profiles
    """
    return {"users": user.matchlist}

@users_list.route("/liked_by", methods=["GET"])
@jsonify_output
@validated_required
def get_liked_by(user):
    """
    List people liking you as an array of full json encoded profiles
    """
    return {"users": user.liked_by_list}

@users_list.route("/visits", methods=["GET"])
@jsonify_output
@validated_required
def get_visits(user):
    """
    List visits as an array of full json encoded profiles
    """
    return {"users": user.visits_list}

@users_list.route("/blocked", methods=["GET"])
@jsonify_output
@validated_required
def get_blocked(user):
    """
    List blocked users as an array of full json encoded profiles
    """
    return {"users": user.blocked_list}
