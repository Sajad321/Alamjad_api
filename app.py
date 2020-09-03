from flask import request, Flask, jsonify, render_template, abort
import logging
from models import setup_db, order, item_order
from flask_cors import CORS
from flask_mail import Mail, Message
import json
from routes.auth import AuthError


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
    def post_order():
        data = json.loads(request.data)
        try:
            [provider, user_id] = data['user_id'].split('|')
            company_id = data['company_id']
            date_of_order = data['date_of_order']
            pharmacy_id = data['pharmacy_id']
            doctor_id = data['doctor_id']
            zone_id = data['zone_id']
            comment = data['comment']
            price = data['price']

            new_order = order(
                date_of_order=date_of_order,
                zone_id=zone_id,
                user_id=user_id,
                company_id=company_id,
                doctor_id=doctor_id,
                pharmacy_id=pharmacy_id,
                comment=comment,
                price=price
            )
            id_order = order.insert(new_order)

            items = data['items']
            for i in items:
                i_id = i['item_id']
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

            msg = Message('طلبية - نظام الاعلام الدوائي', sender='alamjads@alamjadsb.com',
                           recipients=['krvhrv188@gmail.com', 'dr.husseinfadel@alamjadpharm.com'])
            msg.html = render_template('msg.html', user=username, zone=zonename, history=date_of_order, pharmacy=pharmacy_name, co=companyname, items=itemsname_quantity_bonusintuple,
                                        gift=giftcomment)
            mail.send(msg)

            return jsonify({
                'success': True,
            }), 201

        except:
            abort(500)

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
