from flask import Flask
import logging
from models import setup_db

def create_app(test_config=None):
    app = Flask(__name__)

    setup_db(app)

    from routes.salesmen import SalesmenRoutes, UserRoute
    app.register_blueprint(SalesmenRoutes)
    app.register_blueprint(UserRoute)
    from routes.pharmacies import PharmaciesRoutes
    app.register_blueprint(PharmaciesRoutes)
    from routes.doctors import DoctorsRoutes
    app.register_blueprint(DoctorsRoutes)
    from routes.company import Companyroute, Itemroute
    app.register_blueprint(Companyroute)
    app.register_blueprint(Itemroute)
    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=8080)