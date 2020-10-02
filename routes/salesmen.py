from flask import jsonify, abort, Blueprint, request
import json
from .auth import requires_auth
from models import user, report, history_of_pharmacy, history_of_user_activity, doctor, zone, pharmacy, company, item, acceptance_of_item, order, availability_of_item, doctor_pharmacies, notification
SalesmenRoutes = Blueprint('salesmen', __name__)


@SalesmenRoutes.route("/reports", methods=["GET"])
@requires_auth("salesmen:role")
def get_reports(token):
    [provider, user_id] = token['sub'].split("|")
    query = report.query.join(user, user.id == report.user_id).join(doctor, doctor.id == report.doctor_id).join(zone, zone.id == report.zone_id).join(
        pharmacy, pharmacy.id == report.pharmacy_id).join(company, company.id == report.company_id).join(item, item.id == report.item_id).join(acceptance_of_item, acceptance_of_item.id == report.acceptance_of_item_id).filter(user.id == user_id).order_by(report.id.desc()).all()

    reports = [r.short() for r in query]
    for date in reports:
        last_pharmacy_order_query = history_of_pharmacy.query.join(order, order.id == history_of_pharmacy.order_id).filter(
            history_of_pharmacy.pharmacy_id == date['pharmacy_id']).order_by(order.date_of_order.desc()).first()
        if last_pharmacy_order_query:
            data = history_of_pharmacy.format(last_pharmacy_order_query)
            date['last_pharmacy_order_date'] = str(
                data['last_pharmacy_order_date'])
        date['history'] = str(
            date['history'])

    result = {

        "success": True,
        "reports": reports
    }
    return jsonify(result), 200


@SalesmenRoutes.route("/reports-form", methods=["GET"])
@requires_auth("all:role")
def get_reports_form(token):
    zones_query = zone.query.all()
    zones = [z.format() for z in zones_query]
    pharmacies_query = pharmacy.query.all()
    pharmacies = [p.short() for p in pharmacies_query]
    doctors_pharmacies_query = doctor_pharmacies.query.join(
        doctor, doctor.id == doctor_pharmacies.doctor_id).all()
    doctors_pharmacies = [dp.format() for dp in doctors_pharmacies_query]
    companies_query = company.query.all()
    companies = [c.format() for c in companies_query]
    items_query = item.query.all()
    items = [i.short() for i in items_query]

    results = {"zones": zones,
               "pharmacies": pharmacies,
               "doctors_pharmacies": doctors_pharmacies,
               "companies": companies,
               "items": items,
               "success": True}
    return jsonify(results), 200


@SalesmenRoutes.route("/reports", methods=["POST"])
@requires_auth("salesmen:role")
def post_reports_form(token):
    data = json.loads(request.data)
    try:
        history = data['history']
        [provider, user_id] = data['user_id'].split('|')
        zone_id = data['zone_id']
        doctor_id = data['doctor_id']
        pharmacy_id = data['pharmacy_id']
        company_id = data['company_id']
        item_id = data['item_id']
        acceptance = data['acceptance']
        acceptance_comment = data['acceptance_comment']
        available = data['available'] == "true"
        new_acceptance = acceptance_of_item(
            item_id=item_id,
            acceptance=acceptance,
            doctor_id=doctor_id,
            pharmacy_id=pharmacy_id,
            comment=acceptance_comment,
        )
        id_acceptance = acceptance_of_item.insert(new_acceptance)

        new_availability = availability_of_item(
            item_id=item_id,
            available=available,
            doctor_id=doctor_id,
            pharmacy_id=pharmacy_id,
        )
        id_availability = availability_of_item.insert(new_availability)

        new_report = report(
            date=history,
            user_id=user_id,  # Change when use auth0
            zone_id=zone_id,
            doctor_id=doctor_id,
            pharmacy_id=pharmacy_id,
            company_id=company_id,
            item_id=item_id,
            acceptance_of_item_id=id_acceptance,
            availability_of_item_id=id_availability,
        )

        id_report = report.insert(new_report)

        user_data = user.query.get(user_id)
        user_data.daily_report = True
        user.update(user_data)

        doctor_data = doctor.query.get(doctor_id)
        doctor_data.report_activity = True
        doctor.update(doctor_data)

        new_notification = notification(report_id=id_report)

        notification.insert(new_notification)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@SalesmenRoutes.route("/reports-form/<int:report_id>", methods=["GET"])
@requires_auth("salesmen:role")
def edit_report_form(token, report_id):
    [provider, user_id] = token['sub'].split("|")
    query = report.query.join(user, user.id == report.user_id).join(doctor, doctor.id == report.doctor_id).join(zone, zone.id == report.zone_id).join(
        pharmacy, pharmacy.id == report.pharmacy_id).join(company, company.id == report.company_id).join(item, item.id == report.item_id).join(acceptance_of_item, acceptance_of_item.id == report.acceptance_of_item_id).filter(user.id == user_id, report.id == report_id).all()

    report_editor = [r.edit_report() for r in query]
    for date in report_editor:
        date['history'] = str(
            date['history'])

    result = {
        "success": True,
        "report": report_editor
    }
    return jsonify(result), 200


@SalesmenRoutes.route("/reports/<int:report_id>", methods=["PATCH"])
@requires_auth("salesmen:role")
def patch_report_form(token, report_id):
    data = json.loads(request.data)
    acceptance_of_item_data = acceptance_of_item.query.get(
        data['acceptance_of_item'])
    availability_of_item_data = availability_of_item.query.get(
        data['availability_of_item'])
    report_data = report.query.get(report_id)
    try:
        history = data['history']
        zone_id = data['zone_id']
        doctor_id = data['doctor_id']
        pharmacy_id = data['pharmacy_id']
        company_id = data['company_id']
        item_id = data['item_id']
        acceptance = data['acceptance']
        acceptance_comment = data['acceptance_comment']
        available = data['available']

        acceptance_of_item_data.item_id = item_id
        acceptance_of_item_data.acceptance = acceptance
        acceptance_of_item_data.doctor_id = doctor_id
        acceptance_of_item_data.pharmacy_id = pharmacy_id
        acceptance_of_item_data.comment = acceptance_comment

        acceptance_of_item.update(acceptance_of_item_data)

        availability_of_item_data.item_id = item_id
        availability_of_item_data.available = available
        availability_of_item_data.doctor_id = doctor_id
        availability_of_item_data.pharmacy_id = pharmacy_id

        availability_of_item.update(availability_of_item_data)

        report_data.date = history
        report_data.zone_id = zone_id
        report_data.doctor_id = doctor_id
        report_data.pharmacy_id = pharmacy_id
        report_data.company_id = company_id
        report_data.item_id = item_id

        report.update(report_data)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


#     except BaseException:
#         abort(422)
