
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

# database_name = "trivia"
# database_path = "postgres://postgres:1@{}/{}".format(
#     'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=None):
    if database_path is None:
        app.config.from_object("config")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.create_all()
    db.app = app
    db.init_app(app)


class Base(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class user(Base):
    __tablename__ = 'user'

    id = Column(String(30), unique=True, primary_key=True)
    name = Column(String(200), nullable=False)
    username = Column(String(200), unique=True)
    email = Column(String(200), nullable=False, unique=True)
    phone_number = Column(String(15))
    date_of_joining = Column(Date)
    zone_id = Column(Integer, ForeignKey('zone.id'))
    role = Column(Integer)
    daily_report = Column(Boolean)
    histories_of_user_activity = db.relationship(
        'history_of_user_activity', backref=db.backref('user', uselist=False), lazy='dynamic')
    orders = db.relationship('order', backref=db.backref(
        'user', uselist=False), lazy='dynamic')
    histories_of_company = db.relationship(
        'history_of_company', backref=db.backref('user', uselist=False), lazy='dynamic')
    histories_of_marketing = db.relationship(
        'history_of_marketing', backref=db.backref('user', uselist=False), lazy='dynamic')
    reports = db.relationship('report', backref=db.backref(
        'user', uselist=False), lazy='dynamic')

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'zone': self.zone.zone,
            'email': self.email,
            'phone_number': self.phone_number,
            "daily_report": self.daily_report,
            'date_of_joining': self.date_of_joining,
        }

    def take_role(self):
        return self.role

    def table(self):
        return {
            'id': self.id,
            'name': self.name
        }


