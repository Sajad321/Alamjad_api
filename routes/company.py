from flask import jsonify, abort, Blueprint
import datetime
from models import company, item

Companyroute = Blueprint('company', __name__)

Itemroute = Blueprint('items', __name__)


@Companyroute.route('/company', methods=['GET'])
def get_company():
    query = company.query.all()
    companies = [co.format() for co in query]
    results = {
        "success": True,
        "companies": companies

    }
    return jsonify(results), 200


@Itemroute.route('/items', methods=['GET'])
def get_items():
    query = item.query.all()
    items = [item.format() for item in query]
    results = {
        "success": True,
        "items": items
    }
    return jsonify(results), 200
