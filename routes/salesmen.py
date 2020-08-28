from flask import jsonify, abort, Blueprint
from models import user, report, history_of_pharmacy, history_of_user_activity, doctor, zone, pharmacy, company, item, acceptance_of_item, order

SalesmenRoutes = Blueprint('salesmen', __name__)


@SalesmenRoutes.route("/reports", methods=["GET"])
def get_reports():
    query = report.query.join(user, user.id == report.user_id).join(history_of_pharmacy, history_of_pharmacy.id == report.history_of_pharmacy_id).join(doctor, doctor.id == report.doctor_id).join(zone, zone.id == report.zone_id).join(
        pharmacy, pharmacy.id == report.pharmacy_id).join(company, company.id == report.company_id).join(item, item.id == report.item_id).join(acceptance_of_item, acceptance_of_item.id == report.acceptance_of_item_id).join(order, order.id == history_of_pharmacy.order_id).filter(user.id == 2).all()

    reports = [r.short() for r in query]
    for date in reports:
        date['last_pharmacy_order_date'] = str(
            date['last_pharmacy_order_date'])

    result = {

        "success": True,
        "reports": reports
    }
    return jsonify(result), 200

#     except BaseException:
#         abort(422)
