from flask import Blueprint

from ..models.tag import Tag
from ..utils.decorators import (jsonify_output, validated_required)

list_tags = Blueprint("list_tags", __name__)

@list_tags.route("/tags", methods=["GET"])
@jsonify_output
@validated_required
def get_tags(user):
    """
    List all tags
    """
    return {"tags": Tag.list()}

@list_tags.route("/tags", methods=["POST"])
@jsonify_output
@validated_required
def get_unsuscribbed_tags(user):
    """
    List unsuscribed tags
    """
    return {"tags": Tag.list(as_user=user)}