class history_of_user_activity(Base):
    __tablename__ = 'history_of_user_activity'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('zone.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    date = Column(Date)
    histories_of_doctor = db.relationship('history_of_doctor', backref=db.backref(
        'history_of_user_activity', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
        }


class zone(Base):
    __tablename__ = 'zone'
    id = Column(Integer, primary_key=True)
    zone = Column(String(100), nullable=False)
    users = db.relationship('user', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    histories_of_user_activity = db.relationship(
        'history_of_user_activity', backref=db.backref('zone', uselist=False), lazy='dynamic')
    pharmacies = db.relationship('pharmacy', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    orders = db.relationship('order', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    doctors = db.relationship('doctor', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')
    reports = db.relationship('report', backref=db.backref(
        'zone', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'zone': self.zone,
        }


class pharmacy(Base):
    __tablename__ = 'pharmacy'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone_number = Column(Integer, nullable=False)
    address = Column(String(200), nullable=False)
    zone_id = Column(Integer, ForeignKey('zone.id'), nullable=False)
    support = Column(String(200))
    date_of_joining = Column(Date)
    order_activity = Column(Boolean, default=False)
    histories_of_user_activity = db.relationship(
        'history_of_user_activity', backref=db.backref('pharmacy', uselist=False), lazy='dynamic')
    orders = db.relationship('order', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    acceptance_of_items = db.relationship('acceptance_of_item', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    availability_of_items = db.relationship('availability_of_item', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    histories_Of_marketing = db.relationship(
        'history_of_marketing', backref=db.backref('pharmacy', uselist=False), lazy='dynamic')
    histories_of_pharmacy = db.relationship('history_of_pharmacy', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    reports = db.relationship('report', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')
    doctors_pharmacies = db.relationship('doctor_pharmacies', backref=db.backref(
        'pharmacy', uselist=False), lazy='dynamic')

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'address': self.address,
            'zone': self.zone.zone,
            'zone_id': self.zone_id,
            'support': self.support,
            'date_of_joining': self.date_of_joining,
            'order_activity': self.order_activity
        }

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'zone_id': self.zone_id,
        }


class item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    expire_date = Column(Date, nullable=False)
    price = Column(Float)
    acceptance_of_items = db.relationship(
        'acceptance_of_item', backref=db.backref('item', uselist=False), lazy='dynamic')
    availability_of_items = db.relationship(
        'availability_of_item', backref=db.backref('item', uselist=False), lazy='dynamic')
    item_orders = db.relationship('item_order', backref=db.backref(
        'item', uselist=False), lazy='dynamic')
    reports = db.relationship('report', backref=db.backref(
        'item', uselist=False), lazy='dynamic')

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            "company_id": self.company_id,
            'company': self.company.name,
            'expire_date': self.expire_date,
            'price': self.price,
        }

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'price': self.price,
        }


class report(Base):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('zone.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    acceptance_of_item_id = Column(Integer, ForeignKey(
        "acceptance_of_item.id"), nullable=False)
    availability_of_item_id = Column(Integer, ForeignKey(
        "availability_of_item.id"), nullable=False)
    notifications = db.relationship('notification', backref=db.backref(
        'report', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'history': self.date,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'doctor_id': self.doctor_id,
            'pharmacy_id': self.pharmacy_id,
            'company_id': self.company_id,
            'item_id': self.item_id,
            'acceptance_of_item_id': self.acceptance_of_item_id,
            'availabilty_of_item_id': self.availabilty_of_item_id,
        }

    def short(self):
        return {
            'id': self.id,
            'history': self.date,
            'zone': self.zone.zone,
            'doctor': self.doctor.name,
            'pharmacy': self.pharmacy.name,
            'pharmacy_id': self.pharmacy_id,
            'company': self.company.name,
            'item': self.item.name,
            'acceptance_of_item': self.acceptance_of_item.comment,
        }

    def detail(self):
        return {
            'id': self.id,
            'history': self.date,
            'user': self.user.name,
            'zone': self.zone.zone,
            'doctor': self.doctor.name,
            'pharmacy': self.pharmacy.name,
            'pharmacy_id': self.pharmacy_id,
            'company': self.company.name,
            'item': self.item.name,
            'acceptance_of_item': self.acceptance_of_item.comment,
        }

    def edit_report(self):
        return {
            'id': self.id,
            'history': self.date,
            'user_id': self.user_id,
            'zone': {"id": self.zone.id, "zone": self.zone.zone},
            'zone_id': self.zone_id,
            'doctor': {"id": self.doctor.id, "name": self.doctor.name},
            'doctor_id': self.doctor_id,
            'pharmacy': {"id": self.pharmacy.id, "name": self.pharmacy.name},
            'pharmacy_id': self.pharmacy_id,
            'company': {"id": self.company.id, "name": self.company.name},
            'company_id': self.company_id,
            'item': {"id": self.item.id, "name": self.item.name},
            'item_id': self.item_id,
            'acceptance_of_item': self.acceptance_of_item.id,
            'acceptance': self.acceptance_of_item.acceptance,
            'acceptance_comment': self.acceptance_of_item.comment,
            'availability_of_item': self.availability_of_item.id,
            'available': self.availability_of_item.available
        }

    def get_date(self):
        return self.date


class order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('zone.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=True)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    comment = Column(String(200))
    date_of_order = Column(Date, nullable=False)
    approved = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    histories_of_doctor = db.relationship(
        'history_of_doctor', backref=db.backref('order', uselist=False), lazy='dynamic')
    histories_of_pharmacy = db.relationship(
        'history_of_pharmacy', backref=db.backref('order', uselist=False), lazy='dynamic')
    item_orders = db.relationship('item_order', backref=db.backref(
        'order', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_id': self.zone_id,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'comment': self.comment,
            'date_of_order': self.date_of_order,
        }

    def detail(self):
        return {
            'id': self.id,
            'approval': self.approved,
            'user': self.user.name,
            'zone': self.zone.zone,
            'pharmacy': self.pharmacy.name,
            'doctor_id': self.doctor_id,
            'company': self.company.name,
            'comment': self.comment,
            'price': self.price,
            'date_of_order': self.date_of_order
        }

    def get_date(self):
        return self.date_of_order


class item_order(Base):
    __tablename__ = 'item_order'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    quantity = Column(Integer, default=1)
    bonus = Column(Float)
    gift = Column(Boolean, default=False)

    def format(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
        }

    def detail(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_id': self.item_id,
            'item_name': self.item.name,
            'quantity': self.quantity,
            'bonus': self.bonus,
            'gift': self.gift,
        }


class acceptance_of_item(Base):
    __tablename__ = 'acceptance_of_item'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    acceptance = Column(String(200), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    comment = Column(String(500))
    reports = db.relationship('report', backref=db.backref(
        'acceptance_of_item', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'acceptance': self.acceptance,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
            'comment': self.comment,
        }


class availability_of_item(Base):
    __tablename__ = 'availability_of_item'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    available = Column(Boolean, nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    reports = db.relationship('report', backref=db.backref(
        'availability_of_item', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'acceptance': self.acceptance,
            'pharmacy_id': self.pharmacy_id,
            'doctor_id': self.doctor_id,
        }


class company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    items = db.relationship('item', backref=db.backref(
        'company', uselist=False), lazy='dynamic')
    histories_of_company = db.relationship('history_of_company', backref=db.backref(
        'company', uselist=False), lazy='dynamic')
    orders = db.relationship('order', backref=db.backref(
        'company', uselist=False), lazy='dynamic')
    reports = db.relationship('report', backref=db.backref(
        'company', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class history_of_company(Base):
    __tablename__ = "history_of_company"
    id = Column(Integer, nullable=False, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    date = Column(Date)

    def format(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'user_id': self.user_id,
            'date': self.date
        }


class history_of_marketing(Base):
    __tablename__ = "history_of_marketing"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    date = Column(Date)

    def format(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'user_id': self.user_id,
            'pharmacy_id': self.pharmacy_id,
            'date': self.date,
        }


class doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(12))
    email = Column(String(100))
    zone_id = Column(Integer, ForeignKey('zone.id'))
    speciality = Column(String(200), nullable=False)
    d_class = Column(String(2))
    support = Column(String(200), nullable=False)
    date_of_joining = Column(Date)
    report_activity = Column(Boolean, default=False)
    histories_of_user_activity = db.relationship(
        'history_of_user_activity', backref=db.backref('doctor', uselist=False), lazy='dynamic')
    orders = db.relationship('order', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    acceptance_of_items = db.relationship('acceptance_of_item', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    availability_of_items = db.relationship(
        'availability_of_item', backref=db.backref('doctor', uselist=False), lazy='dynamic')
    histories_of_marketing = db.relationship(
        'history_of_marketing', backref=db.backref('doctor', uselist=False), lazy='dynamic')
    histories_of_doctor = db.relationship('history_of_doctor', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    reports = db.relationship('report', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')
    doctors_pharmacies = db.relationship('doctor_pharmacies', backref=db.backref(
        'doctor', uselist=False), lazy='dynamic')

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'zone_id': self.zone_id,
            'zone': self.zone.zone,
            'speciality': self.speciality,
            'd_class': self.d_class,
            'support': self.support,
            'date_of_joining': self.date_of_joining,
            'report_activity': self.report_activity,
        }

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'zone_id': self.zone_id,

        }

    def d_name(self):
        return self.name


class history_of_doctor(Base):
    __tablename__ = 'history_of_doctor'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    visit_id = Column(Integer, ForeignKey(
        'history_of_user_activity.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'visit': self.visit_id,
            'order': self.order_id
        }


class history_of_pharmacy(Base):
    __tablename__ = 'history_of_pharmacy'
    id = Column(Integer, primary_key=True)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

    def format(self):
        return {
            'last_pharmacy_order_date': self.order.date_of_order
        }


class doctor_pharmacies(Base):
    __tablename__ = 'doctor_pharmacies'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'))

    def format(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'name': self.doctor.name,
            'pharmacy_id': self.pharmacy_id,
        }

    def detail(self):
        return {
            'id': self.id,
            'pharmacy_id': self.pharmacy_id,
            'name': self.pharmacy.name,
        }


class notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('report.id'))
    seen = Column(Boolean, default=False)

    def format(self):
        return {
            'id': self.id,
            'report': self.report.user.name,
            'seen': self.seen
        }
