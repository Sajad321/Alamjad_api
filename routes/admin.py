from flask import jsonify, abort, Blueprint, request
import json
from .auth import requires_auth
from models import user, report, history_of_pharmacy, history_of_user_activity, doctor, zone, pharmacy, doctor_pharmacies, company, item, acceptance_of_item, order, availability_of_item, notification, item_order

AdminRoutes = Blueprint('admin', __name__)


@AdminRoutes.route("/main-admin", methods=['GET'])
@requires_auth("all:role")
def get_main_admin(token):
    users = user.query.filter(user.role == 3).count()
    doctors = doctor.query.count()
    pharmacies = pharmacy.query.count()
    reports = report.query.count()
    orders = order.query.count()
    items = item.query.count()

    results = {
        "success": True,
        'users_count': users,
        'doctors_count': doctors,
        'pharmacies_count': pharmacies,
        'reports_count': reports,
        'orders_count': orders,
        'items_count': items,
    }

    return jsonify(results), 200


@AdminRoutes.route("/notifications", methods=['GET'])
@requires_auth("admin:role")
def get_notifications(token):
    query = notification.query.join(
        report, report.id == notification.report_id).order_by(notification.id.desc()).all()
    notifications = [n.format() for n in query]
    results = {
        "success": True,
        'notifications': notifications
    }

    return jsonify(results), 200


@AdminRoutes.route("/orders", methods=['GET'])
@requires_auth("admin:role")
def get_orders(token):
    query = order.query.join(user, user.id == order.user_id).join(zone, zone.id == order.zone_id).join(
        pharmacy, pharmacy.id == order.pharmacy_id).join(company, company.id == order.company_id).order_by(order.id.desc()).all()
    orders = [o.detail() for o in query]
    for date in orders:
        date['date_of_order'] = str(
            date['date_of_order'])
        doctor_query = doctor.query.get(date['doctor_id'])
        if doctor_query:
            date['doctor'] = doctor.d_name(doctor_query)
        items_query = item_order.query.join(order, order.id == item_order.order_id).join(
            item, item.id == item_order.item_id).filter(item_order.order_id == date['id']).all()
        date['items'] = [i.detail() for i in items_query]
        date["seeMore"] = {"order_id": date['id'], "see": False}
    results = {
        "success": True,
        'orders': orders
    }

    return jsonify(results), 200


@AdminRoutes.route("/orders/<int:order_id>", methods=['PATCH'])
@requires_auth("admin:role")
def patch_orders(token, order_id):
    data = json.loads(request.data)
    order_data = order.query.get(order_id)
    try:
        order_data.approved = int(data['approved'])
        order.update(order_data)
        results = {
            "success": True,
        }

        return jsonify(results), 200

    except:
        abort(500)


@AdminRoutes.route("/reports-detail", methods=["GET"])
@requires_auth("admin:role")
def get_reports_detail(token):
    query = report.query.join(user, user.id == report.user_id).join(doctor, doctor.id == report.doctor_id).join(zone, zone.id == report.zone_id).join(
        pharmacy, pharmacy.id == report.pharmacy_id).join(company, company.id == report.company_id).join(item, item.id == report.item_id).join(acceptance_of_item, acceptance_of_item.id == report.acceptance_of_item_id).order_by(report.id.desc()).all()

    reports = [r.detail() for r in query]
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


@AdminRoutes.route("/users-detail", methods=["GET"])
@requires_auth("admin:role")
def get_users_detail(token):
    query = user.query.join(zone, zone.id == user.zone_id).filter(
        user.role == 3).all()
    users = [u.detail() for u in query]

    for u in users:
        u['reports_count'] = report.query.filter(
            report.user_id == u['id']).count()
        u['date_of_joining'] = str(
            u['date_of_joining'])
    result = {
        "success": True,
        "users": users
    }
    return jsonify(result), 200


