import os
from flask import Blueprint, send_from_directory, request
from werkzeug.utils import secure_filename

from .. import public_host
from ..models.tag import Tag
from ..utils.decorators import user_required, payload_required, jsonify_output
from ..utils.misc import success, error

private_pictures = Blueprint("private_pictures", __name__)

@private_pictures.route("/pictures/<path:filename>", methods=["GET"])
@user_required
def get_picture(filename, user):
    """
    Returns a user picture to logged in users
    """

    return send_from_directory('/data', filename)

@private_pictures.route("/add_picture", methods=["POST"])
@user_required
def new_picture(user):
    """
    Add a picture and returns pictures_list on success
    """
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('bmp', 'png', 'jpg', 'jpeg')
    
    if 'file' not in request.files:
        return error("Pas de fichier joint", 403)
    if len(user.pictures) == 5: ######## HARDCODED LIMIT !!! #########
        return error("Vous avez déjà 5 photos", 409)
    pic = request.files['file']
    if pic.filename == '':
        return error("Pas de fichier joint", 403)
    print(public_host, pic.filename, flush=True)
    if not allowed_file(pic.filename):
        return error(f"Fichier {pic.filename} invalide", 400)
    filename = secure_filename(pic.filename)
    new_name = f"{user.id}_{filename}"
    pic.save(os.path.join("/data", new_name))
    pic_path = f"{public_host}/pictures/{new_name}"
    pictures = user.pictures + [pic_path]
    user.update({'pictures': pictures})
    return success(user.dict, 201)

@private_pictures.route("/pictures/<path:filename>", methods=["DELETE"])
@user_required
def del_picture(filename, user):
    """
    Delete a user picture
    """
    pic_path = f"{public_host}/pictures/{filename}"
    pictures = user.pictures
    pictures.remove(pic_path)
    user.update({'pictures': pictures})
    os.remove(os.path.join("/data", filename))
    return success(user.dict)
