from flask import jsonify, abort, Blueprint
import datetime
from models import User, Report

SalesmenRoutes = Blueprint('salesmen', __name__)
UserRoute = Blueprint('users', __name__)


@SalesmenRoutes.route("/reports", methods=["GET"])
def get_reports():
    query = Report.query.all()
    reports = [report.format() for report in query]
    result = {

        "success": True,
        "reports": reports
    }
    return jsonify(result), 200


@UserRoute.route("/users", methods=["GET"])
def get_users():
    query = User.query.all()
    users = [user.format() for user in query]
    results = {
        "success": True,
        "Users": users
    }
    return jsonify(results), 200
# @UsersRoutes.route("/users", methods=["POST"])
# def add_users():
#     try:

#         new_user_data = json.loads(request.data)

#         new_name = new_user_data['name']
#         new_username = new_user_data['username']
#         new_password = new_user_data['password']
#         new_email = new_user_data['username']
#         new_phone_number = new_user_data['password']
#         role = 3
#         date_of_joining = datetime.date

#         new_user = User(
#             name=new_name,
#             username=new_username,

#         )

#         User.insert(new_user)

#         user = [new_user.format()]
#         results = {
#             "success": True,
#             "user": user
#         }
#         return jsonify(results), 200
#     except BaseException:
#         abort(422)
