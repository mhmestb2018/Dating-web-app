from flask import Blueprint

from ..models.user import User
from ..utils import error, success
from ..utils.decorators import payload_required, jsonify_output, validated_required

actions = Blueprint('user_actions', __name__, url_prefix='/')

@actions.route("/user/<user_id>", methods=["POST"])
@jsonify_output
@validated_required
@payload_required
def user_actions(user_id, user, payload):
    """
    Likes, blocks and matches
    Take an action set to a bool and returns the match status
    """
    found = User.get_user(user_id=user_id)
    if not found or user.id in found.blocklist:
        return error("Utilisateur cible introuvable", 404)
    if found.id == user.id:
        return error("You narcicist fuck.", 418)
    if "block" in payload:
        if payload["block"]:
            if not user.block(found):
                return error("Tu a déjà bloqué cet utilisateur", 400)
        else:
            if not user.unblock(found):
                return error("Tu n'avais pas bloqué cet utilisateur", 400)
    elif "like" in payload:
        match = False
        if payload["like"]:
            if len(user.pictures) is 0:
                return error("Tu n'as pas de photo de profil", 403)
            if not user.like(found):
                return error("Tu a déjà liké cet utilisateur", 400)
        else:
            if not user.unlike(found):
                return error("Tu n'avais pas liké cet utilisateur", 400)
            return ({"match": False})
    else:
        return error("Aucune action valide demandée", 400)
    return ({"match": user.matches_with(found)})

@actions.route("/users/<user_id>", methods=["GET"])
@jsonify_output
@validated_required
def user_profile(user_id, user):
    """
    Returns public profile data of requested user_id
    """
    found = User.get_user(user_id=user_id)
    if not found or user.id in found.blocklist:
        return error("Utilisateur introuvable", 404)
    return success(found.public_as(user))
