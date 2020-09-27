from flask import request, Flask, jsonify, render_template, abort
import logging
from models import setup_db, order, item_order, history_of_pharmacy, user, pharmacy, doctor
from flask_cors import CORS
from flask_mail import Mail, Message
import json
from pytz import timezone
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from routes.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.update(
        # EMAIL SETTINGS
        MAIL_SERVER='mail.alamjadsb.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_USERNAME='_mainaccount@alamjadsb.com',
        MAIL_PASSWORD='1Sy9Lp9c7b'
    )
    mail = Mail(app)

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

    @app.route('/orders', methods=['POST'])
    @requires_auth("all:role")
    def post_order(token):
        data = json.loads(request.data)
        try:
            [provider, user_id] = data['user_id'].split('|')
            user_name = data['user_name']
            company_id = data['company_id']
            company_name = data['company_name']
            date_of_order = data['date_of_order']
            pharmacy_id = data['pharmacy_id']
            pharmacy_name = data['pharmacy_name']
            zone_id = data['zone_id']
            zone_name = data['zone_name']
            comment = data['comment']
            price = data['price']
            if data['doctor_id'] != "":
                doctor_id = data['doctor_id']
                new_order = order(
                    date_of_order=date_of_order,
                    zone_id=zone_id,
                    user_id=user_id,
                    company_id=company_id,
                    pharmacy_id=pharmacy_id,
                    doctor_id=doctor_id,
                    comment=comment,
                    price=price
                )
                id_order = order.insert(new_order)
            else:
                new_order = order(
                    date_of_order=date_of_order,
                    zone_id=zone_id,
                    user_id=user_id,
                    company_id=company_id,
                    pharmacy_id=pharmacy_id,
                    comment=comment,
                    price=price
                )
                id_order = order.insert(new_order)

            items = data['items']
            for i in items:
                i_id = i['item_id']
                i_name = i['item_name']
                i_qty = i['qty']
                i_bonus = int(i['bonus'])
                i_gift = i['gift'] == "true"
                new_item_order = item_order(
                    item_id=i_id,
                    order_id=id_order,
                    quantity=i_qty,
                    bonus=i_bonus,
                    gift=i_gift
                )
                item_order.insert(new_item_order)

            new_history_of_pharmacy = history_of_pharmacy(
                pharmacy_id=pharmacy_id, order_id=id_order)
            history_of_pharmacy.insert(new_history_of_pharmacy)
            msg = Message('طلبية - نظام الاعلام الدوائي', sender='alamjads@alamjadsb.com',
                          recipients=['dr.adnan@alamjadpharm.com', 'dr.husseinfadel@alamjadpharm.com'])
            msg.html = render_template('msg.html', user=user_name, zone=zone_name, history=date_of_order, pharmacy=pharmacy_name, co=company_name, items=items,
                                       gift=comment)
            mail.send(msg)

            return jsonify({
                'success': True,
            }), 201

        except:
            abort(500)

    cron = BackgroundScheduler(daemon=True)

    cron.start()

    @cron.scheduled_job(trigger="cron", day="*/1", timezone=timezone("Asia/Baghdad"), misfire_grace_time=None)
    def salesmen_refresh_daily_report():
        for row in user.query.filter(user.role == 3).all():
            row.daily_report = False
        user.update(user.query.filter(user.role == 3).all())

    @cron.scheduled_job(trigger="cron", day="*/20", timezone=timezone("Asia/Baghdad"), misfire_grace_time=None)
    def doctors_refresh_report_activity():
        for row in doctor.query.all():
            row.report_activity = False
        doctor.update(doctor.query.all())

    @cron.scheduled_job(trigger="cron", month="*/1", timezone=timezone("Asia/Baghdad"), misfire_grace_time=None)
    def pharmacies_refresh_monthly_order():
        for row in pharmacy.query.all():
            row.order_activity = False
        pharmacy.update(pharmacy.query.all())

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: cron.shutdown())

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)  # , use_reloader=False
