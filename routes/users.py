from flask import jsonify, abort, Blueprint, request
from models import user
from .auth import requires_auth
import json
UserRoutes = Blueprint('users', __name__)


@UserRoutes.route("/users/<string:user_id>", methods=["GET"])
@requires_auth("check:user")
def check_role(token, user_id):
    query = user.query.get(user_id)
    user_role = query.take_role()
    return jsonify({"role": user_role}), 200


@UserRoutes.route("/users", methods=["POST"])
@requires_auth("check:user")
def check_user(token):
    data = json.loads(request.data)
    [provider, user_id] = data['sub'].split("|")
    user_data = user.query.get(user_id)
    if not user_data:
        name = data['name']
        email = data['email']
        username = data['nickname']
        new_user = user(id=user_id, name=name, email=email, username=username)
        user.insert(new_user)
    return jsonify({"success": True}), 200
