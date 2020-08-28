from flask import jsonify, abort, Blueprint, request
from models import user
from .auth import requires_auth
import json
UserRoutes = Blueprint('users', __name__)


@UserRoutes.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization, true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, PUT, POST, DELETE, OPTIONS'
    )
    return response


@UserRoutes.route("/new_user", methods=["POST"])
@requires_auth("Send:names")
def check_user(token):
    print(token)
    print(json.loads(request.data))
    return "1"
