from flask import jsonify, abort, Blueprint
import datetime
from models import doctor

DoctorsRoutes = Blueprint('doctors', __name__)


@DoctorsRoutes.route("/doctors", methods=["GET"])
def get_doctors():
    query = doctor.query.all()
    doctors = [doctor.format() for doctor in query]
    result = {
        "success": True,
        "doctors": doctors
    }
    return jsonify(result), 200
