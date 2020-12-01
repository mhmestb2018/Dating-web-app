from flask import Blueprint

from ..utils import success
from ..utils.decorators import jsonify_output
from ..models.orientations import Orientations
from ..models.sexs import Sexs

fields = Blueprint('fields', __name__)

@jsonify_output
@fields.route("/fields", methods=["GET"])
def get_fields():
    return success({"sex": Sexs.available, "orientation": Orientations.available})