@AdminRoutes.route("/doctors-detail", methods=["GET"])
@requires_auth("admin:role")
def get_doctors_detail(token):
    query = doctor.query.join(zone, zone.id == doctor.zone_id).all()

    doctors = [d.detail() for d in query]

    for d in doctors:
        doctors_pharmacies_query = doctor_pharmacies.query.join(
            doctor, doctor.id == doctor_pharmacies.doctor_id).join(pharmacy, pharmacy.id == doctor_pharmacies.pharmacy_id).filter(doctor_pharmacies.doctor_id == d['id']).all()
        doctors_pharmacies = [dp.detail() for dp in doctors_pharmacies_query]
        d["pharmacies"] = doctors_pharmacies
        d['date_of_joining'] = str(
            d['date_of_joining'])

    result = {

        "success": True,
        "doctors": doctors
    }
    return jsonify(result), 200


@AdminRoutes.route("/doctors-form", methods=["GET"])
@requires_auth("admin:role")
def get_doctors_form(token):
    zones_query = zone.query.all()
    zones = [z.format() for z in zones_query]
    pharmacies_query = pharmacy.query.all()
    pharmacies = [p.short() for p in pharmacies_query]

    results = {"zones": zones,
               "pharmacies": pharmacies,
               "success": True}
    return jsonify(results), 200


@AdminRoutes.route("/doctors", methods=["POST"])
@requires_auth("admin:role")
def post_doctors_form(token):
    data = json.loads(request.data)
    try:
        name = data['name']
        date_of_joining = data['date_of_joining']
        email = data['email']
        zone_id = data['zone_id']
        phone = data['phone']
        speciality = data['speciality']
        d_class = data['d_class']
        support = data['support']

        new_doctor = doctor(
            name=name,
            date_of_joining=date_of_joining,
            email=email,
            zone_id=zone_id,
            phone=phone,
            speciality=speciality,
            d_class=d_class,
            support=support
        )

        id_doctor = doctor.insert(new_doctor)

        pharmacies = data['pharmacies']
        for p in pharmacies:
            new_doctor_pharmacy = doctor_pharmacies(
                doctor_id=id_doctor, pharmacy_id=p['pharmacy_id'])
            doctor_pharmacies.insert(new_doctor_pharmacy)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@AdminRoutes.route("/doctors/<int:doctor_id>", methods=["PATCH"])
@requires_auth("admin:role")
def edit_doctor_form(token, doctor_id):
    data = json.loads(request.data)
    doctor_data = doctor.query.get(doctor_id)
    try:
        name = data['name']
        if data['phone']:
            phone = data['phone']
            doctor_data.phone = phone
        if data['email']:
            email = data['email']
            doctor_data.email = email
        zone_id = data['zone_id']
        speciality = data['speciality']
        d_class = data['d_class']
        support = data['support']
        date_of_joining = data['date_of_joining']

        doctor_data.name = name
        doctor_data.zone_id = zone_id
        doctor_data.speciality = speciality
        doctor_data.d_class = d_class
        doctor_data.support = support
        doctor_data.date_of_joining = date_of_joining

        doctor.update(doctor_data)

        pharmacies = data['pharmacies']
        for p in pharmacies:
            if p['id']:
                doctor_pharmacies_data = doctor_pharmacies.query.get(p['id'])
                doctor_pharmacies_data.pharmacy_id = p['pharmacy_id']
                doctor_pharmacies.update(doctor_pharmacies_data)
            else:
                new_doctor_pharmacy = doctor_pharmacies(
                    doctor_id=doctor_id, pharmacy_id=p['pharmacy_id'])
                doctor_pharmacies.insert(new_doctor_pharmacy)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@ AdminRoutes.route("/pharmacies-detail", methods=["GET"])
@ requires_auth("admin:role")
def get_pharmacies_detail(token):
    query = pharmacy.query.join(zone, zone.id == pharmacy.zone_id).all()

    pharmacies = [p.detail() for p in query]

    for p in pharmacies:
        p['date_of_joining'] = str(
            p['date_of_joining'])

    result = {

        "success": True,
        "pharmacies": pharmacies
    }
    return jsonify(result), 200


@ AdminRoutes.route("/pharmacies-form", methods=["GET"])
@ requires_auth("admin:role")
def get_pharmacies_form(token):
    zones_query = zone.query.all()
    zones = [z.format() for z in zones_query]

    results = {"zones": zones,
               "success": True}
    return jsonify(results), 200


