from flask import jsonify, abort, Blueprint
import datetime
from models import pharmacy

PharmaciesRoutes = Blueprint('pharmacies', __name__)


@PharmaciesRoutes.route("/pharmacies", methods=["GET"])
def get_pharmacies():
    query = pharmacy.query.all()
    pharmacies = [pharmacy.format() for pharmacy in query]
    result = {

        "success": True,
        "pharmacies": pharmacies
    }
    return jsonify(result), 200
