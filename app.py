from flask import Flask, jsonify
import logging
from models import setup_db
from flask_cors import CORS
from routes.auth import AuthError


def create_app(test_config=None):

    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, PATCH, OPTIONS'
        )
        return response

    setup_db(app)

    from routes.salesmen import SalesmenRoutes
    app.register_blueprint(SalesmenRoutes)
    from routes.users import UserRoutes
    app.register_blueprint(UserRoutes)
    from routes.admin import AdminRoutes
    app.register_blueprint(AdminRoutes)

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
