from flask import jsonify, abort, Blueprint, request
import json
from models import user, report, history_of_pharmacy, history_of_user_activity, doctor, zone, pharmacy, company, item, acceptance_of_item, order, availabilty_of_item, notification, item_order

AdminRoutes = Blueprint('admin', __name__)


@AdminRoutes.route("/main-admin", methods=['GET'])
def get_main_admin():
    users = user.query.count()
    doctors = doctor.query.count()
    pharmacies = pharmacy.query.count()
    reports = report.query.count()
    orders = order.query.count()
    items = item.query.count()

    results = {
        'users_count': users,
        'doctors_count': doctors,
        'pharmacies_count': pharmacies,
        'reports_count': reports,
        'orders_count': orders,
        'items_count': items,
    }

    return jsonify(results), 200


@AdminRoutes.route("/notifications", methods=['GET'])
def get_notifications():
    query = notification.query.join(
        report, report.id == notification.report_id).order_by(notification.id.desc()).all()
    notifications = [n.format() for n in query]
    print(notifications)
    results = {
        "success": True,
        'notifications': notifications
    }

    return jsonify(results), 200


@AdminRoutes.route("/orders", methods=['GET'])
def get_orders():
    query = order.query.join(user, user.id == order.user_id).join(doctor, doctor.id == order.doctor_id).join(zone, zone.id == order.zone_id).join(
        pharmacy, pharmacy.id == order.pharmacy_id).join(company, company.id == order.company_id).order_by(order.id.desc()).all()
    orders = [o.detail() for o in query]
    for date in orders:
        date['date_of_order'] = str(
            date['date_of_order'])
        items_query = item_order.query.join(order, order.id == item_order.order_id).join(
            item, item.id == item_order.item_id).filter(item_order.order_id == date['id']).all()
        date['items'] = [i.detail() for i in items_query]
    print(orders)
    results = {
        "success": True,
        'orders': orders
    }

    return jsonify(results), 200
