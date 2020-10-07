import os
from flask import Blueprint, send_from_directory

from ..models.tag import Tag
from ..utils.decorators import user_required, payload_required
from ..utils.misc import success, error

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

@private_pictures.route("/pictures/add", methods=["POST"])
@payload_required
@user_required
def add_picture(filename, payload, user):
    """
    Add a picture and returns pictures_list on success
    """
    if "files" not in payload or len(payload["files"]) == 0:
        return error("Pas de fichier joint", 403)
    if len(payload["files"]) + len(user.pictures) > 5: ######## HARDCODED LIMIT !!! #########
        return error("Vous ne pouvez pas avoir plus de 5 photos", 409)
    for f in payload["files"]:
        pass ######################################################################################
    return success(user.pictures)

@private_pictures.route("/pictures/swap", methods=["POST"])
@payload_required
@user_required
def swap_pictures(payload, user):
    """
    Swap pictures order in pictures list, returns pictures list on success
    """
    return success(user.pictures)

@private_pictures.route("/pictures/<path:filename>", methods=["DELETE"])
@user_required
def del_picture(filename, user):
    """
    Returns a user picture to logged in users
    """
    return send_from_directory(
        os.path.join(private_pictures.instance_path, 'pictures'),
        os.path.join('/data', filename)
    )
