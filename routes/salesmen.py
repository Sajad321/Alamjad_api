from flask import jsonify, abort, Blueprint, request
import json
from models import user, report, history_of_pharmacy, history_of_user_activity, doctor, zone, pharmacy, company, item, acceptance_of_item, order, availabilty_of_item

SalesmenRoutes = Blueprint('salesmen', __name__)

# You have wrong Table name (availabilty_of_item) supposed to be (availability_of_item) #


@SalesmenRoutes.route("/reports", methods=["GET"])
def get_reports():
    query = report.query.join(user, user.id == report.user_id).join(doctor, doctor.id == report.doctor_id).join(zone, zone.id == report.zone_id).join(
        pharmacy, pharmacy.id == report.pharmacy_id).join(company, company.id == report.company_id).join(item, item.id == report.item_id).join(acceptance_of_item, acceptance_of_item.id == report.acceptance_of_item_id).filter(user.id == 2).all()

    reports = [r.short() for r in query]
    for date in reports:
        last_pharmacy_order_query = history_of_pharmacy.query.join(order, order.id == history_of_pharmacy.order_id).filter(
            history_of_pharmacy.pharmacy_id == date['pharmacy_id']).order_by(order.date_of_order).first()
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
def get_reports_form():
    zones_query = zone.query.all()
    zones = [z.format() for z in zones_query]
    pharmacies_query = pharmacy.query.all()
    pharmacies = [p.format() for p in pharmacies_query]
    doctors_query = doctor.query.all()
    docotrs = [d.short() for d in doctors_query]
    companies_query = company.query.all()
    companies = [c.format() for c in companies_query]
    items_query = item.query.all()
    items = [i.short() for i in items_query]

    results = {"zones": zones,
               "pharmacies": pharmacies,
               "doctors": docotrs,
               "companies": companies,
               "items": items,
               "success": True}
    return jsonify(results), 200


@SalesmenRoutes.route("/reports", methods=["POST"])
def post_reports_form():
    data = json.loads(request.data)
    print(data)
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

        new_availability = availabilty_of_item(
            item_id=item_id,
            available=available,
            doctor_id=doctor_id,
            pharmacy_id=pharmacy_id,
        )
        id_availability = availabilty_of_item.insert(new_availability)

        new_report = report(
            date=history,
            user_id='2',  # Change when use auth0
            zone_id=zone_id,
            doctor_id=doctor_id,
            pharmacy_id=pharmacy_id,
            company_id=company_id,
            item_id=item_id,
            acceptance_of_item_id=id_acceptance,
            availabilty_of_item_id=id_availability,
        )

        report.insert(new_report)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@SalesmenRoutes.route("/reports-form/<int:report_id>", methods=["GET"])
def edit_report_form(report_id):
    query = report.query.join(user, user.id == report.user_id).join(doctor, doctor.id == report.doctor_id).join(zone, zone.id == report.zone_id).join(
        pharmacy, pharmacy.id == report.pharmacy_id).join(company, company.id == report.company_id).join(item, item.id == report.item_id).join(acceptance_of_item, acceptance_of_item.id == report.acceptance_of_item_id).filter(user.id == 2, report.id == report_id).all()

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
def put_report_form(report_id):
    data = json.loads(request.data)
    print(data)
    acceptance_of_item_data = acceptance_of_item.query.get(
        data['acceptance_of_item'])
    availability_of_item_data = availabilty_of_item.query.get(
        data['availability_of_item'])
    report_data = report.query.get(report_id)
    try:
        history = data['history']
        # [provider, user_id] = data['user_id'].split('|')
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

        availabilty_of_item.update(availability_of_item_data)

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