@ AdminRoutes.route("/pharmacies", methods=["POST"])
@ requires_auth("admin:role")
def post_pharmacies_form(token):
    data = json.loads(request.data)
    try:
        name = data['name']
        date_of_joining = data['date_of_joining']
        phone_number = data['phone_number']
        zone_id = data['zone_id']
        address = data['address']
        support = data['support']

        new_pharmacy = pharmacy(
            name=name,
            date_of_joining=date_of_joining,
            phone_number=phone_number,
            zone_id=zone_id,
            address=address,
            support=support
        )

        pharmacy.insert(new_pharmacy)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@AdminRoutes.route("/pharmacies/<int:pharmacy_id>", methods=["PATCH"])
@requires_auth("admin:role")
def edit_pharmacy_form(token, pharmacy_id):
    data = json.loads(request.data)
    pharmacy_data = pharmacy.query.get(pharmacy_id)
    try:
        name = data['name']
        if data['phone_number']:
            phone_number = data['phone_number']
            pharmacy_data.phone_number = phone_number
        zone_id = data['zone_id']
        address = data['address']
        support = data['support']
        date_of_joining = data['date_of_joining']

        pharmacy_data.name = name
        pharmacy_data.phone_number = phone_number
        pharmacy_data.zone_id = zone_id
        pharmacy_data.address = address
        pharmacy_data.support = support
        pharmacy_data.date_of_joining = date_of_joining

        pharmacy.update(pharmacy_data)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@AdminRoutes.route("/companies", methods=["GET"])
@requires_auth("admin:role")
def get_companies(token):
    query = company.query.all()

    companies = [c.format() for c in query]

    result = {

        "success": True,
        "companies": companies
    }
    return jsonify(result), 200


@AdminRoutes.route("/companies", methods=["POST"])
@requires_auth("admin:role")
def post_companies_form(token):
    data = json.loads(request.data)
    try:
        name = data['name']

        new_company = company(
            name=name
        )

        company.insert(new_company)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@AdminRoutes.route("/companies/<int:company_id>", methods=["PATCH"])
@requires_auth("admin:role")
def edit_companies_form(token, company_id):
    data = json.loads(request.data)
    company_data = company.query.get(company_id)
    try:
        name = data['name']

        company_data.name = name

        company.update(company_data)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@AdminRoutes.route("/items-detail", methods=["GET"])
@requires_auth("admin:role")
def get_items_detail(token):
    query = item.query.join(company, company.id == item.company_id).all()

    items = [i.detail() for i in query]

    for i in items:
        i['expire_date'] = str(
            i['expire_date'])

    result = {

        "success": True,
        "items": items
    }
    return jsonify(result), 200


@AdminRoutes.route("/items-form", methods=["GET"])
@requires_auth("admin:role")
def get_items_form(token):
    companies_query = company.query.all()
    companies = [c.format() for c in companies_query]

    results = {"companies": companies,
               "success": True}
    return jsonify(results), 200


@AdminRoutes.route("/items", methods=["POST"])
@requires_auth("admin:role")
def post_items_form(token):
    data = json.loads(request.data)
    try:
        name = data['name']
        company_id = data['company_id']
        expire_date = data['expire_date']
        price = int(data['price'])
        new_item = item(
            name=name,
            company_id=company_id,
            expire_date=expire_date,
            price=price
        )

        item.insert(new_item)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)


@AdminRoutes.route("/items/<int:item_id>", methods=["PATCH"])
@requires_auth("admin:role")
def edit_items_form(token, item_id):
    data = json.loads(request.data)
    item_data = item.query.get(item_id)
    try:
        name = data['name']
        company_id = data['company_id']
        expire_date = data['expire_date']
        price = int(data['price'])

        item_data.name = name
        item_data.company_id = company_id
        item_data.expire_date = expire_date
        item_data.price = price

        item.update(item_data)

        return jsonify({
            'success': True,
        }), 201

    except:
        abort(500)
