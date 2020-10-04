import os
from flask import Blueprint, send_from_directory

from ..models.tag import Tag
from ..utils.decorators import user_required

private_pictures = Blueprint("private_pictures", __name__)

@private_pictures.route("/pictures/<path:filename>", methods=["GET"])
@user_required
def get_picture(filename, user):
    """
    Returns a user picture to logged in users
    """
    return send_from_directory(
        os.path.join(private_pictures.instance_path, 'pictures'),
        os.path.join('/data', filename)
    )
